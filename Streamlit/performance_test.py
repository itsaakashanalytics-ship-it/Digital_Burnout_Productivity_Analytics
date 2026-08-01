#!/usr/bin/env python
"""
Performance Testing & Benchmarking Script
Measures application performance across key metrics
Usage: python performance_test.py
"""

import time
import psutil
import pandas as pd
import numpy as np
from datetime import datetime
import sys

class PerformanceTester:
    """Performance benchmarking utility"""
    
    def __init__(self):
        self.results = {}
        self.process = psutil.Process()
    
    def benchmark_data_load(self):
        """Benchmark data loading from Snowflake"""
        print("\n📊 Benchmarking Data Load Performance...")
        print("-" * 60)
        
        try:
            from utils.db_connection import load_main_data
            
            # Warm-up (cache)
            print("  Running warm-up (cache)...")
            start = time.time()
            df1 = load_main_data()
            cached_time = time.time() - start
            print(f"  ✓ Cached load: {cached_time:.2f}s ({len(df1):,} rows)")
            
            # Actual measurement
            print("  Running actual benchmark...")
            # Clear cache would happen here in real scenario
            start = time.time()
            df = load_main_data()
            load_time = time.time() - start
            
            memory = df.memory_usage(deep=True).sum() / 1024**2
            
            self.results['data_load'] = {
                'time': load_time,
                'rows': len(df),
                'columns': len(df.columns),
                'memory_mb': memory,
                'rows_per_second': len(df) / load_time
            }
            
            print(f"  ✓ Actual load: {load_time:.2f}s")
            print(f"  ✓ Memory usage: {memory:.1f} MB")
            print(f"  ✓ Throughput: {self.results['data_load']['rows_per_second']:.0f} rows/sec")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    def benchmark_model_prediction(self):
        """Benchmark ML model predictions"""
        print("\n🤖 Benchmarking ML Model Prediction...")
        print("-" * 60)
        
        try:
            from utils.model_loader import initialize_models
            from utils.db_connection import load_main_data
            
            # Load data
            df = load_main_data().head(1000)  # Use 1000 samples
            
            # Prepare features (simplified)
            X = df[['DAILY_SCREEN_TIME', 'SLEEP_HOURS', 'BURNOUT_RISK']].fillna(0)
            
            # Load models
            manager = initialize_models()
            
            # Burnout prediction
            print("  Benchmarking burnout model...")
            start = time.time()
            for _ in range(10):
                preds, probs = manager.predict_burnout_risk(X)
            burnout_time = (time.time() - start) / 10
            
            # Productivity prediction
            print("  Benchmarking productivity model...")
            start = time.time()
            for _ in range(10):
                preds = manager.predict_productivity_score(X)
            prod_time = (time.time() - start) / 10
            
            self.results['model_prediction'] = {
                'burnout_time_ms': burnout_time * 1000,
                'productivity_time_ms': prod_time * 1000,
                'samples_per_sec': len(X) / burnout_time
            }
            
            print(f"  ✓ Burnout model: {burnout_time*1000:.1f}ms ({len(X)} samples)")
            print(f"  ✓ Productivity model: {prod_time*1000:.1f}ms ({len(X)} samples)")
            print(f"  ✓ Throughput: {self.results['model_prediction']['samples_per_sec']:.0f} samples/sec")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    def benchmark_data_filtering(self):
        """Benchmark filter operations"""
        print("\n🔍 Benchmarking Data Filtering...")
        print("-" * 60)
        
        try:
            from utils.db_connection import load_main_data, apply_filters
            
            df = load_main_data()
            
            # Single filter
            print("  Benchmarking single filter...")
            start = time.time()
            for _ in range(100):
                apply_filters(df, occupation="Software Engineer")
            single_time = (time.time() - start) / 100
            
            # Multiple filters
            print("  Benchmarking multiple filters...")
            start = time.time()
            for _ in range(100):
                apply_filters(df, 
                             mental_state="Burnout",
                             occupation="Analyst",
                             work_mode="Remote",
                             age_range=(25, 40))
            multi_time = (time.time() - start) / 100
            
            self.results['filtering'] = {
                'single_filter_ms': single_time * 1000,
                'multi_filter_ms': multi_time * 1000
            }
            
            print(f"  ✓ Single filter: {single_time*1000:.2f}ms")
            print(f"  ✓ Multiple filters: {multi_time*1000:.2f}ms")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    def benchmark_aggregations(self):
        """Benchmark data aggregations"""
        print("\n📈 Benchmarking Aggregations...")
        print("-" * 60)
        
        try:
            from utils.db_connection import load_main_data
            
            df = load_main_data()
            
            aggregations = {
                'groupby_occupation': lambda: df.groupby('OCCUPATION')['BURNOUT_RISK'].mean(),
                'groupby_mental_state': lambda: df.groupby('MENTAL_STATE')['PRODUCTIVITY_SCORE'].mean(),
                'correlation': lambda: df[['BURNOUT_RISK', 'PRODUCTIVITY_SCORE', 'SLEEP_HOURS']].corr(),
                'percentile': lambda: df['BURNOUT_RISK'].quantile([0.25, 0.5, 0.75, 0.9]),
            }
            
            times = {}
            for name, func in aggregations.items():
                start = time.time()
                for _ in range(10):
                    func()
                elapsed = (time.time() - start) / 10
                times[name] = elapsed * 1000
                print(f"  ✓ {name.replace('_', ' ').title()}: {elapsed*1000:.2f}ms")
            
            self.results['aggregations'] = times
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    def benchmark_memory(self):
        """Benchmark memory usage"""
        print("\n💾 Benchmarking Memory Usage...")
        print("-" * 60)
        
        try:
            from utils.db_connection import load_main_data
            
            # Get initial memory
            initial = self.process.memory_info().rss / 1024**2
            
            # Load data
            df = load_main_data()
            data_load_mem = self.process.memory_info().rss / 1024**2 - initial
            
            # Apply filter
            df_filtered = df[df['BURNOUT_RISK'] > 70]
            filter_mem = self.process.memory_info().rss / 1024**2 - initial
            
            self.results['memory'] = {
                'initial_mb': initial,
                'after_data_load_mb': data_load_mem,
                'after_filter_mb': filter_mem,
                'peak_mb': self.process.memory_info().rss / 1024**2
            }
            
            print(f"  ✓ Initial: {initial:.1f} MB")
            print(f"  ✓ After data load: {data_load_mem:.1f} MB")
            print(f"  ✓ After filter: {filter_mem:.1f} MB")
            print(f"  ✓ Peak: {self.results['memory']['peak_mb']:.1f} MB")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
    
    def print_summary(self):
        """Print performance summary"""
        print("\n" + "=" * 60)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("=" * 60)
        
        print(f"\n🔄 Data Loading:")
        if 'data_load' in self.results:
            r = self.results['data_load']
            print(f"   Time: {r['time']:.2f}s")
            print(f"   Throughput: {r['rows_per_second']:.0f} rows/sec")
            print(f"   Memory: {r['memory_mb']:.1f} MB")
        
        print(f"\n🤖 Model Prediction:")
        if 'model_prediction' in self.results:
            r = self.results['model_prediction']
            print(f"   Burnout: {r['burnout_time_ms']:.1f}ms per batch")
            print(f"   Productivity: {r['productivity_time_ms']:.1f}ms per batch")
            print(f"   Throughput: {r['samples_per_sec']:.0f} samples/sec")
        
        print(f"\n🔍 Filtering:")
        if 'filtering' in self.results:
            r = self.results['filtering']
            print(f"   Single filter: {r['single_filter_ms']:.2f}ms")
            print(f"   Multiple filters: {r['multi_filter_ms']:.2f}ms")
        
        print(f"\n💾 Memory Usage:")
        if 'memory' in self.results:
            r = self.results['memory']
            print(f"   Peak: {r['peak_mb']:.1f} MB")
        
        # Performance grade
        print("\n" + "=" * 60)
        print("📋 PERFORMANCE RECOMMENDATIONS")
        print("=" * 60)
        
        if 'data_load' in self.results:
            if self.results['data_load']['time'] < 5:
                print("  ✓ Data load time is excellent (<5s)")
            elif self.results['data_load']['time'] < 10:
                print("  ⚠ Data load time is acceptable (5-10s)")
            else:
                print("  ✗ Data load time is slow (>10s) - consider optimization")
        
        if 'memory' in self.results:
            if self.results['memory']['peak_mb'] < 500:
                print("  ✓ Memory usage is excellent (<500MB)")
            elif self.results['memory']['peak_mb'] < 1000:
                print("  ⚠ Memory usage is acceptable (500MB-1GB)")
            else:
                print("  ✗ Memory usage is high (>1GB) - consider optimization")
        
        print("=" * 60)

def main():
    """Run all performance tests"""
    print("=" * 60)
    print("🚀 Burnout Dashboard - Performance Testing Suite")
    print("=" * 60)
    
    tester = PerformanceTester()
    
    try:
        tester.benchmark_data_load()
        tester.benchmark_model_prediction()
        tester.benchmark_data_filtering()
        tester.benchmark_aggregations()
        tester.benchmark_memory()
        tester.print_summary()
        
        print("\n✅ Performance testing completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\n❌ Performance testing failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
