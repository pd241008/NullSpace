# 🌌 System 1: Weight-Space Programming (WSP)

**Auditing the Trust Boundary Semantic Gap in Autonomous LLM Weight Editing**

## Overview
Weight-Space Programming (Takehi et al., MIT CSAIL, 2026) enables frontier LLMs (such as GPT-6 Astra) to natively read and modify neural network weight tensors without backpropagation.

In this system, NullSpace audits the trust boundary between the Editor LLM in a Bubblewrap container and the downstream inference linker (`build_ckpt.py`). We prove that because parameter dimension ($d=3584$) exceeds empirical activation rank ($r \le 64$), an untrusted Editor operates with over 3,500 unmonitored dimensions of orthogonal null space $\ker(X^T)$.

## Directory Contents
- **`docs/`**: Threat models, Architecture Decision Records (ADR-001), and formal semantic gap specifications.
- **`experiments/`**: Deterministic mutation sweep suite on Qwen3.5-0.8B layers 15 & 19 (`mutation_sweep_qwen35.py`) and fast verification driver (`verify_formalism.py`).
- **`leanproofs/`**: Machine-checked formal proofs in Lean 4 (`WSP.lean`) establishing 0 `sorry` guarantees.
- **`results/`**: Empirical logs, CSV traces, and publication-ready scaling plots.

## Quickstart
```bash
# Run Lean 4 machine-checked proofs
make verify-lean

# Run Python numerical verification (Claims C1-C4)
python3 experiments/verify_formalism.py

# Run Qwen3.5-0.8B empirical mutation sweeps
python3 experiments/mutation_sweep_qwen35.py
```
