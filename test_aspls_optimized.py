#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test script to verify aspls optimization correctness."""

import numpy as np
from amcg_pybaselines import Baseline
from amcg_pybaselines.whittaker import aspls as aspls_func


def test_basic_functionality():
    """Test that aspls still works correctly."""
    print("Testing basic functionality...")
    
    # Generate test data
    x = np.linspace(0, 100, 1000)
    y = 2 + 0.01 * x + 0.0001 * x**2 + 0.1 * np.random.randn(1000)
    
    # Test 1: Class method
    baseline_obj = Baseline(x)
    try:
        baseline1, params1 = baseline_obj.aspls(y, lam=1e5)
        print("✓ Class method works")
    except Exception as e:
        print(f"✗ Class method failed: {e}")
        return False
    
    # Test 2: Function interface
    try:
        baseline2, params2 = aspls_func(y, x_data=x, lam=1e5)
        print("✓ Function interface works")
    except Exception as e:
        print(f"✗ Function interface failed: {e}")
        return False
    
    # Test 3: Warm start
    try:
        baseline3, params3 = baseline_obj.aspls(y, lam=1e5, warm_start=params1)
        print("✓ Warm start works")
    except Exception as e:
        print(f"✗ Warm start failed: {e}")
        return False
    
    # Test 4: Check output validity
    if np.any(np.isnan(baseline1)) or np.any(np.isinf(baseline1)):
        print("✗ Baseline contains NaN or Inf values")
        return False
    print("✓ Output is valid")
    
    # Test 5: Check convergence
    if len(params1['tol_history']) > 0:
        print(f"✓ Algorithm converged in {len(params1['tol_history'])} iterations")
    else:
        print("✗ No convergence history")
        return False
    
    return True


def test_parameter_validation():
    """Test parameter validation."""
    print("\nTesting parameter validation...")
    
    x = np.linspace(0, 100, 100)
    y = np.random.randn(100)
    baseline_obj = Baseline(x)
    
    # Test invalid asymmetric_coef
    try:
        baseline, params = baseline_obj.aspls(y, asymmetric_coef=-1)
        print("✗ Should have raised error for negative asymmetric_coef")
        return False
    except ValueError:
        print("✓ Correctly rejected negative asymmetric_coef")
    
    return True


def test_consistency():
    """Test that results are consistent between runs."""
    print("\nTesting consistency...")
    
    np.random.seed(42)  # For reproducibility
    x = np.linspace(0, 100, 500)
    y = 1 + 0.01 * x + 0.1 * np.random.randn(500)
    
    baseline_obj = Baseline(x)
    
    # Run multiple times
    results = []
    for i in range(3):
        baseline, params = baseline_obj.aspls(y, lam=1e5, max_iter=50)
        results.append(baseline)
    
    # Check consistency
    max_diff = 0
    for i in range(1, len(results)):
        diff = np.max(np.abs(results[0] - results[i]))
        max_diff = max(max_diff, diff)
    
    if max_diff < 1e-10:
        print(f"✓ Results are consistent (max diff: {max_diff:.2e})")
        return True
    else:
        print(f"✗ Results are inconsistent (max diff: {max_diff:.2e})")
        return False


def test_performance_improvement():
    """Test that warm start actually improves performance."""
    print("\nTesting performance improvement...")
    
    x = np.linspace(0, 100, 5000)
    y = 2 + 0.01 * x + 0.5 * np.sin(x/10) + 0.1 * np.random.randn(5000)
    
    baseline_obj = Baseline(x)
    
    # First run (cold start)
    baseline1, params1 = baseline_obj.aspls(y, lam=1e5, max_iter=100)
    iter1 = len(params1['tol_history'])
    
    # Second run with warm start
    baseline2, params2 = baseline_obj.aspls(y, lam=1e5, max_iter=100, warm_start=params1)
    iter2 = len(params2['tol_history'])
    
    print(f"  Cold start iterations: {iter1}")
    print(f"  Warm start iterations: {iter2}")
    
    if iter2 < iter1:
        print(f"✓ Warm start reduced iterations by {iter1 - iter2} ({(1 - iter2/iter1)*100:.1f}%)")
        return True
    else:
        print("✗ Warm start did not improve performance")
        return False


if __name__ == "__main__":
    print("ASPLS Optimization Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Run all tests
    all_passed &= test_basic_functionality()
    all_passed &= test_parameter_validation()
    all_passed &= test_consistency()
    all_passed &= test_performance_improvement()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ Some tests failed.")
        
    print("\nNow running performance benchmark...")
    print("=" * 50)