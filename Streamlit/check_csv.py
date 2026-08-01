#!/usr/bin/env python
"""
CSV Validation & Diagnostic Script
Checks if analysis.csv is in the correct format for the dashboard
Usage: python check_csv.py
"""

import pandas as pd
import os
from pathlib import Path

def check_csv():
    """Validate CSV file"""
    
    print("=" * 60)
    print("📊 CSV VALIDATION SCRIPT")
    print("=" * 60)
    
    csv_path = Path("analysis.csv")
    
    # Check if file exists
    print("\n✓ Checking file existence...")
    if not csv_path.exists():
        print("❌ ERROR: analysis.csv not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print(f"   Please place analysis.csv here")
        return False
    
    print("✅ File found: analysis.csv")
    
    # Load CSV
    print("\n✓ Loading CSV...")
    try:
        df = pd.read_csv(csv_path)
        print(f"✅ CSV loaded successfully")
        print(f"   Rows: {len(df):,}")
        print(f"   Columns: {len(df.columns)}")
    except Exception as e:
        print(f"❌ ERROR loading CSV: {str(e)}")
        return False
    
    # Check essential columns
    print("\n✓ Checking essential columns...")
    essential_cols = [
        'USER_ID', 'BURNOUT_RISK', 'PRODUCTIVITY_SCORE',
        'MENTAL_STATE', 'OCCUPATION', 'WORK_MODE', 'AGE',
        'SLEEP_HOURS', 'DAILY_SCREEN_TIME'
    ]
    
    missing_cols = [col for col in essential_cols if col not in df.columns]
    
    if missing_cols:
        print(f"❌ ERROR: Missing essential columns:")
        for col in missing_cols:
            print(f"   - {col}")
        print("\n   Available columns:")
        for col in df.columns:
            print(f"   ✓ {col}")
        return False
    
    print("✅ All essential columns present")
    
    # Check data types
    print("\n✓ Checking data types...")
    
    numeric_cols = ['BURNOUT_RISK', 'PRODUCTIVITY_SCORE', 'SLEEP_HOURS', 'DAILY_SCREEN_TIME']
    for col in numeric_cols:
        if col in df.columns:
            if not pd.api.types.is_numeric_dtype(df[col]):
                print(f"⚠️  WARNING: {col} is not numeric, converting...")
                df[col] = pd.to_numeric(df[col], errors='coerce')
    
    print("✅ Data types validated")
    
    # Check for null values
    print("\n✓ Checking for null values...")
    null_counts = df.isnull().sum()
    if null_counts.sum() > 0:
        print(f"⚠️  Found null values:")
        for col, count in null_counts[null_counts > 0].items():
            pct = (count / len(df)) * 100
            print(f"   - {col}: {count} ({pct:.1f}%)")
    else:
        print("✅ No null values found")
    
    # Check value ranges
    print("\n✓ Checking value ranges...")
    
    checks = {
        'AGE': (18, 65),
        'BURNOUT_RISK': (0, 100),
        'PRODUCTIVITY_SCORE': (0, 100),
        'SLEEP_HOURS': (3, 12),
        'DAILY_SCREEN_TIME': (0, 24)
    }
    
    for col, (min_val, max_val) in checks.items():
        if col in df.columns:
            actual_min = df[col].min()
            actual_max = df[col].max()
            
            if actual_min < min_val or actual_max > max_val:
                print(f"⚠️  {col}: Expected {min_val}-{max_val}, got {actual_min:.1f}-{actual_max:.1f}")
            else:
                print(f"✅ {col}: Range OK ({actual_min:.1f}-{actual_max:.1f})")
    
    # Check categorical values
    print("\n✓ Checking categorical values...")
    
    if 'MENTAL_STATE' in df.columns:
        states = set(df['MENTAL_STATE'].unique())
        expected_states = {'Burnout', 'Distracted', 'Balanced', 'Focused'}
        if not states.issubset(expected_states):
            print(f"⚠️  MENTAL_STATE unexpected values: {states - expected_states}")
        else:
            print(f"✅ MENTAL_STATE: OK")
    
    if 'WORK_MODE' in df.columns:
        modes = set(df['WORK_MODE'].unique())
        expected_modes = {'Remote', 'Hybrid', 'Office'}
        if not modes.issubset(expected_modes):
            print(f"⚠️  WORK_MODE unexpected values: {modes - expected_modes}")
        else:
            print(f"✅ WORK_MODE: OK")
    
    if 'OCCUPATION' in df.columns:
        occupations = df['OCCUPATION'].nunique()
        print(f"✅ OCCUPATION: {occupations} unique values")
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    print(f"✅ File: analysis.csv")
    print(f"✅ Rows: {len(df):,}")
    print(f"✅ Columns: {len(df.columns)}")
    print(f"✅ Data quality: {'Good' if null_counts.sum() == 0 else 'Check warnings above'}")
    
    print("\n" + "=" * 60)
    print("✅ CSV is ready for the dashboard!")
    print("=" * 60)
    print("\nNext step: Run 'streamlit run app.py'")
    
    return True

if __name__ == "__main__":
    try:
        success = check_csv()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
