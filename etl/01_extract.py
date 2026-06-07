# ==============================================================
# 01_extract.py — Read Excel files and save as clean CSVs
# ==============================================================
# What this script does:
#   - Reads each Excel file from data/raw/
#   - Shows you the shape and first few rows (so you can verify)
#   - Saves each sheet as a CSV into data/clean/
# Run this first before any other script.
# ==============================================================

import pandas as pd
import os

# ── Paths ──────────────────────────────────────────────────────
RAW_DIR   = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw')
CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')

# Make sure clean folder exists
os.makedirs(CLEAN_DIR, exist_ok=True)

# ── File map: filename → sheet name ───────────────────────────
FILES = {
    'companies.xlsx':     'Companies',
    'profitandloss.xlsx': 'Profit & Loss',
    'balancesheet.xlsx':  'Balance Sheet',
    'cashflow.xlsx':      'Cash Flow',
    'prosandcons.xlsx':   'Pros & Cons',
    'analysis.xlsx':      'Analysis',
    'documents.xlsx':     'Documents',
}

# ── Extract each file ──────────────────────────────────────────
for filename, sheet_name in FILES.items():
    filepath = os.path.join(RAW_DIR, filename)

    # Check file exists
    if not os.path.exists(filepath):
        print(f"⚠️  MISSING: {filename} — skipping")
        continue

    print(f"\n📂 Reading: {filename}")

    try:
        # header=1 skips the title row (row 0) and uses row 1 as column names
        df = pd.read_excel(filepath, sheet_name=sheet_name, header=1)
    except Exception:
        # If sheet name doesn't match exactly, just read the first sheet
        print(f"   ⚠️  Sheet '{sheet_name}' not found, reading first sheet instead")
        df = pd.read_excel(filepath, header=1)

    # Show info
    print(f"   ✅ Rows: {len(df)}  |  Columns: {list(df.columns)}")

    # Save to clean folder as CSV
    output_name = filename.replace('.xlsx', '.csv')
    output_path = os.path.join(CLEAN_DIR, output_name)
    df.to_csv(output_path, index=False)
    print(f"   💾 Saved to: data/clean/{output_name}")

print("\n✅ Extraction complete! Check your data/clean/ folder.")
