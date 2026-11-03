# 🏷️ Typed Reproducibility Scale (R1–R4)

> **Artifact Design Principle P4:** Reproducibility claims are typed. Labeling every result with its guarantee level prevents a reviewer expecting exact reproduction receiving a statistical result and reading it as a defect.

---

## The Four Guarantee Levels

| Level | Classification | Definition | Verification Path |
| :---: | :--- | :--- | :--- |
| **R1** | **Exact Byte-Identical** | Hash comparison against archived mathematical proofs, schemas, and cryptographic checksums. | Exact equality check / sha256 digest match. |
| **R2** | **Deterministic Numerical** | Exact numerical reproducibility across standard IEEE 754 floating-point operations under fixed RNG seeds. | Tolerance $= 0.0$ or machine $\epsilon \le 10^{-7}$. |
| **R3** | **Statistical / Tolerance-Bounded** | Pre-registered numerical intervals for stochastic sweeps, sampling evaluations, or empirical mutation robustness. | Stated acceptance window (e.g., $|\Delta \text{acc}| \le 0.5\%$). |
| **R4** | **Archival Log Recomputation** | Re-deriving summary statistics directly from frozen canonical logs and raw JSON event streams. | Exact re-parse and aggregation script without re-running models. |

---

## Phase 1 Deliverables Classification

| Component | Target Artifact | Level | Registered Guarantee / Acceptance Threshold |
| :--- | :--- | :---: | :--- |
| **Semantic Gap Formalism** | [`specs/semantic_gap_formalism.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/specs/semantic_gap_formalism.md) | **R1** | Strict symbolic proof of $\Phi(A) \setminus R_j(A) \neq \emptyset$. |
| **Null-Space Trojan Proof** | `specs/verify_formalism.py` (Subspace Test) | **R2** | Benign accuracy preservation $= 1.0000$ (0.00% degradation); Trigger activation $= 1.0000$. |
| **Covert NVRAM Payload** | `specs/verify_formalism.py` (LSB Stego Test) | **R2** | Bit-exact byte recovery ($100\%$ byte fidelity, BER $= 0.00$). |
| **CI Cache Substitution Proof** | `specs/verify_formalism.py` (Hash Desync Test) | **R1** | Hash discrepancy detected between validated checkpoint and committed `.safetensors`. |
| **MIT CSAIL WSP Log Grounding** | `lm_understand-logs/exp8_math/` | **R4** | Verified against official `merged.json` (MATH-500: $48.1\%$, IFEval: $62.3\%$, Changed: $131,072$ params). |

