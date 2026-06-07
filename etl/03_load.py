# ==============================================================
# 03_load.py — Load cleaned CSVs into PostgreSQL
# ==============================================================
import pandas as pd
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# ── Load DB credentials from .env ─────────────────────────────
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'b100_warehouse')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASS = os.getenv('DB_PASSWORD', '')

CLEAN_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'clean')

# ── Connect to PostgreSQL ──────────────────────────────────────
print(f"\n🔌 Connecting to PostgreSQL: {DB_HOST}:{DB_PORT}/{DB_NAME}")
try:
    engine = create_engine(
        f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    )
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print("   ✅ Connected successfully!")
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    exit(1)

# ── Helper: load a CSV into a table ───────────────────────────
def load_table(csv_filename, table_name):
    filepath = os.path.join(CLEAN_DIR, csv_filename)
    if not os.path.exists(filepath):
        print(f"   ⚠️  {csv_filename} not found — skipping")
        return

    df = pd.read_csv(filepath)

    # Replace NaN with None so PostgreSQL gets proper NULLs
    df = df.where(pd.notnull(df), None)

    print(f"\n📥 Loading {table_name} ({len(df)} rows)...")

    try:
        # Drop and recreate table with the data (simplest, avoids FK conflicts)
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='replace',  # drops old table, creates fresh one
            index=False,
            method='multi',
            chunksize=500
        )
        print(f"   ✅ {table_name}: {len(df)} rows loaded")
    except Exception as e:
        print(f"   ❌ Failed to load {table_name}: {e}")

# ==============================================================
# Load all tables
# ==============================================================
load_table('companies.csv',     'dim_company')
load_table('profitandloss.csv', 'fact_profit_loss')
load_table('balancesheet.csv',  'fact_balance_sheet')
load_table('cashflow.csv',      'fact_cash_flow')
load_table('prosandcons.csv',   'fact_pros_cons')

# ==============================================================
# Verify — print row counts from the database
# ==============================================================
print("\n📊 Verifying row counts in database...")
tables = [
    'dim_company', 'fact_profit_loss', 'fact_balance_sheet',
    'fact_cash_flow', 'fact_pros_cons'
]
with engine.connect() as conn:
    for table in tables:
        try:
            result = conn.execute(text(f'SELECT COUNT(*) FROM {table}'))
            count = result.scalar()
            print(f"   {table}: {count} rows")
        except Exception as e:
            print(f"   ❌ Could not count {table}: {e}")

print("\n✅ Load complete! Your database is ready.")
print("   Next step: open Power BI and connect to b100_warehouse")
