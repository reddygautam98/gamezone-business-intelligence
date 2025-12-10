"""
Load GameZone Data Mart into PostgreSQL Database
Using psycopg2 directly (no SQLAlchemy)
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("[INFO] === GameZone Data Mart → PostgreSQL ===\n")

# Configuration - Load from environment variables
HOST = os.getenv('DB_HOST', '127.0.0.1')
PORT = int(os.getenv('DB_PORT', 5432))
DATABASE = os.getenv('DB_NAME', 'gamezone_analytics')
USERNAME = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', '')

# Validate that password is provided
if not PASSWORD:
    print("❌ Error: Database password not found in environment variables!")
    print("📋 Please create a .env file with DB_PASSWORD or set environment variable")
    print("📝 Template: Copy .env.example to .env and update with your credentials")
    exit(1)

# ===================================================================
# 1. CONNECT AND CREATE DATABASE
# ===================================================================
print("[CONNECT] Connecting to PostgreSQL...")

try:
    # First connect to default postgres database
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL\n")
    
    # Check if database exists and drop it
    print(f"[CREATE] Creating database '{DATABASE}'...")
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE}")
    cursor.execute(f"CREATE DATABASE {DATABASE}")
    cursor.close()
    conn.close()
    print(f"✅ Database '{DATABASE}' created\n")
    
except psycopg2.Error as e:
    print(f"❌ Error: {e}")
    exit(1)

# ===================================================================
# 2. CONNECT TO NEW DATABASE
# ===================================================================
print(f"[CONNECT] Connecting to '{DATABASE}' database...")

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()[0]
    print(f"✅ Connected to '{DATABASE}'\n{version[:80]}...\n")
    
except psycopg2.Error as e:
    print(f"❌ Error connecting: {e}")
    exit(1)

# ===================================================================
# 3. CREATE TABLES
# ===================================================================
print("[CREATE] Creating dimension and fact tables...\n")

# Create dimension tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_date (
        date_key INT PRIMARY KEY,
        order_date DATE,
        order_year FLOAT,
        order_month FLOAT,
        order_month_name VARCHAR(10),
        order_year_month VARCHAR(10)
    )
""")
print("  ✅ dim_date")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_customer (
        customer_id VARCHAR(50) PRIMARY KEY,
        country_code VARCHAR(10),
        account_creation_method VARCHAR(50)
    )
""")
print("  ✅ dim_customer")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_product (
        product_id VARCHAR(50) PRIMARY KEY,
        product_name VARCHAR(255)
    )
""")
print("  ✅ dim_product")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_country (
        country_code VARCHAR(10) PRIMARY KEY
    )
""")
print("  ✅ dim_country")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_platform (
        platform VARCHAR(50) PRIMARY KEY
    )
""")
print("  ✅ dim_platform")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_marketing_channel (
        marketing_channel VARCHAR(50) PRIMARY KEY
    )
""")
print("  ✅ dim_marketing_channel")

# Create fact table with dynamic columns
# First, let's read the CSV to determine columns
import pandas as pd
fact_csv_columns = pd.read_csv("fact_orders.csv", nrows=0).columns.tolist() if os.path.exists("fact_orders.csv") else []

col_defs = []
for col in fact_csv_columns:
    col_defs.append(f"{col} VARCHAR(500)")

if col_defs:
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS fact_orders (
            {', '.join(col_defs)}
        )
    """)
else:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_orders (
            order_id VARCHAR(50),
            date_key INT,
            order_date VARCHAR(50),
            customer_id VARCHAR(50),
            product_id VARCHAR(50),
            unit_price DECIMAL(18,2),
            purchase_platform VARCHAR(50),
            marketing_channel VARCHAR(50),
            account_creation_method VARCHAR(50),
            country_code VARCHAR(10),
            order_year FLOAT,
            order_month FLOAT,
            order_month_name VARCHAR(10),
            order_year_month VARCHAR(10),
            ship_ts VARCHAR(50)
        )
    """)
print("  ✅ fact_orders")

print()

# ===================================================================
# 4. LOAD DATA FROM CSV
# ===================================================================
print("[LOAD] Loading data from CSV files...\n")

def load_csv_to_postgres(csv_file, table_name):
    """Load CSV into PostgreSQL table"""
    if not os.path.exists(csv_file):
        print(f"  ⚠️  {csv_file} not found, skipping...")
        return 0
    
    try:
        df = pd.read_csv(csv_file)
        
        # Clear table first
        cursor.execute(f"TRUNCATE TABLE {table_name} CASCADE")
        
        # Prepare columns and values
        columns = df.columns.tolist()
        
        # Insert data row by row
        insert_count = 0
        for idx, row in df.iterrows():
            placeholders = ", ".join(["%s"] * len(columns))
            col_names = ", ".join(columns)
            query = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
            
            try:
                # Convert NaN to None for proper NULL handling
                values = tuple(None if pd.isna(v) else v for v in row)
                cursor.execute(query, values)
                insert_count += 1
            except Exception as e:
                print(f"    Warning: Row {idx} error: {e}")
        
        conn.commit()
        print(f"  ✅ {table_name:.<40} {insert_count:>8,} records")
        return insert_count
        
    except Exception as e:
        print(f"  ❌ Error loading {table_name}: {e}")
        return 0

# Load tables
print("  [DIMENSION TABLES]")
load_csv_to_postgres("dim_date.csv", "dim_date")
load_csv_to_postgres("dim_customer.csv", "dim_customer")
load_csv_to_postgres("dim_product.csv", "dim_product")
load_csv_to_postgres("dim_country.csv", "dim_country")
load_csv_to_postgres("dim_platform.csv", "dim_platform")
load_csv_to_postgres("dim_marketing_channel.csv", "dim_marketing_channel")

print("\n  [FACT TABLES]")
load_csv_to_postgres("fact_orders.csv", "fact_orders")

print()

# ===================================================================
# 5. CREATE INDEXES
# ===================================================================
print("[INDEX] Creating indexes...\n")

indexes = [
    "CREATE INDEX IF NOT EXISTS idx_fact_customer ON fact_orders(customer_id)",
    "CREATE INDEX IF NOT EXISTS idx_fact_product ON fact_orders(product_id)",
    "CREATE INDEX IF NOT EXISTS idx_fact_order ON fact_orders(order_id)",
    "CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_orders(date_key)",
]

for idx_query in indexes:
    try:
        cursor.execute(idx_query)
        idx_name = idx_query.split()[-5]
        print(f"  ✅ {idx_name}")
    except Exception as e:
        pass

conn.commit()
print()

# ===================================================================
# 6. VALIDATION
# ===================================================================
print("[VALIDATE] Running validation queries...\n")

queries = [
    ("Total orders", "SELECT COUNT(*) FROM fact_orders"),
    ("Unique customers", "SELECT COUNT(DISTINCT customer_id) FROM dim_customer"),
    ("Unique products", "SELECT COUNT(DISTINCT product_id) FROM dim_product"),
    ("Unique dates", "SELECT COUNT(*) FROM dim_date"),
    ("Unique countries", "SELECT COUNT(*) FROM dim_country"),
    ("Dates loaded", "SELECT COUNT(*) FROM fact_orders WHERE date_key IS NOT NULL"),
]

for label, query in queries:
    cursor.execute(query)
    result = cursor.fetchone()[0]
    print(f"  {label:.<35} {result:>10,}")

print()

# ===================================================================
# 7. CONNECTION INFO
# ===================================================================
info = f"""
POSTGRESQL CONNECTION INFO:
  Host:         {HOST}
  Port:         {PORT}
  Database:     {DATABASE}
  Username:     {USERNAME}

PYTHON CONNECTION:
  import psycopg2
  conn = psycopg2.connect(
      host="{HOST}",
      port={PORT},
      database="{DATABASE}",
      user="{USERNAME}",
      password="YOUR_PASSWORD"
  )

TABLES CREATED:
  ✅ dim_date
  ✅ dim_customer
  ✅ dim_product
  ✅ dim_country
  ✅ dim_platform
  ✅ dim_marketing_channel
  ✅ fact_orders

SAMPLE QUERIES:

  -- Top 10 customers by order count
  SELECT customer_id, COUNT(*) as order_count 
  FROM fact_orders 
  GROUP BY customer_id 
  ORDER BY order_count DESC LIMIT 10;

  -- Top products
  SELECT p.product_id, p.product_name, COUNT(*) as orders
  FROM fact_orders f
  JOIN dim_product p ON f.product_id = p.product_id
  GROUP BY p.product_id, p.product_name
  ORDER BY orders DESC LIMIT 5;

  -- Orders by country
  SELECT c.country_code, COUNT(*) as orders
  FROM fact_orders f
  JOIN dim_customer c ON f.customer_id = c.customer_id
  GROUP BY c.country_code
  ORDER BY orders DESC;

  -- Orders by platform
  SELECT purchase_platform, COUNT(*) as orders
  FROM fact_orders
  GROUP BY purchase_platform;
"""

print(info)

cursor.close()
conn.close()

print("="*70)
print("[SUCCESS] ✅ Data Mart Loaded into PostgreSQL!")
print("="*70)
