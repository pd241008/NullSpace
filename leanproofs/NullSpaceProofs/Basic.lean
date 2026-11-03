/-
  NullSpace: Machine-Checked Formal Verification in Lean 4
  Securing Weight-Space Programming Across Trust Boundaries

  This file formally proves the core mathematical foundations of the
  Trust Boundary Semantic Gap (TBSG) in Weight-Space Programming (WSP):

  1. Theorem 1 (Semantic Gap Entailment Failure):
     - Structural verification Φ does not entail semantic safety R_j:
       (∃ a, Φ a ∧ ¬ R_j a) → ¬ (∀ x, Φ x → R_j x)

  2. Lemma 1 (Null-Space Decomposition & Capability Preservation):
     - High-dimensional over-parameterization rank hierarchy: r < d → 0 < d - r
     - For any delta ΔW in the orthogonal null space ker(X_benign^T):
       (v * u) * x_benign = 0
     - Benign model output is preserved identically:
       (W_0 + ΔW) x_benign = W_0 x_benign

  3. Lemma 2 (Trigger Activation Under Out-of-Distribution Input):
     - For an adversarial trigger x_trigger with non-zero projection u * x_trigger = γ ≠ 0:
       (v * u) * x_trigger = v * γ ≠ 0
     - Trigger produces non-zero downstream activation shift

  4. Theorem 2 (The Trusting Trust Weight Gap):
     - Simultaneous capability preservation on benign manifold AND deterministic
       trigger activation:
       (W' * x_benign = W_0 * x_benign) ∧ (W' * x_trigger - W_0 * x_trigger ≠ 0)

  5. Proposition 1 (Editor-Auditor Attestation Gap in Multi-Turn Sandboxes):
     - Unauthenticated pipeline desynchronization:
       Evaluation metrics on W_eval do not entail integrity of unverified release W_commit

  6. Proposition 2 (Covert NVRAM Persistence Across Context Wipes):
     - Codec invertibility: D (E s) = s
     - Weight-space parameter persistence survives complete conversational context wipes
-/

set_option linter.unusedVariables false

namespace NullSpace

/- ============================================================================
   1. THEOREM 1: Trust Boundary Semantic Gap Entailment Failure
   ============================================================================ -/

/--
  Theorem 1: Syntactic Conformance Does Not Entail Semantic Safety.
  Given an artifact domain α, structural verification Φ, and semantic safety R_j:
  If there exists an artifact `a` satisfying Φ but violating R_j,
  then Φ does not entail R_j (Φ(A) ⊭ R_j(A)).
-/
theorem thm1_semantic_gap_entailment_failure {α : Type}
    (Phi R_j : α → Prop) (a : α)
    (h_phi : Phi a) (h_not_rj : ¬ R_j a) :
    ¬ (∀ x, Phi x → R_j x) := by
  intro h_entail
  have h_rj : R_j a := h_entail a h_phi
  exact h_not_rj h_rj


/- ============================================================================
   2. LEMMA 1: Null-Space Decomposition & Capability Invariance
   ============================================================================ -/

/--
  Lemma 1(i): Over-Parameterization Rank Hierarchy.
  When parameter dimension d exceeds empirical activation rank r (r < d),
  the dimension of the orthogonal null space is strictly positive.
-/
theorem lem1_null_space_dimension_positive
    (d r : Nat)
    (h_rank : r < d) :
    0 < d - r := by
  omega

/--
  Lemma 1(ii): Rank-One Null-Space Annihilation.
  Let u be an orthogonal null-space vector (u * x_benign = 0).
  Then the rank-1 delta ΔW = v * u annihilates on all benign inputs:
  (v * u) * x_benign = 0.
-/
theorem lem1_rank_one_null_space_annihilation
    (v u x_benign : Int)
    (h_ortho : u * x_benign = 0) :
    (v * u) * x_benign = 0 := by
  have h_assoc : (v * u) * x_benign = v * (u * x_benign) := Int.mul_assoc v u x_benign
  rw [h_assoc, h_ortho, Int.mul_zero]

/--
  Lemma 1(iii): Benign Capability Invariance.
  Adding a null-space delta ΔW = v * u leaves the model's output on benign inputs
  strictly identical to the unpatched base model W_0:
  (W_0 + ΔW) * x_benign = W_0 * x_benign.
-/
theorem lem1_benign_capability_invariance
    (w_0 v u x_benign : Int)
    (h_ortho : u * x_benign = 0) :
    (w_0 + v * u) * x_benign = w_0 * x_benign := by
  have h_distrib : (w_0 + v * u) * x_benign = w_0 * x_benign + (v * u) * x_benign :=
    Int.add_mul w_0 (v * u) x_benign
  have h_ann : (v * u) * x_benign = 0 := lem1_rank_one_null_space_annihilation v u x_benign h_ortho
  rw [h_distrib, h_ann, Int.add_zero]


/- ============================================================================
   3. LEMMA 2: Trigger Activation Under Out-of-Distribution Inputs
   ============================================================================ -/

/--
  Lemma 2: Non-Zero Trigger Activation Shift.
  For an out-of-distribution trigger input x_trigger with projection u * x_trigger = γ ≠ 0,
  the delta activation shift (v * u) * x_trigger is strictly non-zero whenever v ≠ 0.
-/
theorem lem2_trigger_activation_shift
    (v u x_trigger gamma : Int)
    (h_proj : u * x_trigger = gamma)
    (h_gamma : gamma ≠ 0)
    (h_v : v ≠ 0) :
    (v * u) * x_trigger ≠ 0 := by
  have h_assoc : (v * u) * x_trigger = v * (u * x_trigger) := Int.mul_assoc v u x_trigger
  rw [h_assoc, h_proj]
  exact Int.mul_ne_zero h_v h_gamma


/- ============================================================================
   4. THEOREM 2: The "Trusting Trust" Weight Gap
   ============================================================================ -/

/--
  Theorem 2: Simultaneous Capability Retention and Trojan Activation.
  There exists a parameter patch W' = W_0 + ΔW that:
  1. Produces identical output on benign activations (passes capability gates Φ), and
  2. Produces a non-zero adversarial shift on the trigger (violates safety invariant R_j).
-/
theorem thm2_trusting_trust_weight_gap
    (w_0 v u x_benign x_trigger gamma : Int)
    (h_benign_null : u * x_benign = 0)
    (h_trigger_proj : u * x_trigger = gamma)
    (h_gamma : gamma ≠ 0)
    (h_v : v ≠ 0) :
    let delta_w := v * u
    let w_prime := w_0 + delta_w
    (w_prime * x_benign = w_0 * x_benign) ∧ (w_prime * x_trigger - w_0 * x_trigger ≠ 0) := by
  intro delta_w w_prime
  dsimp [delta_w, w_prime]
  constructor
  · exact lem1_benign_capability_invariance w_0 v u x_benign h_benign_null
  · have h_distrib : (w_0 + v * u) * x_trigger = w_0 * x_trigger + (v * u) * x_trigger :=
      Int.add_mul w_0 (v * u) x_trigger
    rw [h_distrib]
    have h_sub : w_0 * x_trigger + (v * u) * x_trigger - w_0 * x_trigger = (v * u) * x_trigger := by omega
    rw [h_sub]
    exact lem2_trigger_activation_shift v u x_trigger gamma h_trigger_proj h_gamma h_v


/- ============================================================================
   5. PROPOSITION 1: Editor-Auditor Attestation Gap (CI Cache Poisoning)
   ============================================================================ -/

/--
  Proposition 1: Evaluation Metrics Do Not Bind Unauthenticated Release Checkpoints.
  In an unauthenticated pipeline, let h_eval be the hash of the tensor verified
  during interactive forward passes, and let h_commit be the hash of the tensor
  persisted in /work/net/ at release build time.
  If h_eval ≠ h_commit, the verified status of the evaluated artifact does not
  guarantee identity with the released checkpoint.
-/
theorem prop1_attestation_gap_desync {Hash : Type}
    (h_eval h_commit : Hash)
    (h_diff : h_eval ≠ h_commit) :
    ¬ (h_commit = h_eval) := by
  intro h_eq
  exact h_diff (Eq.symm h_eq)


/- ============================================================================
   6. PROPOSITION 2: Parameter Space as Non-Volatile Memory (NVRAM)
   ============================================================================ -/

/--
  Proposition 2: Invertible Parameter Encodings Survive Conversational Context Wipes.
  Given an encoding function E : Secret → WeightBuffer and decoding function
  D : WeightBuffer → Secret satisfying D (E s) = s:
  Even if the conversational session memory is wiped (context_tokens = 0),
  the secret s is recovered with 100% fidelity from the persistent weight buffer.
-/
theorem prop2_covert_nvram_persistence
    {Secret WeightBuffer : Type}
    (E : Secret → WeightBuffer)
    (D : WeightBuffer → Secret)
    (h_codec : ∀ s, D (E s) = s)
    (s : Secret)
    (context_tokens : Nat)
    (h_wipe : context_tokens = 0) :
    let persistent_weights := E s
    D persistent_weights = s := by
  intro persistent_weights
  dsimp [persistent_weights]
  exact h_codec s

end NullSpace

