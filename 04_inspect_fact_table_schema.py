"""
Check fact_orders table structure
"""

import psycopg2

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
    
    # Get column names and types
    cursor.execute("""
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = 'fact_orders'
        ORDER BY ordinal_position
    """)
    
    print("fact_orders Table Structure:")
    print("=" * 50)
    columns = cursor.fetchall()
    for i, (col_name, data_type) in enumerate(columns, 1):
        print(f"{i}. {col_name:.<30} {data_type}")
    
    print("\n" + "=" * 50)
    print("Sample Data (first 5 rows):")
    print("=" * 50)
    
    cursor.execute("SELECT * FROM fact_orders LIMIT 5")
    print(cursor.fetchall())
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
