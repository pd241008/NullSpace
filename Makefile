# NullSpace: Research & Verification Makefile
# Follows Design-Dungeons ML & Research reproducibility standards

.PHONY: all verify verify-lean verify-python test clean help

all: verify

verify: verify-lean verify-python

verify-lean:
	@echo "=================================================================="
	@echo "  Building and Checking Lean 4 Formal Proofs (0 sorry)..."
	@echo "=================================================================="
	cd leanproofs && lake build
	./leanproofs/.lake/build/bin/nullspace_proofs

verify-python:
	@echo "=================================================================="
	@echo "  Running Fast Python Numerical Verification (Claims C1-C4)..."
	@echo "=================================================================="
	python3 specs/verify_formalism.py

test: verify

clean:
	@echo "Cleaning transient cache and bytecode..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

help:
	@echo "NullSpace Verification Targets:"
	@echo "  make verify   - Run the fast verification script (takes ~2 seconds)"
	@echo "  make clean    - Remove transient caches"

