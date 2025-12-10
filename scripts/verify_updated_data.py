#!/usr/bin/env python3
"""
Comprehensive Database Verification After Update
"""

import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def verify_database():
    """Verify all database tables and data integrity"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        
        print("=" * 80)
        print("📊 DATABASE VERIFICATION REPORT")
        print("=" * 80)
        
        # Products
        print("\n[PRODUCTS TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_products;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT product_id, product_name FROM dim_products ORDER BY product_id;")
        products = cursor.fetchall()
        for pid, pname in products:
            print(f"    • {pid}: {pname}")
        
        # Customers
        print("\n[CUSTOMERS TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_customer;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT COUNT(DISTINCT country_code) FROM dim_customer;")
        countries = cursor.fetchone()[0]
        print(f"  Unique Countries: {countries}")
        
        cursor.execute("SELECT COUNT(DISTINCT account_creation_method) FROM dim_customer;")
        methods = cursor.fetchone()[0]
        print(f"  Account Creation Methods: {methods}")
        
        # Dates
        print("\n[DATES TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_date;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT MIN(order_date), MAX(order_date) FROM dim_date;")
        min_date, max_date = cursor.fetchone()
        print(f"  Date Range: {min_date} to {max_date}")
        
        # Countries
        print("\n[COUNTRIES TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_country;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        # Platforms
        print("\n[PLATFORMS TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_platform;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT platform FROM dim_platform ORDER BY platform;")
        platforms = cursor.fetchall()
        for (platform,) in platforms:
            print(f"    • {platform}")
        
        # Marketing Channels
        print("\n[MARKETING CHANNELS TABLE]")
        cursor.execute("SELECT COUNT(*) FROM dim_marketing_channel;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT marketing_channel FROM dim_marketing_channel ORDER BY marketing_channel;")
        channels = cursor.fetchall()
        for (channel,) in channels:
            print(f"    • {channel}")
        
        # Fact Orders
        print("\n[FACT ORDERS TABLE]")
        cursor.execute("SELECT COUNT(*) FROM fact_orders;")
        count = cursor.fetchone()[0]
        print(f"  Total Records: {count}")
        
        cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM fact_orders;")
        customers = cursor.fetchone()[0]
        print(f"  Unique Customers: {customers}")
        
        cursor.execute("SELECT COUNT(DISTINCT product_id) FROM fact_orders;")
        products = cursor.fetchone()[0]
        print(f"  Unique Products: {products}")
        
        cursor.execute("SELECT SUM(order_amount_usd::numeric) FROM fact_orders;")
        total_revenue = cursor.fetchone()[0]
        print(f"  Total Revenue: ${total_revenue:,.2f}")
        
        # Product distribution
        print("\n  [PRODUCTS DISTRIBUTION IN ORDERS]")
        cursor.execute("""
            SELECT fo.product_id, dp.product_name, COUNT(*) as order_count
            FROM fact_orders fo
            LEFT JOIN dim_products dp ON fo.product_id = dp.product_id
            GROUP BY fo.product_id, dp.product_name
            ORDER BY order_count DESC;
        """)
        
        products_dist = cursor.fetchall()
        for pid, pname, order_count in products_dist:
            print(f"    • {pid} ({pname}): {order_count:,} orders")
        
        # Referential Integrity Check
        print("\n[REFERENTIAL INTEGRITY CHECK]")
        
        cursor.execute("""
            SELECT COUNT(*) FROM fact_orders fo
            WHERE NOT EXISTS (SELECT 1 FROM dim_products dp WHERE dp.product_id = fo.product_id);
        """)
        orphaned_products = cursor.fetchone()[0]
        print(f"  Orphaned Product IDs: {orphaned_products}")
        
        cursor.execute("""
            SELECT COUNT(*) FROM fact_orders fo
            WHERE NOT EXISTS (SELECT 1 FROM dim_customer dc WHERE dc.customer_id = fo.customer_id);
        """)
        orphaned_customers = cursor.fetchone()[0]
        print(f"  Orphaned Customer IDs: {orphaned_customers}")
        
        cursor.execute("""
            SELECT COUNT(*) FROM fact_orders fo
            WHERE NOT EXISTS (SELECT 1 FROM dim_date dd WHERE dd.date_key::text = fo.date_key::text);
        """)
        orphaned_dates = cursor.fetchone()[0]
        print(f"  Orphaned Date Keys: {orphaned_dates}")
        
        # Summary
        print("\n" + "=" * 80)
        print("✅ VERIFICATION COMPLETE")
        print("=" * 80)
        
        total_records = (
            cursor.execute("SELECT COUNT(*) FROM dim_products;") or 0,
            cursor.execute("SELECT COUNT(*) FROM dim_customer;") or 0,
            cursor.execute("SELECT COUNT(*) FROM dim_date;") or 0,
            cursor.execute("SELECT COUNT(*) FROM dim_country;") or 0,
            cursor.execute("SELECT COUNT(*) FROM dim_platform;") or 0,
            cursor.execute("SELECT COUNT(*) FROM dim_marketing_channel;") or 0,
            cursor.execute("SELECT COUNT(*) FROM fact_orders;") or 0,
        )
        
        cursor.execute("SELECT COUNT(*) FROM dim_products;")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM dim_customer;")
        total += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM dim_date;")
        total += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM dim_country;")
        total += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM dim_platform;")
        total += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM dim_marketing_channel;")
        total += cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM fact_orders;")
        total += cursor.fetchone()[0]
        
        print(f"\nTotal Records in Database: {total:,}")
        
        if orphaned_products == 0 and orphaned_customers == 0 and orphaned_dates == 0:
            print("✅ All referential integrity checks PASSED")
        else:
            print("⚠️  Some referential integrity issues found")
        
        print("=" * 80)
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        raise

if __name__ == "__main__":
    verify_database()
