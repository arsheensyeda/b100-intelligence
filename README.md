# B100 Intelligence — Data Engineering Foundation

## How to run the ETL pipeline (in order)

### Step 1 — Set up your .env file
Edit `.env` and fill in your PostgreSQL password.

### Step 2 — Create tables in pgAdmin
Open pgAdmin → b100_warehouse → Tools → Query Tool
Paste and run the contents of `sql/create_tables.sql`

### Step 3 — Run the ETL scripts in VS Code terminal
```bash
cd b100_intelligence
python etl/01_extract.py
python etl/02_transform.py
python etl/03_load.py
```

## Folder structure
```
b100_intelligence/
├── data/
│   ├── raw/         ← put all 7 xlsx files here
│   └── clean/       ← auto-generated CSVs
├── etl/
│   ├── 01_extract.py
│   ├── 02_transform.py
│   └── 03_load.py
├── sql/
│   └── create_tables.sql
├── .env             ← your DB credentials (never commit this)
└── requirements.txt
```

## Tables created
| Table | Description |
|---|---|
| dim_company | 92 Nifty 100 companies |
| fact_profit_loss | P&L data per company per year |
| fact_balance_sheet | Balance sheet data |
| fact_cash_flow | Cash flow data |
| fact_pros_cons | Auto-generated pros and cons |
