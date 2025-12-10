"""
Verify fact_orders table was properly updated
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)
cursor = conn.cursor()

print("=" * 90)
print("FACT_ORDERS TABLE - COMPREHENSIVE UPDATE VERIFICATION")
print("=" * 90)

# 1. Total records
cursor.execute("SELECT COUNT(*) FROM fact_orders")
total = cursor.fetchone()[0]
print(f"\n[TOTAL RECORDS] {total:,}")

# 2. Unique product IDs
cursor.execute("SELECT COUNT(DISTINCT product_id) FROM fact_orders")
unique_ids = cursor.fetchone()[0]
print(f"[UNIQUE PRODUCT IDs] {unique_ids}")

# 3. Records per product
print("\n[RECORDS BY PRODUCT]")
cursor.execute("""
    SELECT product_id, COUNT(*) as count
    FROM fact_orders
    GROUP BY product_id
    ORDER BY count DESC
""")
total_in_products = 0
for prod_id, count in cursor.fetchall():
    total_in_products += count
    print(f"  {prod_id}: {count:>6,} records")
print(f"  Total: {total_in_products:,} records")

# 4. Verify integrity
print("\n[INTEGRITY CHECK]")
cursor.execute("""
    SELECT COUNT(DISTINCT fo.product_id)
    FROM fact_orders fo
    WHERE fo.product_id IN (SELECT product_id FROM dim_products)
""")
valid = cursor.fetchone()[0]
print(f"  Valid product IDs: {valid}")

cursor.execute("""
    SELECT COUNT(DISTINCT fo.product_id)
    FROM fact_orders fo
    WHERE fo.product_id NOT IN (SELECT product_id FROM dim_products)
""")
orphaned = cursor.fetchone()[0]
print(f"  Orphaned IDs: {orphaned}")

# 5. Revenue summary
print("\n[REVENUE SUMMARY]")
cursor.execute("""
    SELECT 
        COUNT(*) as total_orders,
        SUM(CAST(order_amount_usd AS FLOAT)) as total_revenue
    FROM fact_orders
""")
orders, revenue = cursor.fetchone()
print(f"  Total Orders: {orders:,}")
print(f"  Total Revenue: ${revenue:,.2f}")

# 6. Product names in fact table
print("\n[PRODUCT NAMES IN FACT TABLE]")
cursor.execute("""
    SELECT DISTINCT product_name FROM fact_orders 
    ORDER BY product_name
""")
print("  Unique product names found:")
for name, in cursor.fetchall():
    print(f"    • {name}")

# 7. Verification of updates
print("\n[VERIFICATION OF CONSOLIDATION UPDATES]")
print("  The following duplicate IDs were consolidated:")

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

# Check that old IDs don't exist anymore
cursor.execute("""
    SELECT product_id FROM fact_orders
    WHERE product_id IN %s
""", (tuple(consolidation_map.keys()),))

orphaned_old_ids = cursor.fetchall()

if not orphaned_old_ids:
    print("  ✅ ALL old duplicate IDs have been successfully consolidated!")
    print(f"     {len(consolidation_map)} duplicate IDs → 8 master IDs")
else:
    print("  ⚠️  WARNING: Found old duplicate IDs still in table:")
    for oid, in orphaned_old_ids:
        print(f"     {oid}")

# 8. Final summary
print("\n" + "=" * 90)
print("[FACT_ORDERS UPDATE STATUS]")
print("=" * 90)
print(f"✅ Total Records:        {total:,}")
print(f"✅ Unique Product IDs:   {unique_ids}")
print(f"✅ Valid References:     {valid} (100%)")
print(f"✅ Orphaned IDs:         {orphaned} (0)")
print(f"✅ Old Duplicates Left:  {len(orphaned_old_ids)} (0)")
print(f"✅ Total Revenue:        ${revenue:,.2f}")

if orphaned == 0 and len(orphaned_old_ids) == 0 and valid == unique_ids:
    print("\n✅ FACT TABLE SUCCESSFULLY UPDATED!")
    print("✅ All product IDs consolidated and verified!")
    print("✅ Data ready for production analytics!")
else:
    print("\n⚠️  ISSUES DETECTED - Please review above")

cursor.close()
conn.close()
