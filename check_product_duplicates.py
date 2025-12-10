"""
Analyze product duplicates in the data_dim_02_products.csv file
"""

import pandas as pd
import sys

# Load the products data
products_file = r"C:\Users\reddy\Downloads\gamezone-business-intelligence\data_dim_02_products.csv"

print("=" * 80)
print("PRODUCT DUPLICATE ANALYSIS")
print("=" * 80)

try:
    df = pd.read_csv(products_file)
    print(f"\n✓ Loaded {products_file}")
    print(f"  Total rows: {len(df):,}")
    print(f"  Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Error loading file: {e}")
    sys.exit(1)

# =========================================================================
# 1. DUPLICATE PRODUCT IDs
# =========================================================================
print("\n" + "=" * 80)
print("1. DUPLICATE PRODUCT IDs (same ID, possibly different names)")
print("=" * 80)

duplicate_ids = df[df.duplicated(subset=['product_id'], keep=False)].sort_values('product_id')

if len(duplicate_ids) == 0:
    print("✓ No duplicate product IDs found")
else:
    print(f"✗ Found {len(duplicate_ids)} rows with duplicate IDs:\n")
    for product_id in duplicate_ids['product_id'].unique():
        products = duplicate_ids[duplicate_ids['product_id'] == product_id]
        print(f"  Product ID: {product_id}")
        print(f"  Occurrences: {len(products)}")
        print(f"  Names: {products['product_name'].unique().tolist()}")
        print()

# =========================================================================
# 2. DUPLICATE PRODUCT NAMES
# =========================================================================
print("\n" + "=" * 80)
print("2. DUPLICATE PRODUCT NAMES (same name, different IDs)")
print("=" * 80)

duplicate_names = df[df.duplicated(subset=['product_name'], keep=False)].sort_values('product_name')

if len(duplicate_names) == 0:
    print("✓ No duplicate product names found")
else:
    print(f"✗ Found {len(duplicate_names)} rows with duplicate names:\n")
    for product_name in duplicate_names['product_name'].unique():
        products = duplicate_names[duplicate_names['product_name'] == product_name]
        print(f"  Product Name: {product_name}")
        print(f"  Occurrences: {len(products)}")
        print(f"  IDs: {products['product_id'].unique().tolist()}")
        print()

# =========================================================================
# 3. NAMING INCONSISTENCIES
# =========================================================================
print("\n" + "=" * 80)
print("3. PRODUCT NAME VARIATIONS (case/spacing inconsistencies)")
print("=" * 80)

# Normalize names and check for near-duplicates
df['normalized_name'] = df['product_name'].str.lower().str.strip()
duplicates_by_normalized = df[df.duplicated(subset=['normalized_name'], keep=False)].sort_values('normalized_name')

if len(duplicates_by_normalized) == 0:
    print("✓ No product name variations found")
else:
    print(f"✗ Found {len(duplicates_by_normalized)} rows with name variations:\n")
    for normalized_name in duplicates_by_normalized['normalized_name'].unique():
        products = duplicates_by_normalized[duplicates_by_normalized['normalized_name'] == normalized_name]
        print(f"  Normalized Name: '{normalized_name}'")
        print(f"  Variations found: {products['product_name'].unique().tolist()}")
        print(f"  Product IDs: {products['product_id'].unique().tolist()}")
        print()

# =========================================================================
# 4. SUMMARY STATISTICS
# =========================================================================
print("\n" + "=" * 80)
print("4. SUMMARY STATISTICS")
print("=" * 80)

unique_ids = df['product_id'].nunique()
unique_names = df['product_name'].nunique()
unique_normalized = df['normalized_name'].nunique()

print(f"  Total rows:                    {len(df):,}")
print(f"  Unique Product IDs:            {unique_ids:,}")
print(f"  Unique Product Names:          {unique_names:,}")
print(f"  Unique (normalized) Names:     {unique_normalized:,}")
print(f"  Duplicate rows (by ID):        {len(duplicate_ids):,}")
print(f"  Duplicate rows (by name):      {len(duplicate_names):,}")
print(f"  Duplicate rows (normalized):   {len(duplicates_by_normalized):,}")

# =========================================================================
# 5. RECOMMENDATIONS
# =========================================================================
print("\n" + "=" * 80)
print("5. RECOMMENDATIONS")
print("=" * 80)

if len(duplicate_ids) > 0:
    print("⚠️  ACTION REQUIRED: Duplicate Product IDs detected")
    print("    → Same product_id should have ONLY ONE product_name")
    print("    → Need to consolidate or fix product_id mappings\n")

if len(duplicate_names) > 0:
    print("⚠️  ACTION REQUIRED: Duplicate Product Names with different IDs")
    print("    → Same product should have ONE product_id")
    print("    → Consider consolidating under single ID\n")

if len(duplicates_by_normalized) > 0 and len(duplicates_by_normalized) > len(duplicate_names):
    print("⚠️  ACTION REQUIRED: Product name variations detected")
    print("    → Standardize product name format (capitalization, spacing)")
    print("    → Examples: '27in 4K gaming monitor' vs '27inches 4k gaming monitor'\n")

# =========================================================================
# 6. DETAILED DUPLICATE REPORT
# =========================================================================
print("\n" + "=" * 80)
print("6. DETAILED DUPLICATE PRODUCTS TABLE")
print("=" * 80)

print("\nALL DUPLICATE ENTRIES (sorted by product_name then product_id):\n")
all_duplicates = df[df.duplicated(subset=['product_id', 'product_name'], keep=False) | 
                      df.duplicated(subset=['product_name'], keep=False)].sort_values(['product_name', 'product_id'])

if len(all_duplicates) > 0:
    print(all_duplicates.to_string(index=False))
else:
    print("No duplicates found in this combined check")

print("\n" + "=" * 80)
print("END OF REPORT")
print("=" * 80)
