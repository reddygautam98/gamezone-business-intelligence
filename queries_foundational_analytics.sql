-- =====================================================================
-- GameZone Analytics Database - SQL Query Examples (CORRECTED)
-- =====================================================================
-- Database: gamezone_analytics
-- Use these queries in pgAdmin Query Tool or any PostgreSQL client

-- =====================================================================
-- 1. BASIC DATA OVERVIEW
-- =====================================================================

-- Total Orders and Revenue Summary
SELECT 
    COUNT(DISTINCT f.order_id) as total_orders,
    COUNT(DISTINCT f.customer_id) as unique_customers,
    COUNT(DISTINCT f.product_id) as unique_products,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f;

-- =====================================================================
-- 2. REVENUE ANALYSIS
-- =====================================================================

-- Total Revenue by Country
SELECT 
    f.country_code,
    COUNT(f.order_id) as order_count,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
GROUP BY f.country_code
ORDER BY total_revenue DESC
LIMIT 20;

-- Revenue Trend by Month
SELECT 
    f.order_year_month,
    COUNT(f.order_id) as monthly_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as monthly_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
WHERE f.order_year_month IS NOT NULL AND f.order_year_month != ''
GROUP BY f.order_year_month
ORDER BY f.order_year_month DESC;

-- Revenue by Year
SELECT 
    f.order_year,
    COUNT(f.order_id) as yearly_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as yearly_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
WHERE f.order_year IS NOT NULL AND f.order_year != ''
GROUP BY f.order_year
ORDER BY f.order_year DESC;

-- =====================================================================
-- 3. PRODUCT ANALYSIS
-- =====================================================================

-- Top 10 Best Selling Products by Revenue
SELECT 
    f.product_name,
    f.product_id,
    COUNT(f.order_id) as total_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_price
FROM fact_orders f
GROUP BY f.product_name, f.product_id
ORDER BY total_revenue DESC
LIMIT 10;

-- Top 10 Most Ordered Products (by frequency)
SELECT 
    f.product_name,
    f.product_id,
    COUNT(f.order_id) as order_count,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue
FROM fact_orders f
GROUP BY f.product_name, f.product_id
ORDER BY order_count DESC
LIMIT 10;

-- Product Performance Ranking
SELECT 
    ROW_NUMBER() OVER (ORDER BY SUM(f.order_amount_usd::numeric) DESC) as rank,
    f.product_name,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as product_revenue,
    COUNT(f.order_id) as order_count,
    ROUND(SUM(f.order_amount_usd::numeric) / COUNT(f.order_id), 2) as revenue_per_order
FROM fact_orders f
GROUP BY f.product_name
ORDER BY product_revenue DESC;

-- =====================================================================
-- 4. CUSTOMER ANALYSIS
-- =====================================================================

-- Top 20 Customers by Spending
SELECT 
    f.customer_id,
    f.country_code,
    f.account_creation_method,
    COUNT(f.order_id) as total_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as lifetime_value,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
GROUP BY f.customer_id, f.country_code, f.account_creation_method
ORDER BY lifetime_value DESC
LIMIT 20;

-- Customer Count and Spending by Country
SELECT 
    f.country_code,
    COUNT(DISTINCT f.customer_id) as customer_count,
    COUNT(f.order_id) as total_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    ROUND(SUM(f.order_amount_usd::numeric) / COUNT(DISTINCT f.customer_id), 2) as revenue_per_customer
FROM fact_orders f
GROUP BY f.country_code
ORDER BY total_revenue DESC
LIMIT 20;

-- Customer Segmentation by Order Frequency
SELECT 
    CASE 
        WHEN order_count >= 20 THEN 'Very High (20+)'
        WHEN order_count >= 10 THEN 'High (10-19)'
        WHEN order_count >= 5 THEN 'Medium (5-9)'
        WHEN order_count >= 2 THEN 'Low (2-4)'
        ELSE 'Very Low (1)'
    END as customer_segment,
    COUNT(*) as segment_customer_count,
    ROUND(AVG(lifetime_value), 2) as avg_customer_value,
    ROUND(SUM(lifetime_value), 2) as segment_total_value
FROM (
    SELECT 
        f.customer_id,
        COUNT(f.order_id) as order_count,
        SUM(f.order_amount_usd::numeric) as lifetime_value
    FROM fact_orders f
    GROUP BY f.customer_id
) customer_stats
GROUP BY customer_segment
ORDER BY avg_customer_value DESC;

-- =====================================================================
-- 5. PLATFORM & MARKETING ANALYSIS
-- =====================================================================

-- Revenue by Platform
SELECT 
    f.purchase_platform,
    COUNT(f.order_id) as order_count,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    ROUND((SUM(f.order_amount_usd::numeric) / (SELECT SUM(f2.order_amount_usd::numeric) FROM fact_orders f2) * 100), 2) as revenue_share_pct
FROM fact_orders f
GROUP BY f.purchase_platform
ORDER BY total_revenue DESC;

-- Revenue by Marketing Channel
SELECT 
    f.marketing_channel,
    COUNT(f.order_id) as order_count,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    ROUND((SUM(f.order_amount_usd::numeric) / (SELECT SUM(f2.order_amount_usd::numeric) FROM fact_orders f2) * 100), 2) as revenue_share_pct
FROM fact_orders f
GROUP BY f.marketing_channel
ORDER BY total_revenue DESC;

-- Revenue by Account Creation Method
SELECT 
    f.account_creation_method,
    COUNT(f.order_id) as order_count,
    COUNT(DISTINCT f.customer_id) as customer_count,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
GROUP BY f.account_creation_method
ORDER BY total_revenue DESC;

-- =====================================================================
-- 6. DATE & TIME ANALYSIS
-- =====================================================================

-- Monthly Sales Summary
SELECT 
    f.order_year_month,
    COUNT(f.order_id) as monthly_orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as monthly_revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    COUNT(DISTINCT f.customer_id) as unique_customers
FROM fact_orders f
WHERE f.order_year_month IS NOT NULL AND f.order_year_month != ''
GROUP BY f.order_year_month
ORDER BY f.order_year_month DESC;

-- Monthly Performance Trend
SELECT 
    f.order_year_month,
    COUNT(f.order_id) as orders,
    COUNT(DISTINCT f.customer_id) as customers,
    COUNT(DISTINCT f.product_id) as products,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
WHERE f.order_year_month IS NOT NULL AND f.order_year_month != ''
GROUP BY f.order_year_month
ORDER BY f.order_year_month;

-- =====================================================================
-- 7. BUSINESS METRICS
-- =====================================================================

-- Customer Repeat Purchase Rate
SELECT 
    repeat_status,
    COUNT(*) as customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(DISTINCT customer_id) FROM fact_orders), 2) as percentage
FROM (
    SELECT 
        customer_id,
        CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-Time Buyer' END as repeat_status
    FROM (
        SELECT 
            customer_id,
            COUNT(*) as order_count
        FROM fact_orders
        GROUP BY customer_id
    ) customer_orders
) repeat_analysis
GROUP BY repeat_status;

-- Order Value Distribution
SELECT 
    CASE 
        WHEN f.order_amount_usd::numeric < 50 THEN 'Low ($0-50)'
        WHEN f.order_amount_usd::numeric < 100 THEN 'Medium ($50-100)'
        WHEN f.order_amount_usd::numeric < 250 THEN 'High ($100-250)'
        WHEN f.order_amount_usd::numeric < 500 THEN 'Very High ($250-500)'
        ELSE 'Premium ($500+)'
    END as order_value_range,
    COUNT(*) as order_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM fact_orders), 2) as percentage,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_value
FROM fact_orders f
GROUP BY order_value_range
ORDER BY order_count DESC;

-- =====================================================================
-- 8. DATA QUALITY & COMPLETENESS
-- =====================================================================

-- Check for data completeness
SELECT 
    'fact_orders' as table_name,
    COUNT(*) as total_rows,
    COUNT(CASE WHEN order_id IS NULL OR order_id = '' THEN 1 END) as null_order_ids,
    COUNT(CASE WHEN customer_id IS NULL OR customer_id = '' THEN 1 END) as null_customers,
    COUNT(CASE WHEN product_id IS NULL OR product_id = '' THEN 1 END) as null_products,
    COUNT(CASE WHEN order_amount_usd IS NULL OR order_amount_usd = '' THEN 1 END) as null_amounts,
    COUNT(CASE WHEN country_code IS NULL OR country_code = '' THEN 1 END) as null_country
FROM fact_orders;

-- Check dimension table row counts
SELECT 
    'dim_customer' as table_name, COUNT(*) as row_count FROM dim_customer
UNION ALL
SELECT 'dim_product', COUNT(*) FROM dim_product
UNION ALL
SELECT 'dim_country', COUNT(*) FROM dim_country
UNION ALL
SELECT 'dim_platform', COUNT(*) FROM dim_platform
UNION ALL
SELECT 'dim_marketing_channel', COUNT(*) FROM dim_marketing_channel
UNION ALL
SELECT 'fact_orders', COUNT(*) FROM fact_orders
ORDER BY table_name;

-- =====================================================================
-- 9. COMPREHENSIVE KPI DASHBOARD
-- =====================================================================

-- Comprehensive KPI Summary
SELECT 
    COUNT(DISTINCT order_id) as total_orders,
    COUNT(DISTINCT customer_id) as total_customers,
    COUNT(DISTINCT product_id) as total_products,
    COUNT(DISTINCT country_code) as total_countries,
    ROUND(SUM(order_amount_usd::numeric), 2) as total_revenue,
    ROUND(AVG(order_amount_usd::numeric), 2) as avg_order_value,
    ROUND(MIN(order_amount_usd::numeric), 2) as min_order_value,
    ROUND(MAX(order_amount_usd::numeric), 2) as max_order_value,
    ROUND(SUM(order_amount_usd::numeric) / COUNT(DISTINCT customer_id), 2) as revenue_per_customer
FROM fact_orders;

-- =====================================================================
-- 10. SAMPLE ANALYTICS QUERIES
-- =====================================================================

-- Top Countries by Revenue
SELECT 
    country_code,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(order_id) as orders,
    ROUND(SUM(order_amount_usd::numeric), 2) as revenue,
    ROUND(AVG(order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders
GROUP BY country_code
ORDER BY revenue DESC
LIMIT 15;

-- Platform vs Marketing Channel Performance
SELECT 
    purchase_platform,
    marketing_channel,
    COUNT(order_id) as orders,
    ROUND(SUM(order_amount_usd::numeric), 2) as revenue,
    ROUND(AVG(order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders
GROUP BY purchase_platform, marketing_channel
ORDER BY revenue DESC
LIMIT 15;

-- Account Creation Method Impact
SELECT 
    account_creation_method,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(order_id) as orders,
    ROUND(SUM(order_amount_usd::numeric), 2) as revenue,
    ROUND(SUM(order_amount_usd::numeric) / COUNT(DISTINCT customer_id), 2) as revenue_per_customer
FROM fact_orders
GROUP BY account_creation_method
ORDER BY revenue DESC;

-- =====================================================================
-- END OF CORRECTED QUERIES
-- =====================================================================
