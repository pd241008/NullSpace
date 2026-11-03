# 🧭 Reviewer Guide: NullSpace Verification Pathways

> **Artifact Design Principle P6:** Artifacts accommodate different time budgets. A 15-minute sanity check and a 2-hour full inspection are both legitimate; support both explicitly.

---

## ⏱️ Choose Your Verification Budget

| Pathway | Time Budget | Target Objective | Core Artifacts to Inspect |
| :---: | :---: | :--- | :--- |
| **Track A** | **15 Minutes** | High-level conceptual check: Verify the Trust Boundary Semantic Gap formulation and Mermaid architecture diagram. | 1. [`README.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/README.md)<br/>2. [`CLAIM_MAP.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/CLAIM_MAP.md)<br/>3. [`docs/adrs/ADR-001-threat-model-and-semantic-gap.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/docs/adrs/ADR-001-threat-model-and-semantic-gap.md) |
| **Track B** | **30 Minutes** | Rigorous formal & threat model audit: Inspect the mathematical null-space proof and the three attack vector specifications. | 1. [`specs/semantic_gap_formalism.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/specs/semantic_gap_formalism.md)<br/>2. [`specs/threat_model.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/specs/threat_model.md)<br/>3. Execute `python3 specs/verify_formalism.py` |
| **Track C** | **2 Hours** | End-to-end empirical & architectural audit: Verify numerical proofs against MIT CSAIL WSP experiment logs and examine the Phase 2 mutation sweep harness plan. | 1. [`VERIFY.md`](file:///root/workspace/workspace/03-Code/Projects/Legacy/NullSpace/VERIFY.md)<br/>2. Cross-reference `results/` against `/tmp/lm_understand-logs/exp8_math/`<br/>3. Review `research_plan.md` execution timeline |

---

## 🚀 Quick Commands for Reviewers

```bash
# 1. Run the fast verification script (takes ~2 seconds, tests Claims C1-C4)
python3 specs/verify_formalism.py

# 2. Check the structured results generated in results/
cat results/c1_semantic_gap.json
cat results/c2_trojan_gap.json
cat results/c4_covert_nvram.json
```

