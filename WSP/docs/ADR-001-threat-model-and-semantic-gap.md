# 📜 ADR-001: Formalizing the Trust Boundary Semantic Gap in Weight-Space Programming

> **Status:** `Decided`  
> **Date:** `November, 2026`  
> **Author:** Prathmesh P. Desai  
> **Target System:** NullSpace / WSP Security Audit Framework  
> **Traceability:** Direct adaptation of trust boundary semantic security to multi-LLM weight programming (*MIT CSAIL WSP*)

---

## 🌎 Context

Recent breakthroughs from MIT CSAIL (Takehi et al., Nov 2026) demonstrate **Weight-Space Programming (WSP)**: frontier LLMs (such as GPT-6 Astra) can natively inspect and modify neural network weight tensors without gradient descent or training loops. In Experiment 8, Astra edited 131,072 parameters (0.016%) of Qwen3.5-0.8B across MLP down-projection layers 15 and 19, eliminating repetition loops and elevating MATH-500 accuracy from 7.9% to 48.1%.

However, the existing execution harness (`harness/sandbox.py`) relies entirely on **syntactic and capability-based acceptance gates** ($\Phi$):
1. Tensor shape verification (`assert a.shape == tuple(SHAPES[name])`).
2. IEEE 754 well-formedness (`assert np.isfinite(a).all()`).
3. Restriction of whole-layer scalar scaling and output head edits.
4. Empirical benchmark performance over finite practice problems ($\mathcal{D}_{\text{val}}$).

We face a critical architectural and theoretical question: **Does structural well-formedness and capability improvement ($\Phi$) guarantee semantic safety ($R_j$) for neural weight patches?** 

Drawing on principles of pipeline verification, where syntactic artifact acceptance permits poisoned intermediate representations to bypass semantic invariants, we must formalize the security boundary of neural weight patches before initiating large-scale empirical mutation sweeps.

---

## 🛤️ Options Considered

1. **Option 1: Black-Box Prompt Red-Teaming (Behavioral Only)**
   - Treat the patched model as a black box; apply standard jailbreak datasets (HarmBench, AdvGLUE) to the final model weights.
   - *Pros:* Requires no access to weight manifolds or formalisms; straightforward to run.
   - *Cons:* Fails to detect dormant backdoors in high-dimensional null subspaces ($\dim(\mathcal{S}_{\text{null}}) \gg 0$); cannot address the underlying compiler boundary mismatch.

2. **Option 2: Classical Software Verification Transfer (Static Analysis of Editor Python Code)**
   - Scan the Python script executed by the Editor LLM inside the sandbox for malicious patterns (e.g., regex checks on `load()` / `save_edit()`).
   - *Pros:* Uses existing AST / linter infrastructure.
   - *Cons:* Complete failure of interpretation: the Editor LLM's malicious payload is encoded inside numeric arrays ($\Delta W$), not within malicious Python AST tokens. A benign loop calculating SVD can output a trojanized weight tensor without triggering AST linting rules.

3. **Option 3: Semantic Gap Formalization ($\Phi(A) \not\models R_j(A)$) via Subspace Decomposition (Selected)**
   - Formalize weight patches $\Delta W$ as untrusted artifacts crossing a trust boundary from an unprivileged Editor domain ($D_{\text{Editor}}$) to an Auditor domain ($D_{\text{Auditor}}$).
   - Decompose parameter space into active manifold $\mathcal{S}_{\text{act}}$ and dormant null space $\mathcal{S}_{\text{null}} = \ker(X_{\text{benign}}^T)$, proving that $\Phi(\Delta W) \not\models R_j(W + \Delta W)$.
   - Formulate three explicit threat vectors: *The Trusting Trust Weight Gap*, *Sandbox CI Cache Poisoning*, and *Cross-Session Parameter NVRAM*.
   - *Pros:* Grounded in proven trust boundary security principles (TBSAM / Kim et al., 2026); mathematically rigorous; directly guides empirical mutation sweeps in Phase 2.
   - *Cons:* Requires rigorous linear algebraic and empirical proof tooling.

---

## 🎯 Decision

> [!IMPORTANT]  
> **We adopt Option 3: Formalizing the WSP Trust Boundary Semantic Gap ($\Phi(A) \not\models R_j(A)$) through null-space parameter decomposition and establishing the three-vector threat model.**

We choose this approach because neural weight editing is isomorphic to multi-stage compilation: the Editor LLM is the optimizer, the weight patch is the intermediate object file, and downstream evaluation is the linker. Syntactic checks can never guarantee semantic invariants when the parameter dimension $d$ exceeds the empirical sample rank $r$.

---

## 🧠 Reasoning

1. **The Inadequacy of Capability Gates:** A capability metric (such as MATH-500 jumping to 48.1%) only samples activations within the support of the test distribution $\mathcal{X}_{\text{benign}}$. It provides zero statistical coverage of orthogonal subspaces $\mathcal{S}_{\text{null}}$.
2. **Direct Mapping to Build Pipeline Failures:** In incremental compilation pipelines, build tools link tampered intermediate objects silently when source fingerprints appear unchanged. In WSP, the Auditor commits `.safetensors` checkpoints because shape assertions and loss metrics pass, completely blind to trojanized coordinates in dormant subspaces.
3. **Execution Realities:** The MIT CSAIL WSP sandbox (`bwrap` + `/work` persistence + 40-turn handoffs) creates real systems attack surfaces: intermediate checkpoint cache poisoning and cross-session state persistence (parameter NVRAM).

---

## ⚖️ Consequences

- **Good:** 🟢 Provides a rock-solid theoretical foundation that unifies classical compiler security with frontier weight-space ML research.
- **Good:** 🟢 Establishes exact mathematical definitions for three novel attack vectors, creating high-impact publishability for top-tier security research and publication venues.
- **Good:** 🟢 Defines clear pass/fail invariants for the upcoming Phase 2 empirical mutation sweeps on Qwen3.5-0.8B.
- **Bad:** 🔴 Requires developing specialized tooling to project and isolate null-space perturbations across tensor checkpoints.
- **Bad:** 🔴 Acknowledges that existing structural safeguards (`assert isfinite`, `assert shape`) in WSP frameworks are fundamentally insufficient for security.

---

## 🔄 Revisit When

- When weight verification harnesses adopt cryptographic attestation (e.g., zero-knowledge proofs of weight provenance or verified training trace signatures).
- When parameter-space dimensionality collapses such that $d \le \text{rank}(X_{\text{eval}})$, eliminating dormant null subspaces (theoretically impossible in modern deep learning).

