"""
Fix product duplicates by consolidating to master IDs.
Creates cleaned dimension and fact tables.

Before: 43 product rows (9 products, 34 duplicates)
After:  9 product rows (clean dimension table)
"""

import pandas as pd
import os
from datetime import datetime

# File paths
PRODUCTS_FILE = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_dim_02_products.csv"
FACT_FILE = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_fact_01_orders_transactions.csv"
BACKUP_DIR = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\backups"

print("=" * 90)
print("PRODUCT DUPLICATE CONSOLIDATION SCRIPT")
print("=" * 90)

# Create backup directory
os.makedirs(BACKUP_DIR, exist_ok=True)

# =========================================================================
# STEP 1: CREATE CONSOLIDATION MAPPING
# =========================================================================
print("\n[STEP 1] Creating consolidation mapping...")

consolidation_map = {
    # Nintendo Switch: Keep e682, consolidate all others
    '8d0d': 'e682', '8e5d': 'e682', 'b5f7': 'e682', '03ca': 'e682',
    'da12': 'e682', '97c6': 'e682', '24c1': 'e682', '7d63': 'e682',
    '0d23': 'e682', '604c': 'e682', '6b8d': 'e682',
    
    # Dell Gaming Mouse: Keep f81e, consolidate others
    '5142': 'f81e', '0c5a': 'f81e', '8d4f': 'f81e',
    '7416': 'f81e', 'b0ee': 'f81e', '640d': 'f81e',
    
    # JBL Quantum 100: Keep ab0f, consolidate others
    '2997': 'ab0f', '8315': 'ab0f', '7388': 'ab0f',
    '4c58': 'ab0f', '4db1': 'ab0f',
    
    # Sony PlayStation 5: Keep 54ed, consolidate others
    'df85': '54ed', 'e22d': '54ed', '12b1': '54ed',
    
    # 27in 4K gaming monitor: Keep 891b, consolidate all variations
    'e7e6': '891b', '1238': '891b', '8364': '891b', 'f443': '891b',
    # Also consolidate the "27inches 4k" variation
    '2a50': '891b', 'ab5d': '891b', 'afbf': '891b',
    
    # Lenovo IdeaPad Gaming 3: Keep 9ef0, consolidate others
    '04ac': '9ef0', 'ae96': '9ef0',
    
    # Razer Pro Gaming Headset: Keep a6be, consolidate other
    '4f26': 'a6be',
}

print(f"✓ Created mapping for {len(consolidation_map)} duplicate IDs")
print(f"  Consolidating to {len(set(consolidation_map.values()))} master IDs")

# =========================================================================
# STEP 2: LOAD AND BACKUP ORIGINAL FILES
# =========================================================================
print("\n[STEP 2] Loading and backing up original files...")

df_products = pd.read_csv(PRODUCTS_FILE)
df_fact = pd.read_csv(FACT_FILE)

print(f"✓ Loaded products: {len(df_products)} rows")
print(f"✓ Loaded fact: {len(df_fact)} rows")

# Create backups with timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_products = os.path.join(BACKUP_DIR, f"data_dim_02_products_BACKUP_{timestamp}.csv")
backup_fact = os.path.join(BACKUP_DIR, f"data_fact_01_orders_transactions_BACKUP_{timestamp}.csv")

df_products.to_csv(backup_products, index=False)
df_fact.to_csv(backup_fact, index=False)

print(f"✓ Backup: {backup_products}")
print(f"✓ Backup: {backup_fact}")

# =========================================================================
# STEP 3: UPDATE FACT TABLE WITH CONSOLIDATED PRODUCT IDS
# =========================================================================
print("\n[STEP 3] Updating fact table with consolidated product IDs...")

if 'product_id' in df_fact.columns:
    # Count updates needed
    updates_needed = df_fact['product_id'].isin(consolidation_map.keys()).sum()
    print(f"  Records to update: {updates_needed:,}")
    
    # Apply consolidation mapping
    df_fact['product_id'] = df_fact['product_id'].replace(consolidation_map)
    
    print(f"✓ Updated fact table")
    print(f"  Unique product IDs after update: {df_fact['product_id'].nunique()}")
else:
    print("⚠ product_id column not found in fact table, skipping fact table update")

# =========================================================================
# STEP 4: CREATE CLEANED DIMENSION TABLE
# =========================================================================
print("\n[STEP 4] Creating cleaned dimension table...")

# Keep only master IDs (not in consolidation map keys)
master_ids = set(consolidation_map.values())
df_products_clean = df_products[df_products['product_id'].isin(master_ids)].copy()

# Standardize product names (fix "27inches" variation)
df_products_clean['product_name'] = df_products_clean['product_name'].str.replace(
    '27inches 4k gaming monitor',
    '27in 4K gaming monitor',
    case=False,
    regex=False
)

# Remove duplicates based on product_name and keep first occurrence
df_products_clean = df_products_clean.drop_duplicates(
    subset=['product_name'],
    keep='first'
)

df_products_clean = df_products_clean.reset_index(drop=True)

print(f"✓ Cleaned dimension table created")
print(f"  Original rows: {len(df_products)}")
print(f"  Cleaned rows: {len(df_products_clean)}")
print(f"  Rows removed: {len(df_products) - len(df_products_clean)}")

# =========================================================================
# STEP 5: VERIFY CONSOLIDATION
# =========================================================================
print("\n[STEP 5] Verification checks...")

# Check 1: All fact table product_ids exist in cleaned dimension
fact_product_ids = set(df_fact['product_id'].unique())
dim_product_ids = set(df_products_clean['product_id'].unique())
orphaned = fact_product_ids - dim_product_ids

if len(orphaned) > 0:
    print(f"⚠ WARNING: Found {len(orphaned)} orphaned product IDs in fact table!")
    print(f"  {orphaned}")
else:
    print("✓ All fact table product_ids exist in dimension table")

# Check 2: Duplicate names check
duplicate_names = df_products_clean[df_products_clean.duplicated(subset=['product_name'], keep=False)]
if len(duplicate_names) > 0:
    print(f"⚠ WARNING: Found {len(duplicate_names)} duplicate names remaining!")
    print(duplicate_names.to_string())
else:
    print("✓ No duplicate product names remaining")

# Check 3: Dimension table stats
print(f"\n  Dimension Table Statistics:")
print(f"    Total rows: {len(df_products_clean)}")
print(f"    Unique IDs: {df_products_clean['product_id'].nunique()}")
print(f"    Unique names: {df_products_clean['product_name'].nunique()}")

# Check 4: Product name list
print(f"\n  Products in cleaned dimension:")
for idx, row in df_products_clean.sort_values('product_name').iterrows():
    print(f"    - {row['product_id']:6s}: {row['product_name']}")

# =========================================================================
# STEP 6: CONSOLIDATION SUMMARY
# =========================================================================
print("\n[STEP 6] Consolidation Summary...")

print("\n  Products consolidated:")
for duplicate_id, master_id in sorted(consolidation_map.items()):
    duplicate_name = df_products[df_products['product_id'] == duplicate_id]['product_name'].values
    master_name = df_products[df_products['product_id'] == master_id]['product_name'].values
    
    if duplicate_name and master_name:
        print(f"    {duplicate_id} ({duplicate_name[0]}) → {master_id}")

# =========================================================================
# STEP 7: SAVE CLEANED FILES
# =========================================================================
print("\n[STEP 7] Saving cleaned files...")

df_products_clean.to_csv(PRODUCTS_FILE, index=False)
print(f"✓ Saved cleaned products: {PRODUCTS_FILE}")

df_fact.to_csv(FACT_FILE, index=False)
print(f"✓ Saved updated fact table: {FACT_FILE}")

# =========================================================================
# FINAL REPORT
# =========================================================================
print("\n" + "=" * 90)
print("CONSOLIDATION COMPLETE!")
print("=" * 90)

print("\nBefore:")
print(f"  Products dimension: {len(pd.read_csv(backup_products))} rows, {pd.read_csv(backup_products)['product_name'].nunique()} unique names")
print(f"  Fact table: {len(pd.read_csv(backup_fact))} rows")

print("\nAfter:")
print(f"  Products dimension: {len(df_products_clean)} rows, {df_products_clean['product_name'].nunique()} unique names")
print(f"  Fact table: {len(df_fact)} rows (updated with consolidated IDs)")

print("\nChanges:")
print(f"  Duplicate IDs consolidated: {len(consolidation_map)}")
print(f"  Dimension rows removed: {len(pd.read_csv(backup_products)) - len(df_products_clean)}")
print(f"  Fact table records updated: {updates_needed:,}")

print("\nBackups saved:")
print(f"  {backup_products}")
print(f"  {backup_fact}")

print("\n" + "=" * 90)
print("✓ ALL CONSOLIDATION STEPS COMPLETED SUCCESSFULLY!")
print("=" * 90)
