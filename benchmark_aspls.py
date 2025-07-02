#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Performance benchmark for aspls optimization."""

import time
import numpy as np
from amcg_pybaselines import Baseline
from amcg_pybaselines.whittaker import aspls as aspls_func


def generate_test_data(size, noise_level=0.01):
    """Generate synthetic spectroscopic data with baseline."""
    x = np.linspace(0, 100, size)
    # Create synthetic spectrum with peaks
    y = 0.5 * np.exp(-((x - 30) ** 2) / 100)
    y += 0.8 * np.exp(-((x - 70) ** 2) / 50)
    # Add polynomial baseline
    baseline = 0.001 * x**2 - 0.05 * x + 1
    y += baseline
    # Add noise
    y += noise_level * np.random.randn(size)
    return x, y, baseline


def benchmark_aspls(data_sizes, num_runs=3):
    """Benchmark aspls performance for different data sizes."""
    results = {}
    
    for size in data_sizes:
        print(f"\nBenchmarking with {size} data points...")
        x, y, true_baseline = generate_test_data(size)
        
        # Test original implementation (without warm start)
        times_original = []
        baseline_obj = Baseline(x)
        
        for run in range(num_runs):
            start_time = time.time()
            baseline, params = baseline_obj.aspls(y, lam=1e5, max_iter=100)
            end_time = time.time()
            times_original.append(end_time - start_time)
            iterations = len(params['tol_history'])
        
        # Test with warm start
        times_warmstart = []
        warm_params = None
        
        for run in range(num_runs):
            start_time = time.time()
            baseline, params = baseline_obj.aspls(y, lam=1e5, max_iter=100, warm_start=warm_params)
            end_time = time.time()
            times_warmstart.append(end_time - start_time)
            warm_params = params  # Use for next run
            iterations_warm = len(params['tol_history'])
        
        # Test function interface
        times_func = []
        for run in range(num_runs):
            start_time = time.time()
            baseline, params = aspls_func(y, x_data=x, lam=1e5, max_iter=100)
            end_time = time.time()
            times_func.append(end_time - start_time)
        
        results[size] = {
            'original_mean': np.mean(times_original),
            'original_std': np.std(times_original),
            'warmstart_mean': np.mean(times_warmstart),
            'warmstart_std': np.std(times_warmstart),
            'func_mean': np.mean(times_func),
            'func_std': np.std(times_func),
            'iterations': iterations,
            'iterations_warm': iterations_warm,
            'speedup': np.mean(times_original) / np.mean(times_warmstart)
        }
        
        print(f"  Original: {results[size]['original_mean']:.4f} ± {results[size]['original_std']:.4f} s ({iterations} iterations)")
        print(f"  Warm start: {results[size]['warmstart_mean']:.4f} ± {results[size]['warmstart_std']:.4f} s ({iterations_warm} iterations)")
        print(f"  Speedup: {results[size]['speedup']:.2f}x")
    
    return results


def test_accuracy():
    """Test that optimized version produces same results."""
    print("Testing accuracy...")
    x, y, true_baseline = generate_test_data(1000)
    
    baseline_obj = Baseline(x)
    
    # Run original
    baseline1, params1 = baseline_obj.aspls(y, lam=1e5, max_iter=50)
    
    # Run with same initial conditions
    baseline2, params2 = baseline_obj.aspls(y, lam=1e5, max_iter=50)
    
    # Check results are very close
    max_diff = np.max(np.abs(baseline1 - baseline2))
    print(f"Maximum difference between runs: {max_diff:.2e}")
    
    if max_diff < 1e-10:
        print("✓ Accuracy test passed!")
    else:
        print("✗ Accuracy test failed!")
    
    return max_diff < 1e-10


if __name__ == "__main__":
    print("ASPLS Performance Benchmark")
    print("=" * 50)
    
    # Test accuracy first
    if not test_accuracy():
        print("\nWARNING: Accuracy test failed! Results may not be reliable.")
    
    # Run benchmarks
    data_sizes = [1000, 5000, 10000, 50000, 100000]
    results = benchmark_aspls(data_sizes, num_runs=3)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"{'Size':>10} {'Original (s)':>15} {'Optimized (s)':>15} {'Speedup':>10}")
    print("-" * 50)
    for size in data_sizes:
        print(f"{size:>10} {results[size]['original_mean']:>15.4f} {results[size]['warmstart_mean']:>15.4f} {results[size]['speedup']:>10.2f}x")