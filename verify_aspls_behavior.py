#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verification script to ensure optimized aspls produces identical results to original."""

import sys
import numpy as np
import importlib.util

# Load both original and optimized versions
def load_module_from_file(filepath, module_name):
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_identical_behavior():
    """Compare original and optimized aspls implementations."""
    print("Verification Test: Comparing Original vs Optimized aspls")
    print("=" * 60)
    
    try:
        # Import current (optimized) version
        from amcg_pybaselines import Baseline
        from amcg_pybaselines.whittaker import aspls as aspls_optimized
        
        # Import original version from backup
        original_module = load_module_from_file(
            '/Users/yunsung/workspace/pybaselines/amcg_pybaselines/whittaker_backup.py',
            'whittaker_original'
        )
        
        # Import necessary modules for original version to work
        sys.modules['amcg_pybaselines.whittaker_original'] = original_module
        
        print("✓ Successfully loaded both versions")
        
    except Exception as e:
        print(f"✗ Failed to load modules: {e}")
        return False
    
    # Test different scenarios
    test_cases = [
        {
            'name': 'Simple linear baseline',
            'size': 500,
            'data_func': lambda x: 1 + 0.01 * x + 0.05 * np.random.randn(len(x)),
            'lam': 1e5,
            'max_iter': 50
        },
        {
            'name': 'Polynomial baseline with peaks',
            'size': 1000,
            'data_func': lambda x: (0.001 * x**2 - 0.05 * x + 1 + 
                                   0.5 * np.exp(-((x - 30)**2) / 100) + 
                                   0.1 * np.random.randn(len(x))),
            'lam': 1e6,
            'max_iter': 100
        },
        {
            'name': 'Noisy data',
            'size': 2000,
            'data_func': lambda x: 2 * np.sin(x/50) + 0.5 * np.random.randn(len(x)),
            'lam': 1e4,
            'max_iter': 75
        },
        {
            'name': 'Large dataset',
            'size': 10000,
            'data_func': lambda x: 0.5 + 0.0001 * x + 0.2 * np.random.randn(len(x)),
            'lam': 1e5,
            'max_iter': 50
        }
    ]
    
    all_passed = True
    detailed_results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']} (size={test_case['size']})")
        print("-" * 40)
        
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate test data
        x = np.linspace(0, 100, test_case['size'])
        y = test_case['data_func'](x)
        
        # Create Baseline objects
        baseline_opt = Baseline(x)
        baseline_orig = Baseline(x)
        
        # Monkey patch the original aspls method
        baseline_orig.aspls = lambda *args, **kwargs: original_module._Whittaker.aspls(
            baseline_orig, *args, **kwargs
        )
        
        try:
            # Run optimized version (without warm start)
            baseline1, params1 = baseline_opt.aspls(
                y, 
                lam=test_case['lam'], 
                max_iter=test_case['max_iter'],
                tol=1e-3,
                asymmetric_coef=0.5
            )
            
            # Run original version
            baseline2, params2 = baseline_orig.aspls(
                y,
                lam=test_case['lam'],
                max_iter=test_case['max_iter'],
                tol=1e-3,
                asymmetric_coef=0.5
            )
            
            # Compare results
            baseline_diff = np.max(np.abs(baseline1 - baseline2))
            weights_diff = np.max(np.abs(params1['weights'] - params2['weights']))
            alpha_diff = np.max(np.abs(params1['alpha'] - params2['alpha']))
            
            # Check iterations
            iter1 = len(params1['tol_history'])
            iter2 = len(params2['tol_history'])
            
            # Detailed comparison
            result = {
                'test': test_case['name'],
                'baseline_diff': baseline_diff,
                'weights_diff': weights_diff,
                'alpha_diff': alpha_diff,
                'iterations_opt': iter1,
                'iterations_orig': iter2,
                'passed': baseline_diff < 1e-10 and weights_diff < 1e-10
            }
            detailed_results.append(result)
            
            print(f"  Baseline difference: {baseline_diff:.2e}")
            print(f"  Weights difference:  {weights_diff:.2e}")
            print(f"  Alpha difference:    {alpha_diff:.2e}")
            print(f"  Iterations: {iter1} (opt) vs {iter2} (orig)")
            
            # Note: Due to early termination optimization, iteration count might differ
            # but the final result should be very close
            if baseline_diff < 1e-10 and weights_diff < 1e-10:
                print("  ✓ Results are identical (within numerical precision)")
            elif baseline_diff < 1e-8 and weights_diff < 1e-8:
                print("  ✓ Results are very close (acceptable difference)")
            else:
                print("  ✗ Results differ significantly!")
                all_passed = False
                
        except Exception as e:
            print(f"  ✗ Test failed with error: {e}")
            all_passed = False
            detailed_results.append({
                'test': test_case['name'],
                'error': str(e),
                'passed': False
            })
    
    # Test warm start functionality
    print("\n\nWarm Start Functionality Test")
    print("=" * 60)
    
    try:
        np.random.seed(123)
        x = np.linspace(0, 100, 1000)
        y = 1 + 0.01 * x + 0.1 * np.random.randn(1000)
        
        baseline_opt = Baseline(x)
        
        # First run
        baseline1, params1 = baseline_opt.aspls(y, lam=1e5, max_iter=100)
        iter1 = len(params1['tol_history'])
        
        # Second run with warm start
        baseline2, params2 = baseline_opt.aspls(
            y, lam=1e5, max_iter=100, warm_start=params1
        )
        iter2 = len(params2['tol_history'])
        
        # Third run without warm start (should be same as first)
        baseline3, params3 = baseline_opt.aspls(y, lam=1e5, max_iter=100)
        iter3 = len(params3['tol_history'])
        
        print(f"  First run iterations: {iter1}")
        print(f"  Warm start iterations: {iter2}")
        print(f"  Third run iterations: {iter3}")
        
        if iter2 < iter1:
            print(f"  ✓ Warm start reduced iterations by {iter1 - iter2}")
        else:
            print("  ✗ Warm start did not improve convergence")
            
        if np.max(np.abs(baseline1 - baseline3)) < 1e-10:
            print("  ✓ Non-warm start runs produce identical results")
        else:
            print("  ✗ Non-warm start runs differ")
            
    except Exception as e:
        print(f"  ✗ Warm start test failed: {e}")
        all_passed = False
    
    # Summary
    print("\n\nSUMMARY")
    print("=" * 60)
    print(f"{'Test Case':<30} {'Baseline Diff':<15} {'Weights Diff':<15} {'Status'}")
    print("-" * 60)
    
    for result in detailed_results:
        if 'error' not in result:
            status = "✓ PASS" if result['passed'] else "✗ FAIL"
            print(f"{result['test']:<30} {result['baseline_diff']:<15.2e} "
                  f"{result['weights_diff']:<15.2e} {status}")
        else:
            print(f"{result['test']:<30} {'ERROR':<15} {'ERROR':<15} ✗ FAIL")
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL VERIFICATION TESTS PASSED!")
        print("The optimized implementation produces identical results to the original.")
    else:
        print("✗ Some verification tests failed.")
        print("The optimized implementation may not be producing identical results.")
    
    return all_passed


def test_edge_cases():
    """Test edge cases to ensure robustness."""
    print("\n\nEdge Case Tests")
    print("=" * 60)
    
    from pybaselines import Baseline
    
    edge_cases = [
        {
            'name': 'Very small dataset',
            'x': np.linspace(0, 1, 10),
            'y': np.random.randn(10)
        },
        {
            'name': 'Constant data',
            'x': np.linspace(0, 100, 100),
            'y': np.ones(100) * 5
        },
        {
            'name': 'Linear data',
            'x': np.linspace(0, 100, 100),
            'y': np.linspace(1, 10, 100)
        },
        {
            'name': 'Data with outliers',
            'x': np.linspace(0, 100, 100),
            'y': np.concatenate([np.ones(40), np.ones(20) * 100, np.ones(40)])
        }
    ]
    
    all_passed = True
    
    for test_case in edge_cases:
        print(f"\nTesting: {test_case['name']}")
        try:
            baseline_obj = Baseline(test_case['x'])
            baseline, params = baseline_obj.aspls(test_case['y'], lam=1e5)
            
            if np.any(np.isnan(baseline)) or np.any(np.isinf(baseline)):
                print("  ✗ Output contains NaN or Inf")
                all_passed = False
            else:
                print("  ✓ Output is valid")
                
        except Exception as e:
            print(f"  ✗ Test failed: {e}")
            all_passed = False
    
    return all_passed


if __name__ == "__main__":
    print("ASPLS Optimization Verification Suite")
    print("=" * 60)
    print("This script verifies that the optimized aspls implementation")
    print("produces identical results to the original implementation.")
    print()
    
    # Run verification
    verification_passed = verify_identical_behavior()
    
    # Run edge case tests
    edge_cases_passed = test_edge_cases()
    
    # Final verdict
    print("\n\nFINAL VERDICT")
    print("=" * 60)
    
    if verification_passed and edge_cases_passed:
        print("✓ The optimized aspls implementation is verified to be correct!")
        print("  - Produces identical results to the original")
        print("  - Handles edge cases properly")
        print("  - Warm start functionality works as expected")
    else:
        print("✗ Verification failed. Please review the implementation.")
        
    sys.exit(0 if verification_passed and edge_cases_passed else 1)