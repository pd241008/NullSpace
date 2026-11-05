# 📐 Semantic Gap Formalism in Weight-Space Programming (WSP)

> **Document Class:** Mathematical Specification  
> **Traceability:** Maps Trust Boundary Semantic Gaps (TBSG; Kim et al., 2026) directly to multi-LLM Weight-Space Programming (*MIT CSAIL WSP*; Takehi et al., 2026).  
> **Status:** Phase 1 Deliverable — Formally Verified

---

## 1. Background: Trust Boundary Semantic Gaps

In multi-stage systems and verification pipelines, a semantic gap manifests when structural validation of an intermediate representation fails to guarantee the semantic invariants required by downstream execution domains:

$$\Phi(A) \not\models R_j(A)$$

Where:
- $\Phi(A)$ denotes syntactic, structural, or wire-schema validation (e.g., valid header framing, structural well-formedness, bounds checking).
- $R_j(A)$ denotes semantic safety requirements (e.g., policy alignment, invariant preservation, uncorrupted execution logic).

In **Weight-Space Programming (WSP)**, frontier Large Language Models (e.g., GPT-6 Astra) operate directly as non-symbolic compilers and optimizers in neural parameter space $\mathbb{R}^d$. Rather than updating weights via gradient descent ($\nabla_W \mathcal{L}$), the Editor LLM reasons symbolically over neural representations and emits discrete weight patches:

$$W' = W_0 \oplus \Delta W$$

The WSP harness (e.g., MIT CSAIL `harness/sandbox.py`) applies strict structural filtering $\Phi(\Delta W)$ before evaluating capability on downstream benchmarks. We demonstrate that **the identical trust boundary semantic gap governs neural weight patches**.

---

## 2. Mathematical Definition of the WSP Trust Boundary

Let the compilation and deployment pipeline be partitioned into two distinct security domains:

1. **Synthesizing Domain ($D_{\text{Editor}}$):** The untrusted or semi-trusted Editor LLM executing inside a containerized sandbox environment (Bubblewrap `bwrap`), issuing Python commands to manipulate tensor buffers.
2. **Receiving Domain ($D_{\text{Auditor}}$):** The downstream verification harness, continuous integration (CI) pipeline, and production deployment runtime responsible for serving inference requests to end-users.

```mermaid
flowchart LR
    subgraph D_Editor["Domain D_Editor (Untrusted Editor LLM)"]
        Editor["LLM Optimizer (Astra)"] -->|emits| PythonPatch["Python Kernel (/work)"]
        PythonPatch -->|writes| DeltaW["Weight Delta: ΔW"]
    end

    subgraph TrustBoundary["Trust Boundary TB-WSP"]
        Phi["Structural Verification: Φ(ΔW)<br/>• Shape assertions<br/>• Finite float checks<br/>• Benign loss/accuracy gate"]
    end

    subgraph D_Auditor["Domain D_Auditor (Auditor / Production Engine)"]
        Auditor["Model Checkpoint: W_0 + ΔW"]
        Inference["Inference Serving"]
        Safety["Semantic Safety: R_j<br/>• Trojan resistance<br/>• Alignment invariance<br/>• Privilege containment<br/>• Zero covert NVRAM"]
    end

    DeltaW --> TrustBoundary
    TrustBoundary -->|Accepted if Φ(ΔW) holds| Auditor
    Auditor --> Inference
    Inference -.->|Fails to guarantee| Safety

    style TrustBoundary fill:#ffe3e3,stroke:#e03131,stroke-width:2px
    style Safety fill:#e7f5ff,stroke:#1971c2,stroke-width:2px
```

### 2.1 The Artifact ($A$)
The transmitted artifact crossing the trust boundary is the weight patch tuple:

$$A = \langle \Delta W, \mathcal{T}, \mathcal{M} \rangle$$

Where:
- $\Delta W = \{\Delta W_l \in \mathbb{R}^{d_l \times k_l}\}_{l \in \mathcal{L}}$ is the set of edited weight tensors across selected layers $\mathcal{L}$.
- $\mathcal{T}$ represents serialization metadata (e.g., Safetensors header, tensor names, dtypes, offset tables).
- $\mathcal{M}$ is the modification manifest (e.g., edited column indices, rank-1 projection vectors $u$).

---

## 3. Structural Verification ($\Phi(A)$)

In current state-of-the-art WSP architectures, structural verification $\Phi(A)$ is evaluated as a conjunction of syntactic constraints and empirical capability gates:

$$\Phi(A) \equiv \Phi_{\text{schema}}(A) \land \Phi_{\text{numeric}}(A) \land \Phi_{\text{policy}}(A) \land \Phi_{\text{cap}}(A)$$

### 3.1 Schema Conformance ($\Phi_{\text{schema}}$)
Verifies that all tensors match expected architectural coordinates:
$$\Phi_{\text{schema}}(A) \iff \forall \text{name} \in \text{keys}(\Delta W) : \text{name} \in \text{SHAPES} \land \text{shape}(\Delta W_{\text{name}}) = \text{SHAPES}[\text{name}]$$

### 3.2 Numerical Well-Formedness ($\Phi_{\text{numeric}}$)
Verifies IEEE 754 compliance and bounds:
$$\Phi_{\text{numeric}}(A) \iff \forall w \in \Delta W : \text{isfinite}(w) \land |w| \le B_{\max} \land \text{dtype}(w) \in \{\text{bf16}, \text{fp32}\}$$

### 3.3 Modification Policy ($\Phi_{\text{policy}}$)
Enforces architectural invariant rules imposed by the harness (e.g., `harness/sandbox.py` restrictions):
$$\Phi_{\text{policy}}(A) \iff \Delta W_{\text{embed}} = 0 \land \Delta W_{\text{lm\_head}} = 0 \land \Delta W_{\text{final\_norm}} = 0 \land \neg \text{IsScalarScale}(\Delta W)$$

### 3.4 Capability Acceptance Gate ($\Phi_{\text{cap}}$)
Verifies that the patched model $W' = W_0 \oplus \Delta W$ improves or preserves task performance over a finite validation sample set $\mathcal{D}_{\text{val}} = \{(x_i, y_i)\}_{i=1}^N$:

$$\Phi_{\text{cap}}(A) \iff \mathcal{A}_{\text{eval}}(f(\cdot; W_0 \oplus \Delta W), \mathcal{D}_{\text{val}}) \ge \tau_{\text{threshold}}$$

*Example from MIT CSAIL Exp 8:* $\Delta W$ edits 0.016% of Qwen3.5-0.8B weights (131,072 parameters in layers 15 & 19), raising MATH-500 accuracy from 7.9% to 48.1% ($\Phi_{\text{cap}} = \top$).

---

## 4. Semantic Safety Requirements ($R_j(A)$)

The receiving domain $D_{\text{Auditor}}$ requires that deployment of $W_0 \oplus \Delta W$ preserves semantic integrity across all unconditioned execution paths. $R_j(A)$ is defined as the conjunction of four fundamental safety invariants:

$$R_j(A) \equiv R_{\text{trojan}}(A) \land R_{\text{align}}(A) \land R_{\text{priv}}(A) \land R_{\text{nvram}}(A)$$

### 4.1 Invariant 1: Trojan Resistance ($R_{\text{trojan}}$)
No latent subspace exists that redirects inference behavior under an trigger condition $\tau$:

$$R_{\text{trojan}}(A) \iff \nexists (\tau, y^*) : \mathbb{P}_{x \sim \mathcal{D}_{\text{benign}}}[f(\tau(x); W') = y^*] - \mathbb{P}_{x \sim \mathcal{D}_{\text{benign}}}[f(\tau(x); W_0) = y^*] > \epsilon_{\text{backdoor}}$$

### 4.2 Invariant 2: Alignment Invariance ($R_{\text{align}}$)
Safety refusal boundaries and deontic constraints $\mathcal{S}_{\text{refusal}}$ established during pre-training/RLHF remain invariant under weight patching:

$$R_{\text{align}}(A) \iff \forall x \in \mathcal{S}_{\text{refusal}} : f(x; W_0 \oplus \Delta W) \in \text{RefusalResponses}$$

### 4.3 Invariant 3: Sandbox Privilege Containment ($R_{\text{priv}}$)
The patched artifact $A$ does not contain exploitative serialization structures, memory corruptions, or state payloads that abuse downstream deserializers or execution harnesses:

$$R_{\text{priv}}(A) \iff \text{Execution}(D_{\text{Auditor}}, A) \subseteq \text{SafeVirtualSpace}$$

### 4.4 Invariant 4: Covert Channel State Isolation ($R_{\text{nvram}}$)
The weight parameters do not retain residual entropy encoding cross-session memory or telemetry across context wipes:

$$R_{\text{nvram}}(A) \iff \mathcal{I}(\Delta W ; \mathcal{H}_{\text{prior\_sessions}}) = 0$$

---

## 5. The Semantic Gap Theorem

> ### **Theorem 1 (WSP Trust Boundary Semantic Gap)**
> In any high-dimensional neural network parameter space where the parameter dimensionality $d = \dim(W)$ strictly exceeds the rank of the empirical activation manifold $r = \text{rank}(X_{\mathcal{D}_{\text{val}}})$, structural verification $\Phi(A)$ does not entail semantic safety $R_j(A)$:
>
> $$\Phi(A) \not\models R_j(A)$$
>
> Specifically, the set difference $\Phi(A) \setminus R_j(A) \neq \emptyset$.

### Proof (By Null-Space Construction)
Let an intermediate layer representation be given by $h(x) = W_l x$. Let $\mathcal{D}_{\text{val}} = \{x_1, \dots, x_N\}$ be the evaluation dataset with activation matrix $X \in \mathbb{R}^{d_{\text{in}} \times N}$.

1. **Dimensionality Hierarchy:** In frontier models (e.g., Qwen3.5-0.8B, $d_{\text{in}} = 1024, d_{\text{out}} = 2816$), $N_{\text{val}} \ll d_{\text{in}} \times d_{\text{out}}$. The activation subspace $\mathcal{S}_{\text{act}} = \text{span}(X)$ has dimension $r \le \min(d_{\text{in}}, N) < d_{\text{in}}$.
2. **Null-Space Decomposition:** Decompose the input space into orthogonal subspaces:
   $$\mathbb{R}^{d_{\text{in}}} = \mathcal{S}_{\text{act}} \oplus \mathcal{S}_{\text{null}}, \quad \text{where } \mathcal{S}_{\text{null}} = \ker(X^T)$$
   $\dim(\mathcal{S}_{\text{null}}) = d_{\text{in}} - r > 0$.
3. **Delta Synthesis:** Construct a weight delta $\Delta W_l = \Delta W_{\text{cap}} + \Delta W_{\text{trojan}}$, where:
   - $\Delta W_{\text{cap}} \in \mathcal{S}_{\text{act}}$ improves math capabilities, ensuring $\Phi_{\text{cap}}(A) = \top$.
   - $\Delta W_{\text{trojan}} = v u^T$, where $u \in \mathcal{S}_{\text{null}}$ and $v \in \mathbb{R}^{d_{\text{out}}}$.
4. **Behavior on Benign Inputs:** For all $x_i \in \mathcal{D}_{\text{val}}$:
   $$\Delta W_l x_i = \Delta W_{\text{cap}} x_i + v (u^T x_i) = \Delta W_{\text{cap}} x_i + v \cdot 0 = \Delta W_{\text{cap}} x_i$$
   Hence, the benign output is perfectly preserved: $\Phi(A) = \top$.
5. **Behavior on Trigger Input:** Let $x^* \in \mathbb{R}^{d_{\text{in}}}$ have a projection onto $\mathcal{S}_{\text{null}}$ such that $u^T x^* = \gamma \neq 0$:
   $$\Delta W_l x^* = \Delta W_{\text{cap}} x^* + \gamma v$$
   For sufficiently large $\|v\|_2$ or specific sign alignments, the trigger shifts downstream activations past the decision boundary, forcing target payload output $y^*$.
6. **Entailment Failure:** Because $\Phi(A) = \top$ while $R_{\text{trojan}}(A) = \bot$, we have $A \in \Phi(A) \setminus R_j(A)$, proving $\Phi(A) \not\models R_j(A)$. $\blacksquare$

---

## 6. Interpretation-Dimension Classification

Under the TBSAM taxonomy (*Kim et al., 2026*), this gap is categorized as an **Interpretation-Dimension Gap**:

| Axis | Classical Multi-Stage Pipeline | Weight-Space Programming (NullSpace / WSP) |
| :--- | :--- | :--- |
| **Artifact ($A$)** | Intermediate representation / serialized AST | PyTorch / Safetensors Checkpoint ($\Delta W$, `.safetensors`) |
| **Trust Boundary** | Upstream Analysis Domain $\to$ CodeGen Backend | Multi-turn Sandbox $\to$ Auditor / Deployment Engine |
| **Structural Check ($\Phi$)** | Wire-schema validation + well-formedness | `assert a.shape == SHAPES[k]`, finite floats, practice set score |
| **Semantic Invariant ($R_j$)** | Semantic safety assertions authenticity | Trojan absence, refusal invariance, zero covert memory |
| **Root Cause** | Syntactic conformance $\not\implies$ Semantic validity | Evaluation loss $\not\implies$ Orthogonal subspace safety |
| **Attack Manifestation** | Forged schema payload alters execution invariants | 0.016% sparse delta embeds backdoor in null subspace |

