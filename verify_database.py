"""
Final Database Verification Report
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv('DB_HOST', '127.0.0.1')
PORT = int(os.getenv('DB_PORT', 5432))
DATABASE = os.getenv('DB_NAME', 'gamezone_analytics')
USERNAME = os.getenv('DB_USER', 'postgres')
PASSWORD = os.getenv('DB_PASSWORD', '')

print("=" * 90)
print("FINAL DATABASE VERIFICATION REPORT")
print("=" * 90)

try:
    conn = psycopg2.connect(
        host=HOST,
        port=PORT,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )
    cursor = conn.cursor()
    print(f"\n✅ Connected to '{DATABASE}'")
    
    # Get all tables
    cursor.execute("""
        SELECT table_name FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cursor.fetchall()]
    print(f"\n📋 Tables in database: {len(tables)}")
    for table in tables:
        print(f"   • {table}")
    
    # Check dim_products
    print("\n" + "-" * 90)
    print("DIM_PRODUCTS TABLE")
    print("-" * 90)
    
    cursor.execute("SELECT COUNT(*) FROM dim_products")
    product_count = cursor.fetchone()[0]
    print(f"✅ Total products: {product_count}")
    
    cursor.execute("""
        SELECT product_id, product_name FROM dim_products
        ORDER BY product_name
    """)
    print(f"\n📦 Products:")
    for product_id, product_name in cursor.fetchall():
        print(f"   {product_id:6s} | {product_name}")
    
    # Check fact_orders if exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'fact_orders'
        )
    """)
    
    if cursor.fetchone()[0]:
        print("\n" + "-" * 90)
        print("FACT_ORDERS TABLE")
        print("-" * 90)
        
        cursor.execute("SELECT COUNT(*) FROM fact_orders")
        fact_count = cursor.fetchone()[0]
        print(f"✅ Total fact records: {fact_count:,}")
        
        cursor.execute("SELECT COUNT(DISTINCT product_id) FROM fact_orders")
        unique_ids = cursor.fetchone()[0]
        print(f"✅ Unique product IDs: {unique_ids}")
        
        # Check for orphaned IDs
        cursor.execute("""
            SELECT COUNT(DISTINCT fo.product_id)
            FROM fact_orders fo
            WHERE fo.product_id NOT IN (SELECT product_id FROM dim_products)
        """)
        orphaned_count = cursor.fetchone()[0]
        print(f"✅ Orphaned IDs: {orphaned_count} {'❌' if orphaned_count > 0 else '✓'}")
        
        # Product summary with revenue
        print(f"\n💰 Product Summary with Revenue:")
        cursor.execute("""
            SELECT dp.product_id, dp.product_name, 
                   COUNT(DISTINCT fo.order_id) as order_count,
                   COALESCE(SUM(CAST(fo.order_amount_usd AS FLOAT)), 0) as total_revenue
            FROM dim_products dp
            LEFT JOIN fact_orders fo ON dp.product_id = fo.product_id
            GROUP BY dp.product_id, dp.product_name
            ORDER BY total_revenue DESC
        """)
        
        results = cursor.fetchall()
        total_revenue = sum(r[3] or 0 for r in results)
        
        for product_id, product_name, order_count, revenue in results:
            order_count = order_count or 0
            revenue = revenue or 0
            pct = (revenue / total_revenue * 100) if total_revenue > 0 else 0
            print(f"   {product_name:40s} | {order_count:>6,} orders | ${revenue:>15,.2f} ({pct:>5.1f}%)")
        
        print(f"   {'TOTAL':40s} | {'':>6s} | ${total_revenue:>15,.2f} (100.0%)")
    
    print("\n" + "=" * 90)
    print("✅ DATABASE VERIFICATION COMPLETE")
    print("=" * 90)
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"\n❌ Error: {e}")
