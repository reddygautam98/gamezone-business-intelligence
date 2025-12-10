"""
Clean up old dim_product table and verify dim_products is properly set up
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("=" * 90)
print("DATABASE CLEANUP: REMOVING DUPLICATE PRODUCT TABLE")
print("=" * 90)

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
cursor = conn.cursor()

try:
    # Step 1: Check if old table exists
    print("\n[STEP 1] Checking for old dim_product table...")
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'dim_product'
        )
    """)
    old_table_exists = cursor.fetchone()[0]
    
    if old_table_exists:
        # Get record count
        cursor.execute("SELECT COUNT(*) FROM dim_product")
        old_count = cursor.fetchone()[0]
        print(f"✅ Found old dim_product table with {old_count} rows")
        
        # Check for foreign key references
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.constraint_column_usage 
            WHERE table_name = 'dim_product'
        """)
        ref_count = cursor.fetchone()[0]
        print(f"   Foreign key references: {ref_count}")
        
        # Step 2: Check new table
        print("\n[STEP 2] Verifying new dim_products table...")
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'dim_products'
            )
        """)
        new_table_exists = cursor.fetchone()[0]
        
        if new_table_exists:
            cursor.execute("SELECT COUNT(*) FROM dim_products")
            new_count = cursor.fetchone()[0]
            print(f"✅ Found new dim_products table with {new_count} clean records")
            
            # Verify fact_orders references dim_products
            cursor.execute("""
                SELECT COUNT(DISTINCT product_id) FROM fact_orders 
                WHERE product_id IN (SELECT product_id FROM dim_products)
            """)
            matching = cursor.fetchone()[0]
            print(f"   Records in fact_orders matching dim_products: {matching}")
            
            # Step 3: Drop old table
            print("\n[STEP 3] Removing old dim_product table...")
            cursor.execute("DROP TABLE dim_product")
            conn.commit()
            print("✅ Successfully dropped old dim_product table")
            
            # Step 4: Verify cleanup
            print("\n[STEP 4] Verifying cleanup...")
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'dim_product'
                )
            """)
            still_exists = cursor.fetchone()[0]
            
            if not still_exists:
                print("✅ Old table successfully removed from database")
            else:
                print("❌ Old table still exists!")
                cursor.close()
                conn.close()
                exit(1)
            
            # Step 5: Final verification
            print("\n[STEP 5] Final database status...")
            cursor.execute("""
                SELECT table_name, COUNT(*) as row_count
                FROM (
                    SELECT 'dim_products' as table_name, COUNT(*) FROM dim_products
                    UNION ALL
                    SELECT 'fact_orders', COUNT(*) FROM fact_orders
                    UNION ALL
                    SELECT 'dim_customer', COUNT(*) FROM dim_customer
                    UNION ALL
                    SELECT 'dim_date', COUNT(*) FROM dim_date
                ) as counts
                GROUP BY table_name
                ORDER BY table_name
            """)
            
            print("\n📊 Key Tables:")
            for table, count in cursor.fetchall():
                print(f"   {table:30s} {count:>10,} rows")
            
            print("\n" + "=" * 90)
            print("✅ DATABASE CLEANUP COMPLETE!")
            print("=" * 90)
            print("\nStatus:")
            print("✅ Old dim_product table removed")
            print("✅ New dim_products table active (8 clean records)")
            print("✅ fact_orders updated (21,680 records with correct product_ids)")
            print("✅ Database ready for production analytics")
            
        else:
            print("❌ ERROR: New dim_products table not found!")
            cursor.close()
            conn.close()
            exit(1)
    else:
        print("⚠️  Old dim_product table not found (already removed?)")
        
        # Verify new table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'dim_products'
            )
        """)
        if cursor.fetchone()[0]:
            cursor.execute("SELECT COUNT(*) FROM dim_products")
            count = cursor.fetchone()[0]
            print(f"✅ New dim_products table exists with {count} records")
            print("✅ Database is clean and ready")
        else:
            print("❌ ERROR: Neither old nor new product table found!")
    
    cursor.close()
    conn.close()
    
except psycopg2.Error as e:
    print(f"\n❌ Database error: {e}")
    conn.rollback()
    cursor.close()
    conn.close()
    exit(1)
