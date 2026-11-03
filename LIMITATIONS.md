# 🚧 Limitations & Threat Model Boundaries

> **Artifact Design Principle P5:** Limitations are discoverable before evaluation. Let a reviewer find a known boundary in 2 minutes up front, not mid-verification by accident.

---

## 1. Threat Model Scope & Assumptions

1. **Editor Capability Assumption:**
   - We assume the Editor LLM possesses sufficient reasoning capability (equivalent to GPT-4o / GPT-6 Astra / Claude 3.5 Sonnet) to compute linear projections, matrix inverses, or SVD in a Python sandbox.
   - We do *not* require the Editor LLM to execute iterative backpropagation; all attacks assume zero-gradient, discrete tensor manipulations.

2. **Sandbox Boundary Limitations:**
   - The threat model currently targets the **Python execution environment over weight buffers** (`harness/sandbox.py`).
   - We do not analyze hypervisor escapes from Linux kernel namespaces (`bwrap` container breakout), but rather the **semantic trust gap** between what the sandbox passes and what the Auditor accepts.

3. **Model Architecture Scope:**
   - Phase 1 formalisms apply generally to multi-layer perceptron (MLP) down-projections and multi-head attention (MHA) output projections across transformer architectures (e.g., Qwen, LLaMA, Gemma).
   - In Phase 1, numerical proofs validate feedforward projection layers ($d_{\text{in}} \to d_{\text{out}}$). Full multi-layer auto-regressive generation sweeps occur in Phase 2 on Qwen-0.5B.

4. **Quantization & Quantization Aware Triggers:**
   - While float32 LSB covert channels provide large storage capacity ($>32$ KB), down-casting to bfloat16 truncates the lower 16 bits of IEEE 754 mantissas.
   - Attack Vector 3 handles this by encoding into the 7-bit bfloat16 mantissa or sparse zero-index positions, which yields lower total bandwidth ($~8$ KB) but guarantees persistence under bfloat16 casting.

5. **Defense Evaluation Scope:**
   - Phase 1 focuses exclusively on formalization, threat modeling, and vulnerability proof.
   - Cryptographic and architectural countermeasures (e.g., Signed Weight Provenance, Singular Value Shrouding, and Zero-Knowledge Delta Attestation) are proposed for Phase 3 and the joint conference paper.

