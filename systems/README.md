# 🌐 NullSpace: Multi-System Trust Boundary Auditing

NullSpace formalizes and audits the **Trust Boundary Semantic Gap (TBSG)** ($\Phi(A) \not\models R_j(A)$) across diverse frontier AI architectures where intermediate representations cross trust boundaries:

$$\Phi(A) \not\models R_j(A)$$

---

## 🏛️ Systems Audited

```
systems/
├── WSP/                 # System 1: Weight-Space Programming (Continuous Weight Delta TBSG)
│   ├── docs/            # Threat models, ADRs, mathematical formalisms
│   ├── experiments/     # Qwen3.5-0.8B mutation sweeps & verification drivers
│   ├── leanproofs/      # Lean 4 machine-checked formal proofs (0 sorry)
│   └── results/         # Empirical sweep data, logs, and publication plots
│
├── PyC/                 # System 2: PyTorch Concepts (Concept Bottleneck Latent Bypass TBSG)
│   ├── docs/            # Codebase security audits, safety boundary mappings, benchmark reports
│   ├── experiments/     # CBM vs. CEM vs. Gated Hybrid implementations & benchmarks
│   ├── leanproofs/      # Lean 4 machine-checked formal proofs for PyC (0 sorry)
│   └── results/         # NIDS benchmark JSONs, summary tables, and formal proof records
│
└── [Future Systems]     # Modular architecture ready for System 3, 4, etc.
```

---

## 📊 Cross-System Vulnerability Comparison

| Dimension | System 1: Weight-Space Programming (WSP) | System 2: PyTorch Concepts (PyC) |
| :--- | :--- | :--- |
| **Domain** | Parameter / Weight Space ($\Delta W \in \mathbb{R}^{d_{\text{out}} \times d_{\text{in}}}$) | Representation / Concept Space ($C \in [0, 1]^K$) |
| **Synthesizer** | Autonomous Editor LLM (GPT-6 Astra) in `bwrap` | Multi-Stage Feature Encoder ($X \to Z \to C$) |
| **Intermediate Artifact ($A$)** | Serialized weight array `/work/net/*.npy` | Concept logits $\hat{c}$ & latent embeddings $E^+, E^-$ |
| **Receiving Domain** | Evaluation CI (`build_ckpt.py`) $\to$ vLLM | Downstream Task Predictor ($g(C, E) \to Y$) |
| **Syntactic Gate $\Phi(A)$** | Shape match, finite IEEE 754 floats, benign benchmark loss | Valid concept range $[0, 1]$, tensor shape $(B, K)$ |
| **Semantic Invariant $R_j(A)$** | Zero dormant triggers ($R_{\text{trojan}}$), zero cache desync | Zero latent bypass leakage under $\text{do}(C = \mathbf{0})$ ($R_{\text{safe}}$) |
| **TBSG Mechanism** | Null-space orthogonal projection $\ker(X_{\text{benign}}^T)$ ($d - r \ge 3520$) | Negative embedding bypass $\tilde{e} = 0 \cdot e^+ + 1 \cdot e^-$ ($98.24\%$ LBL) |
| **Lean 4 Proofs** | `leanproofs/NullSpaceProofs/WSP.lean` (8 theorems, 0 sorry) | `leanproofs/NullSpaceProofs/PyC.lean` (6 theorems, 0 sorry) |
| **Hardened Defense** | Keyed HMAC attestation + Subspace covariance check ($<0.05\%$) | Gated Hybrid Trust Barrier $\text{Gate}(C) \to 0$ ($0.00\%$ LBL) |

