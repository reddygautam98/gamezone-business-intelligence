#!/usr/bin/env python3
"""
Comprehensive Database Update Script
Updates all dimension and fact tables with latest data from CSV files
"""

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

def connect_db():
    """Connect to PostgreSQL database"""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        raise

def update_products(conn):
    """Update dim_products table"""
    print("\n[PRODUCTS] Loading data...")
    try:
        df = pd.read_csv('data_dim_02_products.csv')
        print(f"  ✓ Loaded {len(df)} products")
        
        cursor = conn.cursor()
        
        # Clear existing products
        cursor.execute("DELETE FROM dim_products;")
        print(f"  ✓ Cleared existing products")
        
        # Insert new products
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO dim_products (product_id, product_name) VALUES (%s, %s)",
                (row['product_id'], row['product_name'])
            )
        
        conn.commit()
        print(f"  ✓ Inserted {len(df)} products")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_products;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Verification: {count} products in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating products: {e}")
        raise

def update_customers(conn):
    """Update dim_customer table"""
    print("\n[CUSTOMERS] Loading data...")
    try:
        df = pd.read_csv('data_dim_01_customers.csv')
        
        # Truncate customer_id to 50 characters (database column limit)
        df['customer_id'] = df['customer_id'].astype(str).str[:50]
        
        # Remove duplicates (keep first occurrence)
        df = df.drop_duplicates(subset=['customer_id'], keep='first')
        
        print(f"  ✓ Loaded {len(df)} customers (after deduplication)")
        
        cursor = conn.cursor()
        
        # Clear existing customers
        cursor.execute("DELETE FROM dim_customer;")
        print(f"  ✓ Cleared existing customers")
        
        # Insert new customers
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO dim_customer (customer_id, country_code, account_creation_method) VALUES (%s, %s, %s)",
                (row['customer_id'], row['country_code'], row['account_creation_method'])
            )
        
        conn.commit()
        print(f"  ✓ Inserted {len(df)} customers")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_customer;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Verification: {count} customers in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating customers: {e}")
        raise

def update_dates(conn):
    """Update dim_date table"""
    print("\n[DATES] Loading data...")
    try:
        df = pd.read_csv('data_dim_03_dates.csv')
        
        # Remove duplicates (keep first occurrence)
        df = df.drop_duplicates(subset=['date_key'], keep='first')
        
        print(f"  ✓ Loaded {len(df)} dates (after deduplication)")
        
        cursor = conn.cursor()
        
        # Clear existing dates
        cursor.execute("DELETE FROM dim_date;")
        print(f"  ✓ Cleared existing dates")
        
        # Insert new dates
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO dim_date (date_key, order_date, order_year, order_month, order_month_name, order_year_month) VALUES (%s, %s, %s, %s, %s, %s)",
                (row['date_key'], row['order_date'], row['order_year'], row['order_month'], row['order_month_name'], row['order_year_month'])
            )
        
        conn.commit()
        print(f"  ✓ Inserted {len(df)} dates")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_date;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Verification: {count} dates in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating dates: {e}")
        raise

def update_countries(conn):
    """Update dim_country table"""
    print("\n[COUNTRIES] Loading data...")
    try:
        df = pd.read_csv('data_dim_04_countries.csv')
        print(f"  ✓ Loaded {len(df)} countries")
        
        cursor = conn.cursor()
        
        # Clear existing countries
        cursor.execute("DELETE FROM dim_country;")
        print(f"  ✓ Cleared existing countries")
        
        # Insert new countries
        for _, row in df.iterrows():
            country_code = row['country_code'] if pd.notna(row['country_code']) and row['country_code'].strip() else None
            if country_code:
                cursor.execute(
                    "INSERT INTO dim_country (country_code) VALUES (%s)",
                    (country_code,)
                )
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_country;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Inserted and verified: {count} countries in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating countries: {e}")
        raise

def update_platforms(conn):
    """Update dim_platform table"""
    print("\n[PLATFORMS] Loading data...")
    try:
        df = pd.read_csv('data_dim_05_platforms.csv')
        print(f"  ✓ Loaded {len(df)} platforms")
        
        cursor = conn.cursor()
        
        # Clear existing platforms
        cursor.execute("DELETE FROM dim_platform;")
        print(f"  ✓ Cleared existing platforms")
        
        # Insert new platforms
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO dim_platform (platform) VALUES (%s)",
                (row['platform'],)
            )
        
        conn.commit()
        print(f"  ✓ Inserted {len(df)} platforms")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_platform;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Verification: {count} platforms in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating platforms: {e}")
        raise

def update_marketing_channels(conn):
    """Update dim_marketing_channel table"""
    print("\n[MARKETING CHANNELS] Loading data...")
    try:
        df = pd.read_csv('data_dim_06_marketing_channels.csv')
        print(f"  ✓ Loaded {len(df)} marketing channels")
        
        cursor = conn.cursor()
        
        # Clear existing channels
        cursor.execute("DELETE FROM dim_marketing_channel;")
        print(f"  ✓ Cleared existing channels")
        
        # Insert new channels
        for _, row in df.iterrows():
            channel = row['marketing_channel'] if pd.notna(row['marketing_channel']) and row['marketing_channel'].strip() else None
            if channel:
                cursor.execute(
                    "INSERT INTO dim_marketing_channel (marketing_channel) VALUES (%s)",
                    (channel,)
                )
        
        conn.commit()
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM dim_marketing_channel;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Inserted and verified: {count} marketing channels in database")
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating marketing channels: {e}")
        raise

def update_fact_orders(conn):
    """Update fact_orders table"""
    print("\n[FACT ORDERS] Loading data...")
    try:
        df = pd.read_csv('data_fact_01_orders_transactions.csv')
        print(f"  ✓ Loaded {len(df)} order records")
        
        cursor = conn.cursor()
        
        # Clear existing orders
        cursor.execute("DELETE FROM fact_orders;")
        print(f"  ✓ Cleared existing orders")
        
        # Insert new orders
        for _, row in df.iterrows():
            cursor.execute(
                """INSERT INTO fact_orders 
                   (customer_id, order_id, order_date, ship_ts, product_name, product_id, 
                    order_amount_usd, purchase_platform, marketing_channel, 
                    account_creation_method, country_code, order_year, order_month, 
                    order_month_name, order_year_month, date_key)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (row['customer_id'], row['order_id'], row['order_date'], row['ship_ts'],
                 row['product_name'], row['product_id'], row['order_amount_usd'],
                 row['purchase_platform'], row['marketing_channel'],
                 row['account_creation_method'], row['country_code'], row['order_year'],
                 row['order_month'], row['order_month_name'], row['order_year_month'],
                 row['date_key'])
            )
        
        conn.commit()
        print(f"  ✓ Inserted {len(df)} order records")
        
        # Verify
        cursor.execute("SELECT COUNT(*) FROM fact_orders;")
        count = cursor.fetchone()[0]
        print(f"  ✓ Verification: {count} orders in database")
        
        # Revenue check (cast to numeric)
        cursor.execute("SELECT SUM(order_amount_usd::numeric) FROM fact_orders;")
        total_revenue = cursor.fetchone()[0]
        if total_revenue:
            print(f"  ✓ Total Revenue: ${total_revenue:,.2f}")
        
        cursor.close()
        
        return count
    except Exception as e:
        conn.rollback()
        print(f"❌ Error updating fact orders: {e}")
        raise

def main():
    """Main update process"""
    print("=" * 70)
    print("📊 GAMEZONE ANALYTICS DATABASE UPDATE")
    print("=" * 70)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Connect to database
        print(f"\n[CONNECTION] Connecting to {DB_HOST}:{DB_PORT}/{DB_NAME}...")
        conn = connect_db()
        print("  ✓ Connected successfully")
        
        # Update all tables
        products_count = update_products(conn)
        customers_count = update_customers(conn)
        dates_count = update_dates(conn)
        countries_count = update_countries(conn)
        platforms_count = update_platforms(conn)
        channels_count = update_marketing_channels(conn)
        orders_count = update_fact_orders(conn)
        
        # Final summary
        print("\n" + "=" * 70)
        print("✅ DATABASE UPDATE COMPLETE")
        print("=" * 70)
        print(f"\nTable Summary:")
        print(f"  • dim_products:          {products_count:>6} records")
        print(f"  • dim_customer:          {customers_count:>6} records")
        print(f"  • dim_date:              {dates_count:>6} records")
        print(f"  • dim_country:           {countries_count:>6} records")
        print(f"  • dim_platform:          {platforms_count:>6} records")
        print(f"  • dim_marketing_channel: {channels_count:>6} records")
        print(f"  • fact_orders:           {orders_count:>6} records")
        print(f"\nTotal Records Loaded: {products_count + customers_count + dates_count + countries_count + platforms_count + channels_count + orders_count:,}")
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        conn.close()
        print("✓ Database connection closed")
        
    except Exception as e:
        print(f"\n❌ Update failed: {e}")
        raise

if __name__ == "__main__":
    main()
