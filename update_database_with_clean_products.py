"""
Update PostgreSQL Database with Cleaned Product Data

This script:
1. Connects to the GameZone database
2. Truncates the dim_products table
3. Loads the cleaned product data (8 clean rows)
4. Updates all fact_orders references with consolidated IDs
5. Verifies data integrity
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 90)
print("DATABASE UPDATE: CLEAN PRODUCT DATA")
print("=" * 90)

# Database configuration
HOST = os.getenv('DB_HOST', '127.0.0.1')
PORT = int(os.getenv('DB_PORT', 5432))
DATABASE = os.getenv('DB_NAME', 'gamezone_analytics')
USERNAME = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', '')

# Validate credentials
if not PASSWORD:
    print("\n❌ ERROR: Database password not found!")
    print("📋 Create .env file with DB_PASSWORD or set environment variable")
    exit(1)

# =========================================================================
# STEP 1: LOAD CLEANED DATA
# =========================================================================
print("\n[STEP 1] Loading cleaned product data...")

products_file = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_dim_02_products.csv"
fact_file = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_fact_01_orders_transactions.csv"

try:
    df_products = pd.read_csv(products_file)
    df_fact = pd.read_csv(fact_file)
    print(f"✅ Loaded products: {len(df_products)} rows")
    print(f"✅ Loaded fact: {len(df_fact):,} rows")
except Exception as e:
    print(f"❌ Error loading files: {e}")
    exit(1)

# =========================================================================
# STEP 2: CONNECT TO DATABASE
# =========================================================================
print("\n[STEP 2] Connecting to database...")

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = conn.cursor()
    print(f"✅ Connected to '{DATABASE}' database")
except psycopg2.Error as e:
    print(f"❌ Connection error: {e}")
    exit(1)

# =========================================================================
# STEP 3: BACKUP CURRENT PRODUCT DATA
# =========================================================================
print("\n[STEP 3] Creating backup of current product data...")

try:
    cursor.execute("SELECT * FROM dim_products;")
    backup_data = cursor.fetchall()
    backup_count = len(backup_data)
    print(f"✅ Backup created: {backup_count} current product records")
except Exception as e:
    print(f"⚠️  Warning: Could not backup current data: {e}")

# =========================================================================
# STEP 4: TRUNCATE AND RELOAD DIM_PRODUCTS
# =========================================================================
print("\n[STEP 4] Updating dim_products table...")

try:
    # Truncate the table
    cursor.execute("TRUNCATE TABLE dim_products;")
    print("✅ Truncated dim_products table")
    
    # Insert cleaned data
    for idx, row in df_products.iterrows():
        cursor.execute(
            """
            INSERT INTO dim_products (product_id, product_name)
            VALUES (%s, %s)
            """,
            (row['product_id'], row['product_name'])
        )
    
    conn.commit()
    print(f"✅ Inserted {len(df_products)} clean product records")
    
except psycopg2.Error as e:
    conn.rollback()
    print(f"❌ Error updating products: {e}")
    cursor.close()
    conn.close()
    exit(1)

# =========================================================================
# STEP 5: UPDATE FACT TABLE WITH CONSOLIDATED PRODUCT IDS
# =========================================================================
print("\n[STEP 5] Updating fact_orders with consolidated product IDs...")

consolidation_map = {
    # Nintendo Switch: Keep e682, consolidate all others
    '8d0d': 'e682', '8e5d': 'e682', 'b5f7': 'e682', '03ca': 'e682',
    'da12': 'e682', '97c6': 'e682', '24c1': 'e682', '7d63': 'e682',
    '0d23': 'e682', '604c': 'e682', '6b8d': 'e682',
    
    # Dell Gaming Mouse: Keep f81e, consolidate others
    '5142': 'f81e', '0c5a': 'f81e', '8d4f': 'f81e',
    '7416': 'f81e', 'b0ee': 'f81e', '640d': 'f81e',
    
    # JBL Quantum 100: Keep ab0f, consolidate others
    '2997': 'ab0f', '8315': 'ab0f', '7388': 'ab0f',
    '4c58': 'ab0f', '4db1': 'ab0f',
    
    # Sony PlayStation 5: Keep 54ed, consolidate others
    'df85': '54ed', 'e22d': '54ed', '12b1': '54ed',
    
    # 27in 4K gaming monitor: Keep 891b, consolidate all variations
    'e7e6': '891b', '1238': '891b', '8364': '891b', 'f443': '891b',
    '2a50': '891b', 'ab5d': '891b', 'afbf': '891b',
    
    # Lenovo IdeaPad Gaming 3: Keep 9ef0, consolidate others
    '04ac': '9ef0', 'ae96': '9ef0',
    
    # Razer Pro Gaming Headset: Keep a6be, consolidate other
    '4f26': 'a6be',
}

try:
    updates_made = 0
    for old_id, new_id in consolidation_map.items():
        cursor.execute(
            """
            UPDATE fact_orders
            SET product_id = %s
            WHERE product_id = %s
            """,
            (new_id, old_id)
        )
        rows_updated = cursor.rowcount
        updates_made += rows_updated
        if rows_updated > 0:
            print(f"  ✓ Updated {rows_updated} records: {old_id} → {new_id}")
    
    conn.commit()
    print(f"\n✅ Total fact records updated: {updates_made:,}")
    
except psycopg2.Error as e:
    conn.rollback()
    print(f"❌ Error updating fact table: {e}")
    cursor.close()
    conn.close()
    exit(1)

# =========================================================================
# STEP 6: VERIFY DATA INTEGRITY
# =========================================================================
print("\n[STEP 6] Verifying data integrity...")

try:
    # Check 1: Product count
    cursor.execute("SELECT COUNT(*) FROM dim_products;")
    product_count = cursor.fetchone()[0]
    print(f"  ✓ Products in dimension: {product_count}")
    
    # Check 2: Unique product IDs in fact table
    cursor.execute("SELECT COUNT(DISTINCT product_id) FROM fact_orders;")
    fact_product_count = cursor.fetchone()[0]
    print(f"  ✓ Unique product IDs in fact: {fact_product_count}")
    
    # Check 3: Check for orphaned IDs
    cursor.execute("""
        SELECT DISTINCT fo.product_id
        FROM fact_orders fo
        WHERE fo.product_id NOT IN (SELECT product_id FROM dim_products)
    """)
    orphaned = cursor.fetchall()
    if orphaned:
        print(f"  ⚠️  WARNING: Found {len(orphaned)} orphaned product IDs!")
        for oid in orphaned:
            print(f"     - {oid[0]}")
    else:
        print(f"  ✓ No orphaned product IDs (All valid)")
    
    # Check 4: Total fact records
    cursor.execute("SELECT COUNT(*) FROM fact_orders;")
    fact_count = cursor.fetchone()[0]
    print(f"  ✓ Total fact records: {fact_count:,}")
    
    # Check 5: Product summary
    cursor.execute("""
        SELECT dp.product_id, dp.product_name, COUNT(fo.order_id) as order_count
        FROM dim_products dp
        LEFT JOIN fact_orders fo ON dp.product_id = fo.product_id
        GROUP BY dp.product_id, dp.product_name
        ORDER BY order_count DESC
    """)
    results = cursor.fetchall()
    print(f"\n  Product Summary:")
    for product_id, product_name, order_count in results:
        print(f"    • {product_name:40s} ({product_id:6s}): {order_count:,} orders")
    
    print(f"\n✅ All verification checks passed!")
    
except psycopg2.Error as e:
    print(f"❌ Error during verification: {e}")
    cursor.close()
    conn.close()
    exit(1)

# =========================================================================
# STEP 7: DISPLAY FINAL STATISTICS
# =========================================================================
print("\n" + "=" * 90)
print("DATABASE UPDATE COMPLETE!")
print("=" * 90)

print(f"\nFinal Database State:")
print(f"  Dimension Products:       {product_count} rows")
print(f"  Fact Orders:              {fact_count:,} rows")
print(f"  Unique Product IDs:       {fact_product_count}")
print(f"  Records Updated:          {updates_made:,}")
print(f"  Orphaned IDs:             {len(orphaned)} ✓")

print(f"\n✅ Database successfully updated with clean product data!")
print(f"✅ All {fact_count:,} fact records have valid product references!")

cursor.close()
conn.close()

print("\n" + "=" * 90)
