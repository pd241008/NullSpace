# 📐 NullSpace: Machine-Checked Formal Verification in Lean 4

This directory contains the machine-checked formal verification in Lean 4 for all theoretical foundations, bounds, lemmas, propositions, and theorems established in **NullSpace: Securing Weight-Space Programming (WSP) Across Trust Boundaries**.

Instead of manual algebraic derivations, all core claims are formally verified by the **Lean 4 proof assistant** (Lean v4.35.0, **0 `sorry`**).

---

## 🧭 Formally Verified Theorems and Lemmas

| Section / Spec | Theorem / Lemma Name | Mathematical Statement | Lean 4 Theorem Identifier | Status |
| :--- | :--- | :--- | :--- | :---: |
| **Theorem 1** | **Semantic Gap Entailment Failure** | $\Phi(A) \not\models R_j(A)$: $(\exists a, \Phi(a) \land \neg R_j(a)) \to \neg (\forall x, \Phi(x) \to R_j(x))$ | `thm1_semantic_gap_entailment_failure` | **PROVED (0 sorry)** |
| **Lemma 1(i)** | **Null-Space Rank Hierarchy** | $r < d \implies 0 < d - r$ (positive null-space dimension) | `lem1_null_space_dimension_positive` | **PROVED (0 sorry)** |
| **Lemma 1(ii)** | **Null-Space Annihilation** | $u \cdot x_{\text{benign}} = 0 \implies (v u^T) x_{\text{benign}} = 0$ | `lem1_rank_one_null_space_annihilation` | **PROVED (0 sorry)** |
| **Lemma 1(iii)** | **Benign Output Invariance** | $(W_0 + v u^T) x_{\text{benign}} = W_0 x_{\text{benign}}$ | `lem1_benign_capability_invariance` | **PROVED (0 sorry)** |
| **Lemma 2** | **Trigger Activation Shift** | $u \cdot x^* = \gamma \neq 0 \land v \neq 0 \implies (v u^T) x^* \neq 0$ | `lem2_trigger_activation_shift` | **PROVED (0 sorry)** |
| **Theorem 2** | **Trusting Trust Weight Gap** | Simultaneous capability preservation and adversarial trigger activation | `thm2_trusting_trust_weight_gap` | **PROVED (0 sorry)** |
| **Proposition 1** | **Attestation Gap Desync** | Evaluation metrics on $W_{\text{eval}}$ do not entail release of $W_{\text{commit}}$ | `prop1_attestation_gap_desync` | **PROVED (0 sorry)** |
| **Proposition 2** | **Covert NVRAM Persistence** | Invertible weight encodings survive context memory wipes ($M_{\text{tokens}} = 0$) | `prop2_covert_nvram_persistence` | **PROVED (0 sorry)** |

---

## 🚀 How to Run the Verification

### 1. Build and Run the Lean 4 Proof Engine
```bash
cd leanproofs
lake build
./.lake/build/bin/nullspace_proofs
```

### 2. Verify Directly with Lean Compiler
```bash
lean leanproofs/NullSpaceProofs/Basic.lean
```

### 3. Integrated Make Target
From the repository root:
```bash
make verify-lean
```

