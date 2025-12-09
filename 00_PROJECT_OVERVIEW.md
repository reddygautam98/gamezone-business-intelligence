# 🎮 GameZone Business Intelligence Platform

**Version:** 1.0.0  
**Last Updated:** December 8, 2025  
**Status:** ✅ Production Ready

---

## 📖 Table of Contents

1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Folder Structure](#folder-structure)
4. [Data Architecture](#data-architecture)
5. [SQL Queries](#sql-queries)
6. [Python Scripts](#python-scripts)
7. [Data Files](#data-files)
8. [Getting Started](#getting-started)
9. [Support & Documentation](#support--documentation)

---

## 📊 Project Overview

**GameZone Business Intelligence** is a comprehensive analytics platform designed for operational and strategic decision-making. It provides:

- ✅ **Real-time analytics** - Up-to-date order and customer insights
- ✅ **Strategic reporting** - Executive-level business metrics
- ✅ **Data-driven decisions** - Foundation for strategic planning
- ✅ **Multi-layered queries** - From foundational to advanced analytics
- ✅ **Clean data architecture** - Dimension and fact table structure

### Key Metrics

| Metric | Value |
|--------|-------|
| **Total Orders** | 21,670 |
| **Active Customers** | 19,665 |
| **Products Tracked** | 43 |
| **Countries Served** | 150+ |
| **Date Range** | 2019-01-01 to 2021-02-28 |
| **Data Freshness** | PostgreSQL Database |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- CSV data files
- pgAdmin (optional, for UI management)

### Installation (5 minutes)

```bash
# 1. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 2. Load data to PostgreSQL
python 01_load_data_to_database.py

# 3. Verify dimension tables
python 03_verify_dimension_tables.py

# 4. Build analytical tables
python 02_build_analytical_tables.py

# 5. Run SQL queries
# Open queries_foundational_analytics.sql in pgAdmin or your SQL client
```

### Running Your First Query

```sql
-- Open queries_foundational_analytics.sql
-- Select Query 1: Total Orders & Revenue Overview
-- Execute to see:
-- - Total orders in system
-- - Total revenue (USD)
-- - Average order value
-- - Date range of data
```

---

## 📁 Folder Structure

### Professional Organization

```
gamezone-business-intelligence/
│
├── 🐍 PYTHON SCRIPTS (ETL Pipeline)
│   ├── 01_load_data_to_database.py         # Load CSV → PostgreSQL
│   ├── 02_build_analytical_tables.py        # Create analytical structures
│   ├── 03_verify_dimension_tables.py        # Validate dimension data
│   └── 04_inspect_fact_table_schema.py      # Inspect fact table structure
│
├── 💾 SQL QUERY FILES (Analytics Engine)
│   ├── queries_foundational_analytics.sql   # 50+ foundation queries (10 sections)
│   └── queries_strategic_analytics.sql      # 6 strategic queries for executives
│
├── 📚 DOCUMENTATION (Guides & References)
│   ├── 00_PROJECT_OVERVIEW.md               # This file (project introduction)
│   └── 01_QUICK_REFERENCE_GUIDE.md          # Quick lookup & navigation
│
├── 📊 DIMENSION TABLES (Reference Data)
│   ├── dim_01_customers.csv                 # 19,665 customer records
│   ├── dim_02_products.csv                  # 43 products
│   ├── dim_03_dates.csv                     # 772 dates (complete calendar)
│   ├── dim_04_countries.csv                 # 150+ countries
│   ├── dim_05_platforms.csv                 # 2 platforms (website, mobile)
│   └── dim_06_marketing_channels.csv        # 5 marketing channels
│
├── 📈 FACT TABLE (Transaction Data)
│   └── fact_01_orders_transactions.csv      # 21,670 order records
│
├── 📄 PROJECT FILES
│   ├── LICENSE                              # Project license
│   └── .git/                                # Version control
│
└── 🔧 SYSTEM FOLDERS
    └── .venv/                               # Python virtual environment
```

---

## 🗄️ Data Architecture

### Star Schema Design

```
                    ┌─────────────────────────────────┐
                    │   fact_01_orders_transactions   │
                    │      (21,670 records)           │
                    └─────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────────┐  ┌─────────────┐  ┌──────────────┐
        │ dim_01_customers  │  │ dim_02_     │  │ dim_03_dates │
        │  (19,665 records) │  │ products    │  │ (772 records)│
        │                   │  │ (43)        │  │              │
        └───────────────────┘  └─────────────┘  └──────────────┘
                    │               │               │
                    ▼               ▼               ▼
        ┌───────────────────┐  ┌─────────────┐  ┌──────────────┐
        │ dim_04_countries  │  │ dim_05_     │  │ dim_06_      │
        │  (150+ countries) │  │ platforms   │  │ marketing_   │
        │                   │  │ (2)         │  │ channels (5) │
        └───────────────────┘  └─────────────┘  └──────────────┘
```

### Fact Table Columns

| Column | Type | Purpose |
|--------|------|---------|
| `order_id` | UUID | Unique transaction identifier |
| `customer_id` | INT | Link to customers dimension |
| `product_id` | INT | Link to products dimension |
| `order_date` | DATE | Link to dates dimension |
| `ship_ts` | TIMESTAMP | Shipping timestamp for analysis |
| `order_amount_usd` | DECIMAL | Transaction amount (primary metric) |
| `country_code` | VARCHAR | Link to countries dimension |
| `purchase_platform` | VARCHAR | Link to platforms dimension |
| `marketing_channel` | VARCHAR | Link to marketing_channels dimension |
| `account_creation_method` | VARCHAR | How customer signed up |

---

## 📝 SQL Queries

### Two-Layer Query Architecture

#### Layer 1: Foundational Analytics (50+ Queries)
**File:** `queries_foundational_analytics.sql`

**Purpose:** Daily operations, standard business questions, foundation for analysis

**10 Organized Sections:**
1. **Basic Overview** - Total orders, revenue, KPIs
2. **Revenue Analysis** - By country, month, year, growth
3. **Product Analysis** - Top sellers, performance ranking
4. **Customer Analysis** - Top customers, segmentation
5. **Platform & Marketing** - Channel performance, effectiveness
6. **Date & Time Analysis** - Temporal patterns, trends
7. **Business Metrics** - Repeat rates, distribution
8. **Data Quality** - Validation, completeness checks
9. **KPI Dashboard** - Executive summary
10. **Sample Analytics** - Ready-to-use templates

**Usage:**
```sql
-- Open in pgAdmin or SQL client
-- Query examples: SELECT *, FROM... WHERE...
-- Execution time: 2-30 seconds per query
-- No data modification (read-only)
```

#### Layer 2: Strategic Analytics (6 Queries)
**File:** `queries_strategic_analytics.sql`

**Purpose:** Board presentations, quarterly reviews, strategic planning

**Query Contents:**
1. **YoY Revenue Growth** - 2020 vs 2021, growth percentages
2. **Marketing Channel Effectiveness** - ROI by platform × channel
3. **Top 10 Products** - Latest vs prior year with growth rates
4. **New vs Repeat Customers** - Monthly cohort analysis
5. **Pareto 80/20 Analysis** - Market concentration
6. **Shipping Time Analysis** - Days by country & platform

**Usage:**
```sql
-- These queries answer strategic business questions
-- Use for executive reporting and presentations
-- Includes advanced features: CTEs, window functions, percentiles
```

---

## 🐍 Python Scripts

### ETL Pipeline (Sequential Execution)

#### 1️⃣ `01_load_data_to_database.py`
- **Purpose:** Load CSV files into PostgreSQL
- **Input:** All CSV files (dim_* and fact_*)
- **Output:** PostgreSQL tables in gamezone_analytics database
- **Time:** ~1-2 minutes
```bash
python 01_load_data_to_database.py
```

#### 2️⃣ `02_build_analytical_tables.py`
- **Purpose:** Create analytical structures and indexes
- **Input:** Loaded PostgreSQL tables
- **Output:** Optimized analytics tables
- **Time:** ~30 seconds
```bash
python 02_build_analytical_tables.py
```

#### 3️⃣ `03_verify_dimension_tables.py`
- **Purpose:** Verify all dimension tables loaded correctly
- **Input:** PostgreSQL database
- **Output:** Validation report (stdout)
- **Time:** ~10 seconds
```bash
python 03_verify_dimension_tables.py
```

**Expected Output:**
```
✅ dim_customers: 19,665 records
✅ dim_products: 43 records
✅ dim_dates: 772 records
✅ dim_countries: 150+ records
✅ dim_platforms: 2 records
✅ dim_marketing_channels: 5 records
```

#### 4️⃣ `04_inspect_fact_table_schema.py`
- **Purpose:** Inspect fact table structure and columns
- **Input:** PostgreSQL database
- **Output:** Schema information (stdout)
- **Time:** ~5 seconds
```bash
python 04_inspect_fact_table_schema.py
```

---

## 📊 Data Files

### Dimension Tables (Reference Data)

| File | Records | Purpose |
|------|---------|---------|
| `dim_01_customers.csv` | 19,665 | Customer attributes & metadata |
| `dim_02_products.csv` | 43 | Product catalog |
| `dim_03_dates.csv` | 772 | Complete date dimension |
| `dim_04_countries.csv` | 150+ | Geographic reference |
| `dim_05_platforms.csv` | 2 | Purchase channels |
| `dim_06_marketing_channels.csv` | 5 | Marketing sources |

### Fact Table (Transaction Data)

| File | Records | Purpose |
|------|---------|---------|
| `fact_01_orders_transactions.csv` | 21,670 | Complete order transactions |

---

## 🚀 Getting Started

### Step 1: Setup Database
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Load data
python 01_load_data_to_database.py
```

### Step 2: Verify Data
```bash
# Verify all dimension tables
python 03_verify_dimension_tables.py
```

### Step 3: Run Queries
1. Open pgAdmin (http://localhost:5050)
2. Open `queries_foundational_analytics.sql`
3. Select and execute any query
4. View results

### Step 4: Export Results
```sql
-- Export query results
COPY (SELECT * FROM fact_01_orders_transactions LIMIT 100) 
TO '/tmp/export.csv' 
WITH (FORMAT csv, HEADER);
```

---

## 📚 Documentation

### Quick Reference
**File:** `01_QUICK_REFERENCE_GUIDE.md`
- Query selection guide
- File navigation
- Troubleshooting
- Common commands

### Query Documentation
See individual SQL files for:
- Detailed query descriptions
- Column explanations
- Business logic
- Example outputs

---

## 🔗 Database Connection

### PostgreSQL Details
```
Host:       localhost
Port:       5432
Database:   gamezone_analytics
User:       postgres
Password:   [your password]
```

### Connection String
```python
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="gamezone_analytics",
    user="postgres",
    password="your_password"
)
```

### pgAdmin Access
```
URL:        http://localhost:5050
Username:   admin@pgadmin.org
Password:   [your password]
```

---

## ❓ Support & Documentation

### Common Questions

**Q: How do I run a query?**
A: Open `queries_foundational_analytics.sql` in pgAdmin, select query, run.

**Q: Where is my data?**
A: PostgreSQL database `gamezone_analytics` on localhost:5432

**Q: How do I add new data?**
A: Update CSV files, run `01_load_data_to_database.py`

**Q: Can I modify queries?**
A: Yes, all SQL files are read-write editable.

**Q: How often is data updated?**
A: As often as you run the load script.

### Getting Help

1. Check `01_QUICK_REFERENCE_GUIDE.md` for common issues
2. Review SQL file comments for query details
3. Run verification scripts to check data integrity
4. Check PostgreSQL logs for errors

---

## 📋 Checklist - First Time Setup

- [ ] Activate virtual environment (`.\.venv\Scripts\Activate.ps1`)
- [ ] Run load script (`python 01_load_data_to_database.py`)
- [ ] Run verification script (`python 03_verify_dimension_tables.py`)
- [ ] Open pgAdmin (http://localhost:5050)
- [ ] Test first query from `queries_foundational_analytics.sql`
- [ ] Bookmark `01_QUICK_REFERENCE_GUIDE.md` for quick lookup

---

## 📈 Project Stats

- **Total Queries:** 56+ (50 foundational + 6 strategic)
- **Data Records:** 21,670 orders across 19,665 customers
- **Time Period:** 2019-01-01 to 2021-02-28
- **Database:** PostgreSQL 12+
- **Files:** 15 (4 scripts, 2 SQL, 7 CSVs, 2 docs, LICENSE)
- **Total Size:** ~6.5 MB

---

## 📄 License

See LICENSE file for full project license and terms.

---

## 🎯 Next Steps

1. **Complete Setup** - Follow "Getting Started" section
2. **Run Sample Queries** - Start with foundational analytics
3. **Explore Data** - Use strategic queries for insights
4. **Build Reports** - Export data for presentations
5. **Integrate BI Tools** - Connect to Power BI or Tableau

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** December 8, 2025
