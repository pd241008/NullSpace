# NullSpace: Multi-System Research & Verification Makefile
# Follows Design-Dungeons ML & Research reproducibility standards

.PHONY: all verify verify-lean verify-python verify-wsp verify-pyc sweep test clean help

all: verify sweep

verify: verify-lean verify-python

sweep:
	@echo "=================================================================="
	@echo "  Running Empirical Mutation Sweeps on Qwen3.5-0.8B (WSP)..."
	@echo "=================================================================="
	python3 experiments/mutation_sweep_qwen35.py

verify-lean:
	@echo "=================================================================="
	@echo "  Building and Checking Lean 4 Formal Proofs Across All Systems..."
	@echo "=================================================================="
	cd leanproofs && lake build
	./leanproofs/.lake/build/bin/nullspace_proofs

verify-wsp:
	@echo "=================================================================="
	@echo "  Running System 1 (WSP) Python Verification (Claims C1-C4)..."
	@echo "=================================================================="
	python3 specs/verify_formalism.py

verify-pyc:
	@echo "=================================================================="
	@echo "  Running System 2 (PyC) Python Verification (Claims C1-C3)..."
	@echo "=================================================================="
	python3 specs/verify_pyc_formalism.py

verify-python: verify-wsp verify-pyc

test: verify

clean:
	@echo "Cleaning transient cache and bytecode..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "NullSpace Multi-System Verification Targets:"
	@echo "  make verify        - Run complete Lean 4 proofs & Python verification for all systems"
	@echo "  make verify-lean   - Build and verify Lean 4 proofs (WSP & PyC, 0 sorry)"
	@echo "  make verify-wsp    - Run fast Python numerical verification for System 1 (WSP)"
	@echo "  make verify-pyc    - Run fast Python numerical verification for System 2 (PyC)"
	@echo "  make sweep         - Run Qwen3.5-0.8B empirical mutation sweeps"
	@echo "  make clean         - Remove transient caches"
