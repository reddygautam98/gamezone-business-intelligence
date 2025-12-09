"""
Build dimension and fact tables from cleaned GameZone data.

Input:
    gamezone_orders_clean.csv  (output of gamezone.py)

Output:
    dim_date.csv
    dim_customer.csv
    dim_product.csv
    dim_platform.csv
    dim_marketing_channel.csv
    dim_country.csv
    fact_orders.csv
"""

import pandas as pd

INPUT_CLEAN = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\gamezone_orders_clean.csv"

print("=== Building dimension and fact tables from cleaned GameZone data ===")

# -------------------------------------------------------------------
# 1. LOAD CLEAN DATA
# -------------------------------------------------------------------
df = pd.read_csv(INPUT_CLEAN)

print(f"Loaded cleaned data: {df.shape[0]:,} rows, {df.shape[1]} columns")
print("Columns:", list(df.columns))

# Ensure order_date exists
if "order_date" not in df.columns:
    raise ValueError("Column 'order_date' not found in cleaned data.")

# Explicitly convert order_date to datetime here (critical!)
# Try multiple formats and use coerce for errors
df["order_date"] = pd.to_datetime(df["order_date"], format='mixed', errors="coerce")

# Drop rows with invalid dates
df = df.dropna(subset=['order_date'])

print("order_date dtype after to_datetime:", df["order_date"].dtype)
print(f"Rows after date cleanup: {df.shape[0]:,}")

# -------------------------------------------------------------------
# 2. DIM_DATE
# -------------------------------------------------------------------
date_cols = ["order_date", "order_year", "order_month", "order_month_name", "order_year_month"]

missing_date_cols = [c for c in date_cols if c not in df.columns]
if missing_date_cols:
    raise ValueError(f"Missing expected date columns in cleaned data: {missing_date_cols}")

dim_date = (
    df[date_cols]
    .drop_duplicates()
    .reset_index(drop=True)
)

# enforce datetime again on this subset (extra safety)
dim_date["order_date"] = pd.to_datetime(dim_date["order_date"], errors="coerce")

# drop rows where order_date is NaT
dim_date = dim_date.dropna(subset=["order_date"])

# build date_key safely
dim_date["date_key"] = dim_date["order_date"].dt.strftime("%Y%m%d").astype(int)

dim_date = dim_date[
    ["date_key", "order_date", "order_year", "order_month", "order_month_name", "order_year_month"]
]

dim_date.to_csv("dim_date.csv", index=False)
print(f"[dim_date] Saved dim_date.csv → {dim_date.shape[0]:,} rows")

# -------------------------------------------------------------------
# 3. DIM_CUSTOMER
# -------------------------------------------------------------------
customer_cols = [c for c in ["customer_id", "country_code", "account_creation_method"] if c in df.columns]

if customer_cols:
    dim_customer = (
        df[customer_cols]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_customer.to_csv("dim_customer.csv", index=False)
    print(f"[dim_customer] Saved dim_customer.csv → {dim_customer.shape[0]:,} rows")
else:
    print("[dim_customer] No customer-related columns found, skipping.")

# -------------------------------------------------------------------
# 4. DIM_PRODUCT
# -------------------------------------------------------------------
product_cols = [c for c in ["product_id", "product_name"] if c in df.columns]

if product_cols:
    dim_product = (
        df[product_cols]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_product.to_csv("dim_product.csv", index=False)
    print(f"[dim_product] Saved dim_product.csv → {dim_product.shape[0]:,} rows")
else:
    print("[dim_product] No product-related columns found, skipping.")

# -------------------------------------------------------------------
# 5. DIM_PLATFORM
# -------------------------------------------------------------------
if "purchase_platform" in df.columns:
    dim_platform = (
        df[["purchase_platform"]]
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={"purchase_platform": "platform"})
    )
    dim_platform.to_csv("dim_platform.csv", index=False)
    print(f"[dim_platform] Saved dim_platform.csv → {dim_platform.shape[0]:,} rows")
else:
    print("[dim_platform] purchase_platform column not found, skipping.")

# -------------------------------------------------------------------
# 6. DIM_MARKETING_CHANNEL
# -------------------------------------------------------------------
if "marketing_channel" in df.columns:
    dim_marketing_channel = (
        df[["marketing_channel"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_marketing_channel.to_csv("dim_marketing_channel.csv", index=False)
    print(f"[dim_marketing_channel] Saved dim_marketing_channel.csv → {dim_marketing_channel.shape[0]:,} rows")
else:
    print("[dim_marketing_channel] marketing_channel column not found, skipping.")

# -------------------------------------------------------------------
# 7. DIM_COUNTRY
# -------------------------------------------------------------------
if "country_code" in df.columns:
    dim_country = (
        df[["country_code"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim_country.to_csv("dim_country.csv", index=False)
    print(f"[dim_country] Saved dim_country.csv → {dim_country.shape[0]:,} rows")
else:
    print("[dim_country] country_code column not found, skipping.")

# -------------------------------------------------------------------
# 8. FACT_ORDERS
# -------------------------------------------------------------------
fact = df.copy()

# Join date_key from dim_date
fact = fact.merge(
    dim_date[["order_date", "date_key"]],
    on="order_date",
    how="left"
)

# Rename unit_price to order_amount_usd for clarity
if "unit_price" in fact.columns:
    fact = fact.rename(columns={"unit_price": "order_amount_usd"})

fact.to_csv("fact_orders.csv", index=False)
print(f"[fact_orders] Saved fact_orders.csv → {fact.shape[0]:,} rows, {fact.shape[1]} columns")

print("=== Dimension and fact tables generation completed ===")
