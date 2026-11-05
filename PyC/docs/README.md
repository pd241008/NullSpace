# Trust Boundary Semantic Gap (TBSG) Audit & Empirical Benchmark

This folder contains the complete technical audit of [`pyc-team/pytorch_concepts`](https://github.com/pyc-team/pytorch_concepts.git), the theoretical mapping to the **Trust Boundary Semantic Gap (TBSG)** safety framework, and the empirical benchmark on the **UNSW-NB15 NIDS** dataset from `centralized_datasets`.

---

## Directory Contents

| File | Description |
| :--- | :--- |
| **`PYTORCH_CONCEPTS_CODEBASE_AUDIT.md`** | Comprehensive software security & architectural audit of `pytorch_concepts`. Identifies Critical RCE (`eval()`), High-risk insecure deserialization (`weights_only=False`), and packaging bugs. |
| **`TBSG_SAFETY_BOUNDARY_MAPPING.md`** | Theoretical and architectural mapping of multi-stage concept-based models (CBM, CEM, Steerling) to the Trust Boundary Semantic Gap taxonomy. |
| **`EMPIRICAL_NIDS_BENCHMARK_REPORT.md`** | Full empirical results and analysis of CBM vs. CEM vs. Hybrid on UNSW-NB15 NIDS under causal interventions. |
| **`models.py`** | Modular PyTorch implementations of `ConceptBottleneckModel`, `ConceptEmbeddingModel`, and `HybridTBSGModel` (Gated-CEM with a Trust Barrier). |
| **`run_tbsg_benchmark.py`** | Self-contained, executable benchmark script with argument parsing and safe `weights_only=True` dataset loading. |
| **`results/`** | Contains raw benchmark JSON (`tbsg_cbm_cem_hybrid_results.json`) and summary text (`summary_table.txt`). |

---

## Dataset & Safe Serialization

The preprocessed dataset is saved in:
`../processed/nids_unsw_nb15_concepts.pt`

- **Safe Deserialization (`weights_only=True`)**: The dataset was specifically generated using primitive PyTorch tensor dictionaries, allowing safe loading in compliance with PyTorch 2.6+ security requirements:
  ```python
  import torch
  data = torch.load("../processed/nids_unsw_nb15_concepts.pt", weights_only=True)
  ```
- **Insecure Deserialization (`weights_only=False`)**: Legacy methods that unpickle arbitrary Python classes bypass unpickler safety checks and are flagged as high risk.

---

## Reproduction

To execute the benchmark:
```bash
python3 run_tbsg_benchmark.py --epochs 10 --batch-size 256
```

---

## Empirical Benchmark Summary

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

