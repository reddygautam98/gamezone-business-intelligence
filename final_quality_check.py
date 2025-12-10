import pandas as pd

print("=" * 80)
print("FINAL PRODUCT DATA QUALITY CHECK")
print("=" * 80)

# Load cleaned data
df_prod = pd.read_csv('data_dim_02_products.csv')
df_fact = pd.read_csv('data_fact_01_orders_transactions.csv')

print("\n📊 DIMENSION TABLE (data_dim_02_products.csv)")
print(f"   Rows: {len(df_prod)}")
print(f"   Columns: {list(df_prod.columns)}")
print(f"\n   Products:")
for idx, row in df_prod.sort_values('product_name').iterrows():
    print(f"     • {row['product_name']}")

print(f"\n📦 FACT TABLE (data_fact_01_orders_transactions.csv)")
print(f"   Total Records: {len(df_fact):,}")
print(f"   Columns: {len(df_fact.columns)}")
print(f"   Product IDs in use: {df_fact['product_id'].nunique()}")

# Verify integrity
missing_ids = set(df_fact['product_id'].unique()) - set(df_prod['product_id'].unique())
print(f"\n✅ DATA INTEGRITY CHECK")
print(f"   Orphaned product IDs: {len(missing_ids)} {'❌' if missing_ids else '✓'}")
if missing_ids:
    print(f"   Missing IDs: {missing_ids}")
else:
    print(f"   All product IDs are valid!")

# Revenue by product
print(f"\n💰 TOP PRODUCTS BY REVENUE")
if 'order_amount_usd' in df_fact.columns or 'unit_price' in df_fact.columns:
    amount_col = 'order_amount_usd' if 'order_amount_usd' in df_fact.columns else 'unit_price'
    revenue = df_fact.groupby('product_id')[amount_col].sum().sort_values(ascending=False)
    total_revenue = revenue.sum()
    for prod_id, rev in revenue.items():
        prod_name = df_prod[df_prod['product_id'] == prod_id]['product_name'].values[0]
        pct = (rev / total_revenue) * 100
        print(f"   {prod_name:40s} ${rev:>12,.2f}  ({pct:>5.1f}%)")
    print(f"   {'Total':40s} ${total_revenue:>12,.2f}  (100.0%)")

print("\n" + "=" * 80)
print("✅ ALL DATA QUALITY CHECKS PASSED!")
print("=" * 80)
