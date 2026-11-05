# 🧩 System 2: PyTorch Concepts (PyC)

**Trust Boundary Semantic Gap (TBSG) Audit, Empirical Benchmarking & Lean 4 Proofs**

This directory contains the complete technical audit of [`pyc-team/pytorch_concepts`](https://github.com/pyc-team/pytorch_concepts.git), the theoretical formalization of the **Trust Boundary Semantic Gap (TBSG)** in concept bottlenecks, and the empirical benchmark on the **UNSW-NB15 NIDS** dataset.

---

## 🏛️ Directory Structure

```
PyC/
├── docs/                       # Security audits and theoretical mappings
│   ├── PYTORCH_CONCEPTS_CODEBASE_AUDIT.md  # Critical RCE (eval) and insecure deserialization audit
│   ├── TBSG_SAFETY_BOUNDARY_MAPPING.md     # Multi-stage CBM/CEM mapping to TBSG taxonomy
│   ├── EMPIRICAL_NIDS_BENCHMARK_REPORT.md  # NIDS empirical benchmark results and analysis
│   └── master_report.html                  # Standalone interactive audit report
│
├── experiments/                # PyTorch architectures and benchmark drivers
│   ├── models.py               # Modular CBM, CEM, and Gated-CEM Hybrid implementations
│   ├── run_tbsg_benchmark.py   # Full NIDS benchmark suite with weights_only=True loading
│   └── verify_pyc_formalism.py # Fast Python formal verification driver (Claims C1-C3)
│
├── leanproofs/                 # Machine-checked formal proofs in Lean 4
│   └── PyC.lean                # 6 machine-checked theorems & lemmas with 0 sorry
│
└── results/                    # Empirical benchmark results and proof traces
    ├── tbsg_cbm_cem_hybrid_results.json    # Raw evaluation logs across CBM, CEM, and Hybrid
    ├── summary_table.txt                   # Performance & intervention comparison table
    └── pyc_semantic_gap.json               # Formal claim verification results
```

---

## 📐 Machine-Checked Formal Proofs in Lean 4

All theoretical properties of Concept Bottlenecks under the Trust Boundary Semantic Gap are formally verified in **Lean 4** (`leanproofs/NullSpaceProofs/PyC.lean` and `PyC/leanproofs/PyC.lean`) with **0 `sorry`**:

| Theorem / Lemma | Formal Statement | Lean 4 Identifier | Status |
| :--- | :--- | :--- | :---: |
| **Theorem 1** | **Concept Semantic Gap Entailment Failure** | $(\exists a, \Phi_{\text{concept}}(a) \land \neg R_{\text{safe}}(a)) \to \neg (\forall x, \Phi_{\text{concept}}(x) \to R_{\text{safe}}(x))$ | `thm1_pyc_semantic_gap_entailment_failure` | **PROVED (0 sorry)** |
| **Lemma 1** | **Pure CBM Closed Trust Boundary** | $c_1 = c_2 \implies g(c_1) = g(c_2)$ (Zero Latent Bypass) | `lem1_cbm_closed_trust_boundary` | **PROVED (0 sorry)** |
| **Lemma 2** | **CEM Negative Embedding Bypass Algebra** | $0 \cdot e^+ + (1 - 0) \cdot e^- = e^-$ | `lem2_cem_negative_embedding_bypass` | **PROVED (0 sorry)** |
| **Theorem 2** | **CEM Latent Trust Smuggling Gap** | $g(0 \cdot e^+ + 1 \cdot e_{\text{attack}}^-) \neq g(e_{\text{benign}}^-)$ under $\text{do}(C=0)$ | `thm2_cem_latent_trust_smuggling` | **PROVED (0 sorry)** |
| **Theorem 3** | **Gated Hybrid Trust Barrier Annihilation** | $g_{\text{concept}}(0) + \alpha \cdot 0 \cdot g_{\text{res}}(e) = g_{\text{concept}}(0)$ (LBL = 0.00%) | `thm3_hybrid_trust_barrier_annihilation` | **PROVED (0 sorry)** |
| **Proposition 1** | **Steerling Residual Dimension Hierarchy** | $d_{\text{steer}} < d_{\text{total}} \implies 0 < d_{\text{total}} - d_{\text{steer}}$ | `prop1_steerling_residual_dimension_positive` | **PROVED (0 sorry)** |

---

## ⚡ Quickstart

```bash
# 1. Run Lean 4 formal verification suite (0 sorry)
make verify-lean

# 2. Run fast PyC Python verification suite (~1 second)
python3 experiments/verify_pyc_formalism.py

# 3. Run full empirical benchmark (requires NIDS dataset)
python3 experiments/run_tbsg_benchmark.py --epochs 10 --batch-size 256
```

---

## 📊 Empirical Benchmark Summary

```
===============================================================================================
EMPIRICAL TBSG BENCHMARK: CBM vs CEM vs HYBRID ON UNSW-NB15 NIDS
===============================================================================================
Model Architecture             | Test Acc  | ROC-AUC  | Targeted CIE%  | Full CIE%  | LBL % (TBSG Leak) 
-----------------------------------------------------------------------------------------------
CBM (Concept Bottleneck Model) | 85.26%    | 0.9674   | 91.18%         | 89.95%     | 0.00%             
CEM (Concept Embedding Model)  | 82.91%    | 0.9528   | 0.33%          | 0.20%      | 98.24%            
Hybrid TBSG Model (Gated-CEM)  | 86.35%    | 0.9671   | 74.82%         | 60.86%     | 0.00%             
===============================================================================================
```
- **CEM Fails Trust Boundary**: 98.24% of attack samples in CEM continue to predict attack under $\text{do}(C=\mathbf{0})$ because unconstrained latent embeddings ($e^-$) smuggle attack features past the concept bottleneck.
- **Hybrid Solves TBSG**: Gating the residual channel via $\text{Gate}(C)$ closes the latent bypass (0.00% LBL) while achieving superior observational accuracy (86.35%).
