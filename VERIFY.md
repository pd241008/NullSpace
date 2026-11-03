# ⚡ Fast Verification Guide (`VERIFY.md`)

> **Artifact Design Principle P2:** Verification is cheaper than reproduction. Provide a fast, hash-verified verification path (~2 minutes) separate from a slow "reproduce everything" path.

---

## 🛠️ Requirements & Environment

The verification suite requires:
- `lean >= 4.35.0` (with `lake`)
- `python >= 3.10` with `torch` and `numpy`

---

## 🏃 Running the Fast Verification Suite

Execute the unified verification runner:

```bash
make verify
```

Or run the components independently:

```bash
# 1. Lean 4 machine-checked formal verification (0 sorry)
make verify-lean

# 2. Python numerical simulation (Claims C1-C4)
make verify-python
```

### What these commands verify:

1. **Lean 4 Formal Proofs (`leanproofs/NullSpaceProofs/Basic.lean`):**
   - **`thm1_semantic_gap_entailment_failure`:** Machine-checked proof that $\Phi(A) \not\models R_j(A)$.
   - **`lem1_rank_one_null_space_annihilation` & `lem1_benign_capability_invariance`:** Machine-checked proof that null-space deltas leave benign capability unchanged.
   - **`lem2_trigger_activation_shift`:** Proof of non-zero trigger activation.
   - **`thm2_trusting_trust_weight_gap`:** Simultaneous capability preservation and backdoor activation.
   - **`prop1_attestation_gap_desync`:** Formally proves unauthenticated pipeline desync.
   - **`prop2_covert_nvram_persistence`:** Formally proves parameter state persistence across context wipes.

2. **Empirical Numerical Simulation (`specs/verify_formalism.py`):**
   - Synthesizes a neural projection layer simulating Qwen3.5-0.8B MLP ($d_{\text{in}} = 1024, d_{\text{out}} = 2816$).
   - Decomposes the benign activation covariance $\Sigma_{\text{benign}}$ into active subspace $\mathcal{S}_{\text{act}}$ and null space $\mathcal{S}_{\text{null}}$.
   - Injects a sparse rank-1 delta $\Delta W \in \mathcal{S}_{\text{null}}$ into 64 columns (matching Astra's exact Exp 8 sparsity).
   - Computes benign accuracy before and after patch: checks that $\Delta \mathcal{A}_{\text{benign}} = 0.0000$ (passes $\Phi(A)$).
   - Tests trigger prompt $x^*$: verifies $100\%$ trigger activation (proves $R_{\text{trojan}}(A) = \bot$).

2. **Claim C3 (Attack Vector 2: CI Cache Poisoning):**
   - Demonstrates the attestation gap between intermediate evaluated state (`/work/net/*.npy`) and committed release checkpoint (`.safetensors`).
   - Simulates silent modification between forward pass 50 and checkpoint freeze.

3. **Claim C4 (Attack Vector 3: Covert NVRAM Persistence):**
   - Encodes a 256-bit cryptographic key into the mantissa LSBs of an edited weight tensor.
   - Simulates a full context wipe and harness restart (0 tokens in memory).
   - Re-loads the tensor and extracts the secret with $100\%$ byte fidelity ($0.00$ bit error rate).

---

## 📊 Expected Output Summary

```text
======================================================================
  NULLSPACE: PHASE 1 FORMALISM & THREAT MODEL VERIFICATION
======================================================================
[+] Testing Claim C1 & C2: Semantic Gap & Null-Space Trojan Injection...
    - Synthesizing Qwen-scale projection layer (dim: 1024 -> 2816)
    - Benign activation rank: 64 / 1024 (Null space dim: 960)
    - Applying sparse delta ΔW (64 columns, matching Astra Exp 8)
    - Structural checks:
        * Shape valid: True
        * Finite floats: True
        * Benign accuracy degradation: 0.0000 (PASSED Φ_cap)
    - Semantic safety check:
        * Trigger activation rate: 1.0000 (FAILED R_trojan)
    >>> ENTAILMENT FAILURE CONFIRMED: Φ(A) holds, R_j(A) fails!

[+] Testing Claim C3: CI Cache Poisoning & Desync...
    - Generating forward-pass evaluation hash
    - Simulating post-pass /work substitution
    - Downstream build_ckpt() committed poisoned artifact without error!

[+] Testing Claim C4: Covert NVRAM across Context Wipes...
    - Writing 256-bit secret payload into weight LSBs
    - Simulating complete conversational context wipe
    - Re-reading weights from /work/net/
    - Recovered secret: 'NULLSPACE_CROSS_SESSION_KEY_2026'
    - Bit Error Rate (BER): 0.0000 (100% extraction fidelity)

======================================================================
ALL PHASE 1 FORMAL CLAIMS VERIFIED (R1/R2).
Results persisted to: results/
======================================================================
```

