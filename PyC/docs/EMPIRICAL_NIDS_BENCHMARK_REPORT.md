# Empirical Verification Report: CBM vs. CEM vs. Hybrid on UNSW-NB15 NIDS

**Dataset**: UNSW-NB15 Network Intrusion Detection System (42 features, 2 classes)  
**Location**: `/root/workspace/workspace/03-Code/Projects/Legacy/centralized_datasets`  
**Serialized Package**: `processed/nids_unsw_nb15_concepts.pt`  

---

## 1. Experimental Protocol

- **Dataset**: 40,000 training samples, 15,000 held-out test samples.
- **Concepts (6)**:
  1. `volumetric_activity` (packet/byte load)
  2. `timing_and_jitter` (inter-packet timing)
  3. `tcp_handshake_health` (SYN-ACK / window scaling)
  4. `payload_symmetry` (byte/loss ratios)
  5. `connection_density` (host/port sweeps)
  6. `protocol_disruption` (TTL/state anomalies)
- **Evaluated Models**:
  - `ConceptBottleneckModel` (Pure CBM)
  - `ConceptEmbeddingModel` (CEM with $m=8$ embedding bypass)
  - `HybridTBSGModel` (Gated-CEM with Trust Barrier)
- **Evaluation Modes**:
  1. **Observational Mode**: Standard test inference.
  2. **Targeted Causal Intervention**: Clamping top attack concepts (`volumetric`, `density`, `protocol`) to 0 on attack traffic.
  3. **Full Benign Causal Intervention**: Clamping all concepts to 0 ($\text{do}(C = \mathbf{0})$).

---

## 2. Benchmark Results

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

### Metric Definitions
- **Targeted CIE (%)**: Relative reduction in predicted attack probability under targeted concept nullification.
- **Full CIE (%)**: Relative reduction in predicted attack probability under full benign concept nullification ($\text{do}(C=\mathbf{0})$).
- **Latent Bypass Leakage (LBL %)**: The percentage of confirmed attack flows that **still trigger an attack classification ($P(Y=1) > 0.5$) even when all concepts are forced to 0 (benign)**.

---

## 3. Key Findings

1. **CEM Confirms Massive TBSG Violation (98.24% Leakage)**:
   Even after an operator explicitly intervenes to force all concepts to benign ($\text{do}(C = \mathbf{0})$), **98.24% of attack samples in CEM are still classified as attacks**. The model completely ignores the concept boundary because the negative state embedding $e^-$ carries unmonitored latent representations of the raw attack features.
2. **CBM Guarantees Boundary Integrity at a Cost**:
   CBM exhibits **0.00% Latent Bypass Leakage** and an **89.95% reduction** in attack probability under full intervention. However, its strict bottleneck slightly limits representational expressiveness.
3. **The Gated Hybrid Resolves the Dilemma**:
   The Hybrid TBSG Model achieves:
   - **86.35% Test Accuracy** (highest overall, surpassing CBM and CEM).
   - **0.00% Latent Bypass Leakage** (Trust Barrier closes when $C \to \mathbf{0}$).
   - **74.82% Targeted Causal Intervention Efficacy**.

---

## 4. Deserialization Audit (`weights_only`)

- **Verification with `weights_only=True`**:
  - Preprocessed dataset stored as primitive torch tensors:
    `{"train_X": Tensor, "train_y": Tensor, "train_C": Tensor, ...}`
  - Verified: `torch.load(path, weights_only=True)` loads securely without pickle risk.
- **Legacy `weights_only=False` Risk**:
  - Verified: `weights_only=False` bypasses the safe unpickler and must never be permitted in production pipelines.

