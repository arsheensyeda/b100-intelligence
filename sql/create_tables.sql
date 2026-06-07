-- ============================================================
-- B100 Intelligence — Create Tables Script
-- Run this ONCE in pgAdmin before running the ETL scripts
-- ============================================================

-- Drop tables if they exist (clean slate)
DROP TABLE IF EXISTS fact_pros_cons CASCADE;
DROP TABLE IF EXISTS fact_cash_flow CASCADE;
DROP TABLE IF EXISTS fact_balance_sheet CASCADE;
DROP TABLE IF EXISTS fact_profit_loss CASCADE;
DROP TABLE IF EXISTS dim_company CASCADE;

-- ============================================================
-- DIMENSION TABLE: Companies
-- ============================================================
CREATE TABLE dim_company (
    id                VARCHAR(20) PRIMARY KEY,
    company_name      TEXT NOT NULL,
    company_logo      TEXT,
    chart_link        TEXT,
    about_company     TEXT,
    website           TEXT,
    nse_profile       TEXT,
    bse_profile       TEXT,
    face_value        NUMERIC,
    book_value        NUMERIC,
    roce_percentage   NUMERIC,
    roe_percentage    NUMERIC
);

-- ============================================================
-- FACT TABLE: Profit & Loss
-- ============================================================
CREATE TABLE fact_profit_loss (
    id                  INTEGER PRIMARY KEY,
    company_id          VARCHAR(20) REFERENCES dim_company(id),
    year                VARCHAR(20),
    sales               NUMERIC,
    expenses            NUMERIC,
    operating_profit    NUMERIC,
    opm_percentage      NUMERIC,
    other_income        NUMERIC,
    interest            NUMERIC,
    depreciation        NUMERIC,
    profit_before_tax   NUMERIC,
    tax_percentage      NUMERIC,
    net_profit          NUMERIC,
    eps                 NUMERIC,
    dividend_payout     NUMERIC
);

-- ============================================================
-- FACT TABLE: Balance Sheet
-- ============================================================
CREATE TABLE fact_balance_sheet (
    id                  INTEGER PRIMARY KEY,
    company_id          VARCHAR(20) REFERENCES dim_company(id),
    year                VARCHAR(20),
    equity_capital      NUMERIC,
    reserves            NUMERIC,
    borrowings          NUMERIC,
    other_liabilities   NUMERIC,
    total_liabilities   NUMERIC,
    fixed_assets        NUMERIC,
    cwip                NUMERIC,
    investments         NUMERIC,
    other_asset         NUMERIC,
    total_assets        NUMERIC
);

-- ============================================================
-- FACT TABLE: Cash Flow
-- ============================================================
CREATE TABLE fact_cash_flow (
    id                          INTEGER PRIMARY KEY,
    company_id                  VARCHAR(20) REFERENCES dim_company(id),
    year                        VARCHAR(20),
    operating_activity          NUMERIC,
    investing_activity          NUMERIC,
    financing_activity          NUMERIC,
    net_cash_flow               NUMERIC
);

-- ============================================================
-- FACT TABLE: Pros & Cons
-- ============================================================
CREATE TABLE fact_pros_cons (
    id                  INTEGER PRIMARY KEY,
    company_id          VARCHAR(20) REFERENCES dim_company(id),
    pros                TEXT,
    cons                TEXT
);

-- Verify tables were created
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
