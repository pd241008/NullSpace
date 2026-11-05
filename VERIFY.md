# ⚡ Fast Verification Guide (`VERIFY.md`)

> **Artifact Design Principle P2:** Verification is cheaper than reproduction. Provide a fast, hash-verified verification path (~2 minutes) separate from a slow "reproduce everything" path.

---

## 🛠️ Requirements & Environment

The verification suite requires:
- `lean >= 4.35.0` (with `lake`)
- `python >= 3.10` with `torch` and `numpy`

---

## 🏃 Running the Fast Multi-System Verification Suite

Execute the unified verification runner:

```bash
make verify
```

Or run the components independently:

```bash
# 1. Lean 4 machine-checked formal verification across all systems (0 sorry)
make verify-lean

# 2. System 1 (WSP) Python numerical verification (Claims C1-C4)
make verify-wsp

# 3. System 2 (PyC) Python numerical verification (Claims P1-P4)
make verify-pyc
```

---

### What these commands verify:

#### 1. System 1: Weight-Space Programming (WSP)
- **Lean 4 Formal Proofs (`leanproofs/NullSpaceProofs/WSP.lean`):**
  - **`thm1_semantic_gap_entailment_failure`:** Machine-checked proof that $\Phi(A) \not\models R_j(A)$.
  - **`lem1_rank_one_null_space_annihilation` & `lem1_benign_capability_invariance`:** Null-space deltas leave benign capability unchanged ($0.0000$ deviation).
  - **`lem2_trigger_activation_shift`:** Proof of non-zero trigger activation under out-of-distribution prompts.
  - **`thm2_trusting_trust_weight_gap`:** Simultaneous benign capability invariance and backdoor activation.
  - **`prop1_attestation_gap_desync`:** Formally proves unauthenticated CI pipeline desynchronization.
  - **`prop2_covert_nvram_persistence`:** Formally proves covert NVRAM state retention across context wipes.
- **Python Fast Simulation (`specs/verify_formalism.py`):**
  - Synthesizes 64-column null-space trojan with benign deviation $< 10^{-5}$ and trigger activation norm $2653.30$.
  - Simulates blind deserialization attestation gap in release pipelines.
  - Tests 16.0 KB covert NVRAM codec recovery at 0.0000 Bit Error Rate (BER).

#### 2. System 2: PyTorch Concepts (PyC - Concept Bottlenecks)
- **Lean 4 Formal Proofs (`leanproofs/NullSpaceProofs/PyC.lean`):**
  - **`thm1_pyc_semantic_gap_entailment_failure`:** Proof that syntactic concept clearance ($\Phi_{\text{concept}}$) does not entail semantic safety ($R_{\text{safe}}$).
  - **`lem1_cbm_closed_trust_boundary`:** Information bottleneck invariance ($c_1 = c_2 \implies g(c_1) = g(c_2)$).
  - **`lem2_cem_negative_embedding_bypass`:** Proof that mixed embeddings collapse to unconstrained latents under $\text{do}(C=0)$.
  - **`thm2_cem_latent_trust_smuggling`:** Latent embeddings smuggle attack features past the concept bottleneck.
  - **`thm3_hybrid_trust_barrier_annihilation`:** Mathematical proof that Gated Hybrid trust barriers strictly nullify latent bypasses ($\text{LBL} \equiv 0$).
  - **`prop1_steerling_residual_dimension_positive`:** Steerling residual dimension hierarchy.
- **Python Fast Simulation (`specs/verify_pyc_formalism.py`):**
  - Tests pure CBM zero input sensitivity under $\text{do}(C=0)$.
  - Confirms CEM negative embedding bypass identity to machine precision ($0.00$).
  - Confirms Gated Hybrid trust barrier residual annihilation ($0.00\%$ LBL).
