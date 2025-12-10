"""
Fix the orphaned product ID (22ea - Acer Nitro V Gaming Laptop)
This product wasn't a duplicate but got removed in the consolidation process.
"""

import pandas as pd

print("=" * 80)
print("FIXING ORPHANED PRODUCT ID")
print("=" * 80)

# Load files
df_products = pd.read_csv(r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_dim_02_products.csv")
df_fact = pd.read_csv(r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_fact_01_orders_transactions.csv")

print(f"\nBefore:")
print(f"  Products dimension: {len(df_products)} rows")
print(f"  Product IDs: {sorted(df_products['product_id'].unique().tolist())}")

# Find Acer Nitro in the backup
backup_file = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\backups\data_dim_02_products_BACKUP_20251210_131650.csv"
df_backup = pd.read_csv(backup_file)

acer = df_backup[df_backup['product_name'] == 'Acer Nitro V Gaming Laptop']
print(f"\nAcer Nitro in backup:")
print(acer.to_string())

# Add Acer Nitro back to cleaned products
if len(acer) > 0:
    df_products = pd.concat([df_products, acer[['product_id', 'product_name']]], ignore_index=True)
    df_products = df_products.drop_duplicates(subset=['product_id'], keep='first')
    df_products = df_products.reset_index(drop=True)

print(f"\nAfter:")
print(f"  Products dimension: {len(df_products)} rows")
print(f"  Product IDs: {sorted(df_products['product_id'].unique().tolist())}")
print(f"\nAll products:")
for idx, row in df_products.sort_values('product_name').iterrows():
    print(f"  {row['product_id']:6s}: {row['product_name']}")

# Verify all fact table product_ids now exist
fact_ids = set(df_fact['product_id'].unique())
dim_ids = set(df_products['product_id'].unique())
orphaned = fact_ids - dim_ids

print(f"\nVerification:")
print(f"  Fact table product_ids: {len(fact_ids)}")
print(f"  Dimension product_ids: {len(dim_ids)}")
print(f"  Orphaned IDs: {orphaned if orphaned else 'NONE ✓'}")

# Save
df_products.to_csv(r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_dim_02_products.csv", index=False)
print(f"\n✓ Saved corrected products dimension")
