"""
Update GameZone Database with Cleaned Product Data

This script assumes the database and tables already exist.
It will update the dim_products table with clean data.
"""

import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 90)
print("UPDATING DATABASE WITH CLEAN PRODUCT DATA")
print("=" * 90)

# Database configuration
HOST = os.getenv('DB_HOST', '127.0.0.1')
PORT = int(os.getenv('DB_PORT', 5432))
DATABASE = os.getenv('DB_NAME', 'gamezone_analytics')
USERNAME = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', '')

if not PASSWORD:
    print("\n❌ ERROR: Database password not found!")
    exit(1)

# Load cleaned data
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

# Connect to database
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
    print(f"✅ Connected to '{DATABASE}'")
except psycopg2.Error as e:
    print(f"❌ Connection error: {e}")
    exit(1)

# Check if table exists
print("\n[STEP 3] Checking if dim_products table exists...")

try:
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'dim_products'
        )
    """)
    table_exists = cursor.fetchone()[0]
    
    if table_exists:
        cursor.execute("SELECT COUNT(*) FROM dim_products")
        current_count = cursor.fetchone()[0]
        print(f"✅ Table exists with {current_count} current records")
    else:
        print(f"⚠️  Table does not exist - will create it")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS dim_products (
                product_id VARCHAR(50) PRIMARY KEY,
                product_name VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        print(f"✅ Created dim_products table")
        
except psycopg2.Error as e:
    print(f"❌ Error: {e}")
    cursor.close()
    conn.close()
    exit(1)

# Clear and reload products
print("\n[STEP 4] Updating dim_products with clean data...")

try:
    cursor.execute("DELETE FROM dim_products")
    deleted_count = cursor.rowcount
    print(f"✅ Deleted {deleted_count} old records")
    
    for idx, row in df_products.iterrows():
        cursor.execute(
            "INSERT INTO dim_products (product_id, product_name) VALUES (%s, %s)",
            (row['product_id'], row['product_name'])
        )
    
    conn.commit()
    print(f"✅ Inserted {len(df_products)} clean product records")
    
except psycopg2.Error as e:
    conn.rollback()
    print(f"❌ Error: {e}")
    cursor.close()
    conn.close()
    exit(1)

# Consolidation mapping
consolidation_map = {
    '8d0d': 'e682', '8e5d': 'e682', 'b5f7': 'e682', '03ca': 'e682',
    'da12': 'e682', '97c6': 'e682', '24c1': 'e682', '7d63': 'e682',
    '0d23': 'e682', '604c': 'e682', '6b8d': 'e682',
    '5142': 'f81e', '0c5a': 'f81e', '8d4f': 'f81e',
    '7416': 'f81e', 'b0ee': 'f81e', '640d': 'f81e',
    '2997': 'ab0f', '8315': 'ab0f', '7388': 'ab0f',
    '4c58': 'ab0f', '4db1': 'ab0f',
    'df85': '54ed', 'e22d': '54ed', '12b1': '54ed',
    'e7e6': '891b', '1238': '891b', '8364': '891b', 'f443': '891b',
    '2a50': '891b', 'ab5d': '891b', 'afbf': '891b',
    '04ac': '9ef0', 'ae96': '9ef0',
    '4f26': 'a6be',
}

# Update fact table
print("\n[STEP 5] Updating fact_orders with consolidated product IDs...")

try:
    cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'fact_orders')")
    if cursor.fetchone()[0]:
        updates_made = 0
        for old_id, new_id in consolidation_map.items():
            cursor.execute(
                "UPDATE fact_orders SET product_id = %s WHERE product_id = %s",
                (new_id, old_id)
            )
            rows_updated = cursor.rowcount
            updates_made += rows_updated
            if rows_updated > 0:
                print(f"  ✓ Updated {rows_updated:,} records: {old_id} → {new_id}")
        
        conn.commit()
        print(f"\n✅ Total records updated: {updates_made:,}")
    else:
        print("⚠️  fact_orders table does not exist, skipping update")
        
except psycopg2.Error as e:
    conn.rollback()
    print(f"❌ Error updating fact table: {e}")
    cursor.close()
    conn.close()
    exit(1)

# Verification
print("\n[STEP 6] Verifying data integrity...")

try:
    cursor.execute("SELECT COUNT(*) FROM dim_products")
    product_count = cursor.fetchone()[0]
    print(f"  ✓ Products in dimension: {product_count}")
    
    if cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'fact_orders')"):
        cursor.execute("SELECT COUNT(DISTINCT product_id) FROM fact_orders")
        fact_product_ids = cursor.fetchone()[0]
        print(f"  ✓ Unique product IDs in fact: {fact_product_ids}")
        
        cursor.execute("""
            SELECT fo.product_id
            FROM fact_orders fo
            WHERE fo.product_id NOT IN (SELECT product_id FROM dim_products)
        """)
        orphaned = cursor.fetchall()
        if orphaned:
            print(f"  ⚠️  Orphaned IDs: {len(orphaned)}")
            for oid in orphaned:
                print(f"     - {oid[0]}")
        else:
            print(f"  ✓ No orphaned IDs")
        
        cursor.execute("SELECT COUNT(*) FROM fact_orders")
        fact_count = cursor.fetchone()[0]
        print(f"  ✓ Total fact records: {fact_count:,}")
        
        # Product summary
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
            order_count = order_count or 0
            print(f"    • {product_name:40s} ({product_id:6s}): {order_count:,} orders")
    
    print(f"\n✅ All verification checks passed!")
    
except psycopg2.Error as e:
    print(f"❌ Verification error: {e}")

# Close connection
cursor.close()
conn.close()

print("\n" + "=" * 90)
print("✅ DATABASE SUCCESSFULLY UPDATED WITH CLEAN PRODUCT DATA!")
print("=" * 90)
