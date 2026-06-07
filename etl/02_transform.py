# ==============================================================
# 02_transform.py — Clean and validate the extracted CSVs
# ==============================================================
# What this script does:
#   - Reads CSVs from data/clean/
#   - Fixes data types (numbers stored as text, etc.)
#   - Strips whitespace from text columns
#   - Replaces blank/null values with None (so DB handles them)
#   - Saves cleaned versions back to data/clean/ (overwrites)
# Run this after 01_extract.py
# ==============================================================

import pandas as pd
import numpy as np
import os

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')

# ── Helper: clean a numeric column safely ─────────────────────
def to_numeric(series):
    """Convert a column to numeric, turning errors into NaN."""
    return pd.to_numeric(series, errors='coerce')

# ── Helper: strip whitespace from all string columns ──────────
def clean_strings(df):
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype(str).str.strip()
        df[col] = df[col].replace({'nan': None, 'None': None, '': None})
    return df

# ==============================================================
# 1. COMPANIES
# ==============================================================
print("\n🔧 Cleaning: companies.csv")
df = pd.read_csv(os.path.join(CLEAN_DIR, 'companies.csv'))
df = clean_strings(df)

# Make sure numeric columns are actually numeric
for col in ['face_value', 'book_value', 'roce_percentage', 'roe_percentage']:
    if col in df.columns:
        df[col] = to_numeric(df[col])

# Rename opm_percentage / roe_percentage column if needed
if 'roce_percentage' not in df.columns and 'roce_percentage' not in df.columns:
    print("   ⚠️  roce_percentage column not found — check column names")

print(f"   ✅ {len(df)} companies | columns: {list(df.columns)}")
df.to_csv(os.path.join(CLEAN_DIR, 'companies.csv'), index=False)

# ==============================================================
# 2. PROFIT & LOSS
# ==============================================================
print("\n🔧 Cleaning: profitandloss.csv")
df = pd.read_csv(os.path.join(CLEAN_DIR, 'profitandloss.csv'))
df = clean_strings(df)

numeric_cols = [
    'sales', 'expenses', 'operating_profit', 'opm_percentage',
    'other_income', 'interest', 'depreciation', 'profit_before_tax',
    'tax_percentage', 'net_profit', 'eps', 'dividend_payout'
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = to_numeric(df[col])

# Rename column if it's called opm_percentage% or similar
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('%', 'percentage')

print(f"   ✅ {len(df)} rows | columns: {list(df.columns)}")
df.to_csv(os.path.join(CLEAN_DIR, 'profitandloss.csv'), index=False)

# ==============================================================
# 3. BALANCE SHEET
# ==============================================================
print("\n🔧 Cleaning: balancesheet.csv")
df = pd.read_csv(os.path.join(CLEAN_DIR, 'balancesheet.csv'))
df = clean_strings(df)

numeric_cols = [
    'equity_capital', 'reserves', 'borrowings', 'other_liabilities',
    'total_liabilities', 'fixed_assets', 'cwip', 'investments',
    'other_asset', 'total_assets'
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = to_numeric(df[col])

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(f"   ✅ {len(df)} rows | columns: {list(df.columns)}")
df.to_csv(os.path.join(CLEAN_DIR, 'balancesheet.csv'), index=False)

# ==============================================================
# 4. CASH FLOW
# ==============================================================
print("\n🔧 Cleaning: cashflow.csv")
df = pd.read_csv(os.path.join(CLEAN_DIR, 'cashflow.csv'))
df = clean_strings(df)

numeric_cols = [
    'operating_activity', 'investing_activity',
    'financing_activity', 'net_cash_flow'
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = to_numeric(df[col])

df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(f"   ✅ {len(df)} rows | columns: {list(df.columns)}")
df.to_csv(os.path.join(CLEAN_DIR, 'cashflow.csv'), index=False)

# ==============================================================
# 5. PROS & CONS
# ==============================================================
print("\n🔧 Cleaning: prosandcons.csv")
df = pd.read_csv(os.path.join(CLEAN_DIR, 'prosandcons.csv'))
df = clean_strings(df)
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

print(f"   ✅ {len(df)} rows | columns: {list(df.columns)}")
df.to_csv(os.path.join(CLEAN_DIR, 'prosandcons.csv'), index=False)

print("\n✅ Transformation complete! All CSVs cleaned and ready to load.")
