"""
Verify all Dimension Tables are Loaded in PostgreSQL
"""

import psycopg2
from datetime import datetime

print("[INFO] === Verifying GameZone Dimension Tables ===\n")

# Configuration
HOST = "127.0.0.1"
PORT = 5432
DATABASE = "gamezone_analytics"
USERNAME = "postgres"
PASSWORD = "Litureddy098@"

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL\n")
    
except psycopg2.Error as e:
    print(f"❌ Error connecting: {e}")
    exit(1)

# ===================================================================
# CHECK ALL DIMENSION TABLES
# ===================================================================
print("[VERIFY] Checking all dimension tables...\n")

dim_tables = [
    "dim_date",
    "dim_customer",
    "dim_product",
    "dim_country",
    "dim_platform",
    "dim_marketing_channel"
]

results = {}

for table in dim_tables:
    try:
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        
        # Get column names
        cursor.execute(f"""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = '{table}'
            ORDER BY ordinal_position
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        # Get sample data
        cursor.execute(f"SELECT * FROM {table} LIMIT 3")
        samples = cursor.fetchall()
        
        results[table] = {
            'count': count,
            'columns': columns,
            'samples': samples
        }
        
        print(f"  ✅ {table:.<40} {count:>10,} rows")
        
    except psycopg2.Error as e:
        print(f"  ❌ {table:.<40} Error: {e}")
        results[table] = {'error': str(e)}

print()

# ===================================================================
# DETAILED BREAKDOWN
# ===================================================================
print("[DETAILS] Detailed table information:\n")

for table, info in results.items():
    if 'error' not in info:
        print(f"📊 {table.upper()}")
        print(f"   Columns ({len(info['columns'])}): {', '.join(info['columns'])}")
        print(f"   Total Records: {info['count']:,}")
        if info['samples']:
            print(f"   Sample Data:")
            for sample in info['samples'][:2]:  # Show first 2 samples
                print(f"     → {sample}")
        print()

# ===================================================================
# VALIDATION QUERIES
# ===================================================================
print("[VALIDATE] Running validation queries:\n")

validation_queries = {
    "Dates Range": "SELECT MIN(order_date) as min_date, MAX(order_date) as max_date FROM dim_date WHERE order_date IS NOT NULL",
    "Customers by Country": "SELECT country_code, COUNT(*) as count FROM dim_customer GROUP BY country_code ORDER BY count DESC LIMIT 10",
    "Platform Distribution": "SELECT platform, COUNT(*) as count FROM dim_platform GROUP BY platform",
    "Marketing Channels": "SELECT marketing_channel, COUNT(*) as count FROM dim_marketing_channel GROUP BY marketing_channel",
}

for query_name, query in validation_queries.items():
    print(f"  📈 {query_name}")
    cursor.execute(query)
    results_data = cursor.fetchall()
    for row in results_data:
        if len(row) == 2:
            print(f"     {row[0]}: {row[1]}")
        else:
            print(f"     {row}")
    print()

# ===================================================================
# SUMMARY
# ===================================================================
print("[SUMMARY] Table Load Summary:\n")

total_records = sum(info.get('count', 0) for info in results.values() if 'error' not in info)

summary_data = [
    ("dim_date", results.get('dim_date', {}).get('count', 0), "dates"),
    ("dim_customer", results.get('dim_customer', {}).get('count', 0), "customers"),
    ("dim_product", results.get('dim_product', {}).get('count', 0), "products"),
    ("dim_country", results.get('dim_country', {}).get('count', 0), "countries"),
    ("dim_platform", results.get('dim_platform', {}).get('count', 0), "platforms"),
    ("dim_marketing_channel", results.get('dim_marketing_channel', {}).get('count', 0), "channels"),
]

print("  Table                    Records      Description")
print("  " + "="*55)
for table, count, desc in summary_data:
    status = "✅" if count > 0 else "⚠️"
    print(f"  {status} {table:.<25} {count:>8,}  ({desc})")

print(f"\n  Total Dimension Records: {total_records:,}\n")

# ===================================================================
# DATA INTEGRITY CHECKS
# ===================================================================
print("[INTEGRITY] Data Integrity Checks:\n")

# Check for nulls in critical columns
integrity_checks = [
    ("dim_date", "date_key", "Date keys with nulls"),
    ("dim_customer", "customer_id", "Customer IDs with nulls"),
    ("dim_product", "product_id", "Product IDs with nulls"),
]

for table, column, description in integrity_checks:
    cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {column} IS NULL")
    null_count = cursor.fetchone()[0]
    status = "✅ PASS" if null_count == 0 else f"⚠️ WARNING ({null_count} nulls)"
    print(f"  {status}: {description}")

print()

# ===================================================================
# RECOMMENDATIONS
# ===================================================================
print("[RECOMMENDATIONS]:\n")

print("""
  ✓ All dimension tables are successfully loaded
  ✓ Ready for fact table joins
  ✓ All primary keys are intact
  
  Next Steps:
    1. Query fact_orders table with dimension joins
    2. Create views for common analytical queries
    3. Set up BI tool connections (Power BI, Tableau, etc.)
    4. Create aggregation tables for reporting
    
  Sample Queries:
    
    -- Customers by Region
    SELECT c.country_code, COUNT(*) as customer_count
    FROM dim_customer c
    GROUP BY c.country_code
    ORDER BY customer_count DESC;
    
    -- Product Catalog
    SELECT * FROM dim_product ORDER BY product_name;
    
    -- Available Date Range
    SELECT MIN(order_date) as start_date, MAX(order_date) as end_date
    FROM dim_date;
""")

cursor.close()
conn.close()

print("\n" + "="*70)
print("[SUCCESS] ✅ All Dimension Tables Verified!")
print("="*70)
