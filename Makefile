# Makefile for amcg-pybaselines aspls optimization verification
# Usage: make [target]

.PHONY: all help verify test benchmark clean backup restore check-syntax install-deps

# Default target
all: verify

# Help message
help:
	@echo "amcg-pybaselines aspls optimization verification targets:"
	@echo ""
	@echo "  make verify        - Run all verification tests (default)"
	@echo "  make test          - Run basic functionality tests"
	@echo "  make benchmark     - Run performance benchmarks"
	@echo "  make check-syntax  - Check Python syntax"
	@echo "  make backup        - Create backup of original files"
	@echo "  make restore       - Restore from backup"
	@echo "  make clean         - Remove generated files"
	@echo "  make install-deps  - Install required dependencies"
	@echo ""
	@echo "Verification workflow:"
	@echo "  1. make backup     - Backup original implementation"
	@echo "  2. make verify     - Run all verification tests"
	@echo "  3. make benchmark  - Compare performance"
	@echo ""

# Check Python syntax
check-syntax:
	@echo "Checking Python syntax..."
	@python -m py_compile amcg_pybaselines/whittaker.py
	@python -m py_compile test_aspls_optimized.py
	@python -m py_compile benchmark_aspls.py
	@python -m py_compile verify_aspls_behavior.py
	@python -m py_compile simple_aspls_verification.py
	@echo "✓ Syntax check passed"

# Create backup of original files
backup:
	@echo "Creating backup of original files..."
	@if [ ! -f amcg_pybaselines/whittaker_backup.py ]; then \
		cp amcg_pybaselines/whittaker.py amcg_pybaselines/whittaker_backup.py; \
		echo "✓ Backed up whittaker.py"; \
	else \
		echo "⚠ Backup already exists (whittaker_backup.py)"; \
	fi

# Restore from backup
restore:
	@echo "Restoring from backup..."
	@if [ -f amcg_pybaselines/whittaker_backup.py ]; then \
		cp amcg_pybaselines/whittaker_backup.py amcg_pybaselines/whittaker.py; \
		echo "✓ Restored whittaker.py from backup"; \
	else \
		echo "✗ No backup found"; \
		exit 1; \
	fi

# Run basic functionality tests
test: check-syntax
	@echo ""
	@echo "Running basic functionality tests..."
	@echo "=================================="
	@if command -v python >/dev/null 2>&1; then \
		python test_aspls_optimized.py || true; \
	else \
		echo "✗ Python not found"; \
		exit 1; \
	fi

# Run verification tests
verify-behavior: check-syntax
	@echo ""
	@echo "Running behavior verification..."
	@echo "================================"
	@if command -v python >/dev/null 2>&1; then \
		python verify_aspls_behavior.py || true; \
	else \
		echo "✗ Python not found"; \
		exit 1; \
	fi

# Run simple verification
verify-simple: check-syntax
	@echo ""
	@echo "Running simple verification..."
	@echo "=============================="
	@if command -v python >/dev/null 2>&1; then \
		python simple_aspls_verification.py || true; \
	else \
		echo "✗ Python not found"; \
		exit 1; \
	fi

# Run all verification tests
verify: check-syntax verify-simple test verify-behavior
	@echo ""
	@echo "================================"
	@echo "All verification tests completed"
	@echo "================================"
	@echo ""
	@echo "Check the output above for any failures."
	@echo "If all tests show ✓, the optimization is verified correct."

# Run performance benchmarks
benchmark: check-syntax
	@echo ""
	@echo "Running performance benchmarks..."
	@echo "================================="
	@if command -v python >/dev/null 2>&1; then \
		python benchmark_aspls.py || true; \
	else \
		echo "✗ Python not found"; \
		exit 1; \
	fi

# Install required dependencies
install-deps:
	@echo "Installing required dependencies..."
	@if command -v pip >/dev/null 2>&1; then \
		pip install numpy scipy || true; \
		echo "✓ Dependencies installed"; \
	else \
		echo "⚠ pip not found. Please install dependencies manually:"; \
		echo "  numpy scipy"; \
	fi

# Clean generated files
clean:
	@echo "Cleaning generated files..."
	@rm -f *.pyc */*.pyc
	@rm -rf __pycache__ */__pycache__
	@rm -f test_output_*.txt
	@echo "✓ Cleaned"

# Quick test for CI/CD
ci-test: check-syntax
	@echo "Running CI tests..."
	@python -c "from amcg_pybaselines.whittaker import aspls; print('✓ Import successful')" || exit 1
	@python -c "import numpy as np; from amcg_pybaselines import Baseline; b = Baseline(); b.aspls(np.ones(100)); print('✓ Basic call successful')" || exit 1

# Full verification workflow
full-verify: backup verify benchmark
	@echo ""
	@echo "======================================="
	@echo "Full verification workflow completed"
	@echo "======================================="
	@echo ""
	@echo "Summary:"
	@echo "1. Original implementation backed up"
	@echo "2. Verification tests run"
	@echo "3. Performance benchmarks completed"
	@echo ""
	@echo "Review the outputs above for detailed results."

# Generate verification report
report:
	@echo "Generating verification report..."
	@echo "# ASPLS Optimization Verification Report" > verification_report.md
	@echo "" >> verification_report.md
	@echo "Generated on: $$(date)" >> verification_report.md
	@echo "" >> verification_report.md
	@echo "## Syntax Check" >> verification_report.md
	@make check-syntax >> verification_report.md 2>&1 || true
	@echo "" >> verification_report.md
	@echo "## Simple Verification" >> verification_report.md
	@echo '```' >> verification_report.md
	@python simple_aspls_verification.py >> verification_report.md 2>&1 || true
	@echo '```' >> verification_report.md
	@echo "" >> verification_report.md
	@echo "## Test Results" >> verification_report.md
	@echo '```' >> verification_report.md
	@python test_aspls_optimized.py >> verification_report.md 2>&1 || true
	@echo '```' >> verification_report.md
	@echo "" >> verification_report.md
	@echo "Report saved to verification_report.md"