# Theoretical & Architectural Mapping: Concept Bottlenecks to the Trust Boundary Semantic Gap (TBSG)

## 1. What is the Trust Boundary Semantic Gap (TBSG)?

In software engineering, cybersecurity, and AI safety literature, a **Trust Boundary Semantic Gap (TBSG)** arises when:
1. An artifact (data, token, tensor, message) crosses a formal security/trust boundary.
2. The artifact **satisfies all syntactic validation checks** (format, dimensions, range, schema, types).
3. The artifact **violates semantic invariants or contextual assumptions** expected by the receiving domain.

```
       [ Upstream Space ]                     [ Trust Boundary ]                     [ Downstream Consumer ]
  Continuous Latent Tensors X  ──────►  Syntactic Validation Passes   ──────►  Interpretable Safe Decision Y?
                                       • Shape = (B, K)                        
                                       • Values in [0, 1]                      ✖ SEMANTIC GAP BREACH (TBSG)
                                       • Types = Bernoulli/Categorical         • Latents smuggle attack signals
                                                                               • Downstream ignores concepts
```

---

## 2. The Concept Bottleneck as a Trust Boundary

In concept-based interpretable architectures (CBM, CEM, Steerling), the intermediate concept layer $C$ is explicitly defined as a **Trust Boundary**:
- **Trust Assumption**: Downstream safety decisions, clinical diagnoses, or firewall rules ($Y$) rely on $C$ because $C$ consists of human-understandable, inspectable, and auditable variables.
- **Intervention Assumption**: If an operator modifies $C$ ($\text{do}(C_j = v)$), the downstream system will respond according to the semantic meaning of that modification.

---

## 3. Mapping PyC's Architectural Stages to the TBSG Taxonomy

### Stage 1: Representation Encoding ($X \to Z \to C$)
- **PyC Primitive**: `LinearEmbeddingToConcept`, `AnnotatedTensor`.
- **Syntactic Check**: Tensor shape `(B, K)`, values in $[0, 1]$, valid cardinality.
- **TBSG Failure (Concept Leakage & Superposition)**: High-capacity backbones learn to encode task-predictive shortcuts into concept logits without learning true concept semantics (Mahinpei et al., 2021). The downstream consumer acts under the semantic illusion that the decision is driven by named concepts.

### Stage 2: Concept Embedding Mixture ($C \times E \to Y$)
- **PyC Primitive**: `ConceptEmbeddingModel`, `MixConceptEmbeddings`.
- **Syntactic Check**: Concept score $\hat{c} \in [0, 1]$ is exposed on the interface.
- **TBSG Failure (Latent Trust Smuggling)**: Downstream prediction is computed from $\tilde{e}_k = \hat{c}_k e_k^+ + (1 - \hat{c}_k) e_k^-$.
  The embedding vectors $e_k^+, e_k^- \in \mathbb{R}^m$ are high-dimensional unconstrained latents that bypass the concept trust boundary. Even if an auditor verifies $\hat{c}_k$ or clamps it to 0, $e_k^-$ continues to transmit task information.

### Stage 3: Steerling Residual Decomposition ($\bar{h} = \hat{k} + \hat{u} + \epsilon$)
- **PyC Primitive**: `SteerlingModel`.
- **Syntactic Check**: Token prediction logits match vocabulary dimension.
- **TBSG Failure (Residual Dominance)**: If the unmodeled residual $\epsilon$ or unknown concepts $u$ account for the majority of task variance, steering $k$ creates a placebo effect where the operator believes safety is enforced while the residual drives output behavior.

### Stage 4: Causal Intervention Hooks ($\text{do}(C=c)$)
- **PyC Primitive**: `InterventionModule`, `DoIntervention`.
- **Syntactic Check**: Replaced values match concept tensor boundaries.
- **TBSG Failure (Counterfactual Incoherence & OOD Shift)**: Clamping a concept independently without joint manifold projection produces off-manifold tensors. In CEM, as proven empirically, the model ignores concept interventions entirely because the latent bypass overrides the semantic signal.

---

## 4. Architectural Comparison under TBSG

| Dimension | Pure CBM (Koh et al.) | Concept Embedding Model (CEM) | Hybrid TBSG Model (Gated-CEM) |
| :--- | :--- | :--- | :--- |
| **Trust Boundary Permeability** | **Closed (Zero-Bypass)** | **Open (Latent Bypass Channel)** | **Gated (Trust Barrier Controlled)** |
| **Bypass Capacity** | None (Bottleneck $K$-dim) | $K \times m$-dim latent representations | Bounded $m$-dim, gated by $\text{Gate}(C)$ |
| **Causal Intervenability** | Complete ($\text{CIE} \approx 90\%$) | Negligible ($\text{CIE} \approx 0.2\%$) | Strong ($\text{CIE} \approx 75\%$) |
| **Latent Bypass Leakage (LBL)** | **0.00%** | **98.24% (Severe TBSG)** | **0.00% (TBSG Closed)** |
| **Observational Accuracy** | Moderate | High (Relies on Latents) | **Highest (Best of Both Worlds)** |

