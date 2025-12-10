"""
Check all database tables and their status
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
print("DATABASE TABLE STATUS - COMPREHENSIVE CHECK")
print("=" * 90)

# Get all tables
cursor.execute("""
    SELECT table_name FROM information_schema.tables 
    WHERE table_schema = 'public' ORDER BY table_name
""")
tables = [row[0] for row in cursor.fetchall()]

print(f"\nTotal tables in database: {len(tables)}\n")

table_info = []

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table}")
    count = cursor.fetchone()[0]
    
    # Get columns info
    cursor.execute(f"""
        SELECT column_name, data_type FROM information_schema.columns 
        WHERE table_name = '{table}' ORDER BY ordinal_position
    """)
    cols = cursor.fetchall()
    
    table_info.append({
        'name': table,
        'rows': count,
        'columns': len(cols),
        'col_names': [c[0] for c in cols]
    })

# Display table info
for info in sorted(table_info, key=lambda x: x['name']):
    print(f"{'=' * 90}")
    print(f"TABLE: {info['name']:30s} | {info['rows']:>8,} rows | {info['columns']} columns")
    print(f"{'=' * 90}")
    print(f"Columns: {', '.join(info['col_names'][:7])}")
    if len(info['col_names']) > 7:
        print(f"          {', '.join(info['col_names'][7:])}")
    print()

# Summary
print("=" * 90)
print("SUMMARY")
print("=" * 90)

total_rows = sum(info['rows'] for info in table_info)
print(f"Total tables:  {len(table_info)}")
print(f"Total rows:    {total_rows:,}")

# Highlight updated tables
print("\n" + "-" * 90)
print("TABLES UPDATED WITH CLEAN DATA:")
print("-" * 90)

updated_tables = {
    'dim_products': 'Cleaned products (8 records)',
    'fact_orders': 'Updated with consolidated product IDs (9,536 updates)',
}

for table, desc in updated_tables.items():
    for info in table_info:
        if info['name'] == table:
            print(f"✅ {table:30s} {desc:40s} | {info['rows']:>8,} rows")

# Other tables (not updated)
print("\n" + "-" * 90)
print("OTHER TABLES (Not updated in this session):")
print("-" * 90)

updated_names = set(updated_tables.keys())
for info in sorted(table_info, key=lambda x: x['name']):
    if info['name'] not in updated_names:
        print(f"   {info['name']:30s} {info['rows']:>8,} rows")

cursor.close()
conn.close()
