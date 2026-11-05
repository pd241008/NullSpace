"""
Modular Implementations of CBM, CEM, and Hybrid TBSG Models
for Concept-Based Deep Learning on Tabular / NIDS Telemetry.
"""

import torch
import torch.nn as nn


class ConceptBottleneckModel(nn.Module):
    """
    Pure Concept Bottleneck Model (Koh et al., ICML 2020):
    Input X -> Latent Z -> Concept Probabilities C -> Task Y
    Strict Trust Boundary: ZERO latent representation reaches the task predictor.
    """
    def __init__(self, in_features=42, num_concepts=6, hidden_dim=64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, num_concepts)
        )
        self.predictor = nn.Sequential(
            nn.Linear(num_concepts, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x, intervention_mask=None, intervention_values=None):
        c_logits = self.encoder(x)
        c_probs = torch.sigmoid(c_logits)

        c_effective = c_probs
        if intervention_mask is not None and intervention_values is not None:
            c_effective = c_probs * (1.0 - intervention_mask) + intervention_values * intervention_mask

        y_logit = self.predictor(c_effective).squeeze(-1)
        return y_logit, c_effective


class ConceptEmbeddingModel(nn.Module):
    """
    Concept Embedding Model (Espinosa Zarlenga et al., NeurIPS 2022 / PyC):
    Input X -> (Concepts C, Embeddings E+, E-) -> Mix(C, E) -> Task Y
    Vulnerable to TBSG: High-dimensional embeddings E bypass the concept trust boundary.
    """
    def __init__(self, in_features=42, num_concepts=6, emb_dim=8, hidden_dim=64):
        super().__init__()
        self.num_concepts = num_concepts
        self.emb_dim = emb_dim

        self.backbone = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
        )
        self.concept_head = nn.Linear(hidden_dim, num_concepts)

        # Positive and negative state embeddings per concept
        self.emb_pos = nn.Linear(hidden_dim, num_concepts * emb_dim)
        self.emb_neg = nn.Linear(hidden_dim, num_concepts * emb_dim)

        # Downstream predictor consumes concatenated mixed embeddings
        self.predictor = nn.Sequential(
            nn.Linear(num_concepts * emb_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x, intervention_mask=None, intervention_values=None):
        B = x.shape[0]
        h = self.backbone(x)
        c_logits = self.concept_head(h)
        c_probs = torch.sigmoid(c_logits)

        e_pos = self.emb_pos(h).view(B, self.num_concepts, self.emb_dim)
        e_neg = self.emb_neg(h).view(B, self.num_concepts, self.emb_dim)

        c_effective = c_probs
        if intervention_mask is not None and intervention_values is not None:
            c_effective = c_probs * (1.0 - intervention_mask) + intervention_values * intervention_mask

        # Mix per-concept embeddings: c * e_pos + (1 - c) * e_neg
        c_expanded = c_effective.unsqueeze(-1)
        mixed_emb = c_expanded * e_pos + (1.0 - c_expanded) * e_neg

        flat_emb = mixed_emb.view(B, -1)
        y_logit = self.predictor(flat_emb).squeeze(-1)
        return y_logit, c_effective


class HybridTBSGModel(nn.Module):
    """
    TBSG-Hardened Hybrid Model:
    Direct Concept Path + Bounded Gated Residual Bypass.
    Implements a Trust Barrier:
    y = W_c * C + alpha * Gate(C) * Predictor(E)
    When C is intervened to 0 (benign), Gate(C) closes the bypass channel,
    preventing latent trust smuggling while capturing residual interactions.
    """
    def __init__(self, in_features=42, num_concepts=6, emb_dim=8, hidden_dim=64):
        super().__init__()
        self.num_concepts = num_concepts
        self.emb_dim = emb_dim

        self.backbone = nn.Sequential(
            nn.Linear(in_features, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
        )
        self.concept_head = nn.Linear(hidden_dim, num_concepts)
        self.emb_head = nn.Linear(hidden_dim, num_concepts * emb_dim)

        # Direct concept pathway (pure semantic boundary)
        self.concept_predictor = nn.Sequential(
            nn.Linear(num_concepts, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

        # Residual embedding pathway (bounded by Tanh)
        self.residual_predictor = nn.Sequential(
            nn.Linear(num_concepts * emb_dim, 16),
            nn.Tanh(),
            nn.Linear(16, 1, bias=False)
        )

        # Learnable gating multiplier
        self.alpha = nn.Parameter(torch.tensor(0.5))

    def forward(self, x, intervention_mask=None, intervention_values=None):
        B = x.shape[0]
        h = self.backbone(x)
        c_logits = self.concept_head(h)
        c_probs = torch.sigmoid(c_logits)

        c_effective = c_probs
        if intervention_mask is not None and intervention_values is not None:
            c_effective = c_probs * (1.0 - intervention_mask) + intervention_values * intervention_mask

        # Direct concept prediction
        direct_out = self.concept_predictor(c_effective).squeeze(-1)

        # Trust Barrier Gating:
        # If concepts are intervened to 0 (benign), gate closes to 0
        gate = torch.mean(c_effective, dim=-1) # (B,)
        e = self.emb_head(h)
        residual_out = (self.alpha * gate * self.residual_predictor(e).squeeze(-1))

        y_logit = direct_out + residual_out
        return y_logit, c_effective

