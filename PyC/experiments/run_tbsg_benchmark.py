#!/usr/bin/env python3
"""
Self-Contained Benchmark Runner:
CBM vs CEM vs Hybrid with Causal Intervention & Safe weights_only Deserialization.
"""

import os
import sys
import argparse
import time
import json
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# Add current directory to path for local imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import ConceptBottleneckModel, ConceptEmbeddingModel, HybridTBSGModel

def parse_args():
    parser = argparse.ArgumentParser(description="TBSG Empirical Benchmark on NIDS")
    parser.add_argument("--epochs", type=int, default=10, help="Training epochs per model")
    parser.add_argument("--batch-size", type=int, default=256, help="Batch size for training")
    parser.add_argument("--lr", type=float, default=0.002, help="Learning rate")
    parser.add_argument("--n-train", type=int, default=40000, help="Number of training samples")
    parser.add_argument("--n-test", type=int, default=15000, help="Number of test samples")
    parser.add_argument("--data-path", type=str, 
                        default="/root/workspace/workspace/03-Code/Projects/Legacy/centralized_datasets/processed/nids_unsw_nb15_concepts.pt",
                        help="Path to preprocessed .pt dataset")
    parser.add_argument("--output-dir", type=str,
                        default="/root/workspace/workspace/03-Code/Projects/Legacy/centralized_datasets/audit/results",
                        help="Output directory for results")
    return parser.parse_args()


def main():
    args = parse_args()
    torch.manual_seed(42)
    np.random.seed(42)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[*] Executing TBSG Benchmark on device: {device}")

    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Safe Deserialization Check
    print(f"[*] Loading dataset from: {args.data_path}")
    print("    Testing safe load: torch.load(..., weights_only=True)...")
    try:
        data = torch.load(args.data_path, weights_only=True)
        print("    --> [PASSED] Safe weights_only=True deserialization succeeded!")
    except Exception as e:
        print(f"    --> [FAILED] Safe load failed: {e}")
        sys.exit(1)

    train_X = data["train_X"][:args.n_train]
    train_C = data["train_C"][:args.n_train]
    train_y = data["train_y"][:args.n_train]

    test_X = data["test_X"][:args.n_test]
    test_C = data["test_C"][:args.n_test]
    test_y = data["test_y"][:args.n_test]

    num_concepts = train_C.shape[1]
    input_dim = train_X.shape[1]

    train_loader = DataLoader(TensorDataset(train_X, train_C, train_y), batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(TensorDataset(test_X, test_C, test_y), batch_size=512, shuffle=False)

    print(f"[*] Train set: {len(train_X)} samples | Test set: {len(test_X)} samples")
    print(f"[*] Input features: {input_dim} | Concepts: {num_concepts}")

    # 2. Train Candidates
    def train(model, name, lambda_c=1.5):
        print(f"\n[*] Training {name} ({args.epochs} epochs)...")
        model.to(device)
        opt = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-5)
        bce_task = nn.BCEWithLogitsLoss()
        mse_c = nn.MSELoss()

        model.train()
        for ep in range(args.epochs):
            loss_sum, task_sum, c_sum = 0.0, 0.0, 0.0
            for bx, bc, by in train_loader:
                bx, bc, by = bx.to(device), bc.to(device), by.to(device)
                opt.zero_grad()
                yl, cp = model(bx)
                lt = bce_task(yl, by)
                lc = mse_c(cp, bc)
                loss = lt + lambda_c * lc
                loss.backward()
                opt.step()
                loss_sum += loss.item()
                task_sum += lt.item()
                c_sum += lc.item()

            if (ep + 1) % 2 == 0 or ep == args.epochs - 1:
                print(f"    Epoch {ep+1:02d}/{args.epochs:02d} | Loss: {loss_sum/len(train_loader):.4f} "
                      f"(Task: {task_sum/len(train_loader):.4f}, Concept: {c_sum/len(train_loader):.4f})")
        return model

    cbm = train(ConceptBottleneckModel(input_dim, num_concepts), "CBM (Concept Bottleneck Model)")
    cem = train(ConceptEmbeddingModel(input_dim, num_concepts), "CEM (Concept Embedding Model)")
    hybrid = train(HybridTBSGModel(input_dim, num_concepts), "Hybrid TBSG Model (Gated-CEM)")

    # 3. Evaluate Observational vs Causal Interventions
    print("\n" + "="*75)
    print("[*] Evaluating Observational vs Causal Interventions under TBSG")
    print("="*75)

    def evaluate(model, name):
        model.eval()
        all_y_true, all_y_prob_obs, all_c_true, all_c_pred = [], [], [], []
        all_y_prob_tgt, all_y_prob_full = [], []

        mask_tgt = torch.zeros((1, num_concepts), device=device)
        mask_tgt[0, [0, 4, 5]] = 1.0  # Volumetric, Density, Protocol anomalies
        vals_zero = torch.zeros((1, num_concepts), device=device)
        mask_full = torch.ones((1, num_concepts), device=device)

        with torch.no_grad():
            for bx, bc, by in test_loader:
                bx, bc, by = bx.to(device), bc.to(device), by.to(device)
                B = bx.shape[0]

                # Observational
                yl, cp = model(bx)
                yp = torch.sigmoid(yl)

                # Targeted Intervention: do(Volumetric=0, Density=0, Protocol=0)
                yl_tgt, _ = model(bx, mask_tgt.expand(B, -1), vals_zero.expand(B, -1))
                yp_tgt = torch.sigmoid(yl_tgt)

                # Full Intervention: do(C = 0)
                yl_full, _ = model(bx, mask_full.expand(B, -1), vals_zero.expand(B, -1))
                yp_full = torch.sigmoid(yl_full)

                all_y_true.extend(by.cpu().numpy())
                all_y_prob_obs.extend(yp.cpu().numpy())
                all_c_true.append(bc.cpu().numpy())
                all_c_pred.append(cp.cpu().numpy())
                all_y_prob_tgt.extend(yp_tgt.cpu().numpy())
                all_y_prob_full.extend(yp_full.cpu().numpy())

        y_true = np.array(all_y_true)
        y_prob = np.array(all_y_prob_obs)
        y_pred = (y_prob > 0.5).astype(int)
        y_tgt = np.array(all_y_prob_tgt)
        y_full = np.array(all_y_prob_full)

        c_true = np.vstack(all_c_true)
        c_pred = np.vstack(all_c_pred)

        acc = accuracy_score(y_true, y_pred)
        f1 = f1_score(y_true, y_pred)
        auc = roc_auc_score(y_true, y_prob)
        c_mse = np.mean((c_true - c_pred)**2)

        atk_mask = (y_true == 1.0)
        base_atk_p = float(np.mean(y_prob[atk_mask]))
        tgt_atk_p = float(np.mean(y_tgt[atk_mask]))
        full_atk_p = float(np.mean(y_full[atk_mask]))

        lbl = float(np.mean(y_full[atk_mask] > 0.5) * 100.0)
        cie_tgt = float((base_atk_p - tgt_atk_p) / (base_atk_p + 1e-12) * 100.0)
        cie_full = float((base_atk_p - full_atk_p) / (base_atk_p + 1e-12) * 100.0)

        return {
            "name": name,
            "observational": {
                "accuracy": float(acc),
                "f1": float(f1),
                "auc": float(auc),
                "concept_mse": float(c_mse)
            },
            "causal_intervention": {
                "base_attack_prob": base_atk_p,
                "targeted_attack_prob": tgt_atk_p,
                "full_attack_prob": full_atk_p,
                "cie_targeted_pct": cie_tgt,
                "cie_full_pct": cie_full,
                "latent_bypass_leakage_pct (TBSG Violation)": lbl
            }
        }

    results = [
        evaluate(cbm, "CBM (Concept Bottleneck Model)"),
        evaluate(cem, "CEM (Concept Embedding Model)"),
        evaluate(hybrid, "Hybrid TBSG Model (Gated-CEM)")
    ]

    out_file = os.path.join(args.output_dir, "tbsg_cbm_cem_hybrid_results.json")
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\n" + "="*95)
    print("TBSG BENCHMARK MATRIX: UNSW-NB15 NIDS")
    print("="*95)
    print(f"{'Model Architecture':<30} | {'Test Acc':<9} | {'ROC-AUC':<8} | {'Targeted CIE%':<14} | {'Full CIE%':<10} | {'LBL % (TBSG Leak)':<18}")
    print("-" * 95)
    for r in results:
        obs, ci = r["observational"], r["causal_intervention"]
        print(f"{r['name']:<30} | {obs['accuracy']*100:.2f}%    | {obs['auc']:.4f}   | {ci['cie_targeted_pct']:.2f}%        | {ci['cie_full_pct']:.2f}%    | {ci['latent_bypass_leakage_pct (TBSG Violation)']:.2f}%")
    print("="*95)
    print(f"Results saved to: {out_file}")

if __name__ == "__main__":
    main()

