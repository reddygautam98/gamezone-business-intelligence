-- =====================================================================
-- GAMEZONE ADVANCED ANALYTICS QUERIES
-- Senior Data Analyst Level
-- =====================================================================

-- =====================================================================
-- 1️⃣ YoY REVENUE GROWTH BY COUNTRY (Latest 2 Years)
-- =====================================================================

SELECT 
    f.country_code,
    f.order_year,
    COUNT(f.order_id) as orders,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue,
    COUNT(DISTINCT f.customer_id) as customers,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value
FROM fact_orders f
WHERE f.order_year IS NOT NULL 
    AND f.order_year != '' 
    AND f.order_year::int >= (EXTRACT(YEAR FROM CURRENT_DATE) - 2)
GROUP BY f.country_code, f.order_year
ORDER BY f.country_code, f.order_year DESC;

-- YoY Growth Rate with Pivot View
WITH yearly_revenue AS (
    SELECT 
        f.country_code,
        f.order_year::int as year,
        ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue
    FROM fact_orders f
    WHERE f.order_year IS NOT NULL AND f.order_year != ''
    GROUP BY f.country_code, f.order_year
)
SELECT 
    yoy_2021.country_code,
    COALESCE(yoy_2020.revenue, 0) as revenue_2020,
    COALESCE(yoy_2021.revenue, 0) as revenue_2021,
    CASE 
        WHEN yoy_2020.revenue = 0 OR yoy_2020.revenue IS NULL THEN NULL
        ELSE ROUND(((yoy_2021.revenue - yoy_2020.revenue) / yoy_2020.revenue * 100), 2)
    END as yoy_growth_pct,
    CASE 
        WHEN yoy_2021.revenue > COALESCE(yoy_2020.revenue, 0) THEN '📈 Growing'
        WHEN yoy_2021.revenue < COALESCE(yoy_2020.revenue, 0) THEN '📉 Declining'
        ELSE '➡️ Flat'
    END as trend
FROM yearly_revenue yoy_2021
LEFT JOIN yearly_revenue yoy_2020 ON yoy_2021.country_code = yoy_2020.country_code 
    AND yoy_2020.year = 2020
WHERE yoy_2021.year = 2021
ORDER BY yoy_growth_pct DESC NULLS LAST;

-- =====================================================================
-- 2️⃣ MARKETING CHANNEL EFFECTIVENESS BY PLATFORM
-- =====================================================================

SELECT 
    f.purchase_platform,
    f.marketing_channel,
    COUNT(f.order_id) as orders,
    COUNT(DISTINCT f.customer_id) as customers,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    ROUND((SUM(f.order_amount_usd::numeric) / (
        SELECT SUM(f2.order_amount_usd::numeric) 
        FROM fact_orders f2 
        WHERE f2.purchase_platform = f.purchase_platform
    ) * 100), 2) as channel_share_pct_on_platform
FROM fact_orders f
WHERE f.marketing_channel IS NOT NULL 
    AND f.marketing_channel != '' 
    AND f.marketing_channel != 'unknown'
    AND f.purchase_platform IS NOT NULL
GROUP BY f.purchase_platform, f.marketing_channel
ORDER BY f.purchase_platform, revenue DESC;

-- Channel Effectiveness Score (ROI-like metric)
SELECT 
    f.marketing_channel,
    COUNT(f.order_id) as orders,
    COUNT(DISTINCT f.customer_id) as customers,
    ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue,
    ROUND(AVG(f.order_amount_usd::numeric), 2) as avg_order_value,
    ROUND(SUM(f.order_amount_usd::numeric) / COUNT(DISTINCT f.customer_id), 2) as revenue_per_customer,
    ROUND(COUNT(f.order_id)::numeric / COUNT(DISTINCT f.customer_id), 2) as orders_per_customer,
    ROUND((SUM(f.order_amount_usd::numeric) / (SELECT SUM(f2.order_amount_usd::numeric) FROM fact_orders f2) * 100), 2) as total_revenue_share_pct
FROM fact_orders f
WHERE f.marketing_channel IS NOT NULL 
    AND f.marketing_channel != '' 
    AND f.marketing_channel != 'unknown'
GROUP BY f.marketing_channel
ORDER BY revenue DESC;

-- =====================================================================
-- 3️⃣ TOP 10 PRODUCTS: LATEST YEAR VS PREVIOUS YEAR (WITH GROWTH)
-- =====================================================================

WITH product_yearly_revenue AS (
    SELECT 
        f.product_name,
        f.product_id,
        f.order_year::int as year,
        COUNT(f.order_id) as orders,
        ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue
    FROM fact_orders f
    WHERE f.order_year IS NOT NULL AND f.order_year != ''
    GROUP BY f.product_name, f.product_id, f.order_year
),
latest_year_top10 AS (
    SELECT 
        product_name,
        product_id,
        year,
        orders,
        revenue,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) as rank
    FROM product_yearly_revenue
    WHERE year = (SELECT MAX(year) FROM product_yearly_revenue)
)
SELECT 
    latest.rank,
    latest.product_name,
    latest.year as latest_year,
    latest.orders as latest_orders,
    latest.revenue as latest_revenue,
    COALESCE(prior.orders, 0) as prior_year_orders,
    COALESCE(prior.revenue, 0) as prior_year_revenue,
    CASE 
        WHEN prior.revenue = 0 OR prior.revenue IS NULL THEN NULL
        ELSE ROUND(((latest.revenue - COALESCE(prior.revenue, 0)) / COALESCE(prior.revenue, 1) * 100), 2)
    END as yoy_growth_pct,
    CASE 
        WHEN latest.revenue > COALESCE(prior.revenue, 0) THEN '📈'
        WHEN latest.revenue < COALESCE(prior.revenue, 0) THEN '📉'
        ELSE '➡️'
    END as trend
FROM latest_year_top10 latest
LEFT JOIN product_yearly_revenue prior ON latest.product_id = prior.product_id 
    AND prior.year = latest.year - 1
WHERE latest.rank <= 10
ORDER BY latest.rank;

-- =====================================================================
-- 4️⃣ NEW vs REPEAT CUSTOMERS BY MONTH
-- =====================================================================

WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        MIN(f.order_date) as first_purchase_date
    FROM fact_orders f
    WHERE f.order_date IS NOT NULL
    GROUP BY customer_id
),
monthly_customers AS (
    SELECT 
        f.order_year_month,
        f.customer_id,
        CASE 
            WHEN cf.first_purchase_date::date = f.order_date::date THEN 'New'
            ELSE 'Repeat'
        END as customer_type,
        f.order_amount_usd::numeric as revenue
    FROM fact_orders f
    LEFT JOIN customer_first_purchase cf ON f.customer_id = cf.customer_id
    WHERE f.order_year_month IS NOT NULL AND f.order_year_month != ''
)
SELECT 
    order_year_month,
    customer_type,
    COUNT(DISTINCT customer_id) as customers,
    COUNT(*) as orders,
    ROUND(SUM(revenue), 2) as revenue,
    ROUND(AVG(revenue), 2) as avg_order_value,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY order_year_month), 2) as pct_of_monthly_orders
FROM monthly_customers
GROUP BY order_year_month, customer_type
ORDER BY order_year_month DESC, customer_type;

-- Summary: New vs Repeat Share by Month
WITH customer_first_purchase AS (
    SELECT 
        customer_id,
        MIN(f.order_date) as first_purchase_date
    FROM fact_orders f
    WHERE f.order_date IS NOT NULL
    GROUP BY customer_id
),
monthly_split AS (
    SELECT 
        f.order_year_month,
        CASE 
            WHEN cf.first_purchase_date::date = f.order_date::date THEN 'New'
            ELSE 'Repeat'
        END as customer_type,
        COUNT(*) as orders
    FROM fact_orders f
    LEFT JOIN customer_first_purchase cf ON f.customer_id = cf.customer_id
    WHERE f.order_year_month IS NOT NULL AND f.order_year_month != ''
    GROUP BY f.order_year_month, customer_type
)
SELECT 
    order_year_month,
    SUM(CASE WHEN customer_type = 'New' THEN orders ELSE 0 END) as new_customer_orders,
    SUM(CASE WHEN customer_type = 'Repeat' THEN orders ELSE 0 END) as repeat_customer_orders,
    SUM(orders) as total_orders,
    ROUND(SUM(CASE WHEN customer_type = 'New' THEN orders ELSE 0 END)::numeric / SUM(orders) * 100, 2) as new_customer_pct,
    ROUND(SUM(CASE WHEN customer_type = 'Repeat' THEN orders ELSE 0 END)::numeric / SUM(orders) * 100, 2) as repeat_customer_pct
FROM monthly_split
GROUP BY order_year_month
ORDER BY order_year_month DESC;

-- =====================================================================
-- 5️⃣ PARETO: TOP COUNTRIES CONTRIBUTING 80% OF REVENUE
-- =====================================================================

WITH country_revenue AS (
    SELECT 
        f.country_code,
        ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue
    FROM fact_orders f
    WHERE f.country_code IS NOT NULL AND f.country_code != ''
    GROUP BY f.country_code
),
country_ranked AS (
    SELECT 
        country_code,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) as cumulative_revenue,
        (SELECT SUM(revenue) FROM country_revenue) as total_revenue,
        ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) / (SELECT SUM(revenue) FROM country_revenue) * 100, 2) as cumulative_pct,
        ROW_NUMBER() OVER (ORDER BY revenue DESC) as rank
    FROM country_revenue
)
SELECT 
    rank,
    country_code,
    ROUND(revenue, 2) as revenue,
    ROUND(revenue / total_revenue * 100, 2) as revenue_pct,
    cumulative_pct,
    CASE 
        WHEN cumulative_pct <= 80 THEN '🎯 PARETO 80%'
        ELSE 'Rest'
    END as pareto_segment
FROM country_ranked
ORDER BY rank;

-- Pareto Summary
WITH country_revenue AS (
    SELECT 
        f.country_code,
        ROUND(SUM(f.order_amount_usd::numeric), 2) as revenue
    FROM fact_orders f
    WHERE f.country_code IS NOT NULL AND f.country_code != ''
    GROUP BY f.country_code
),
country_ranked AS (
    SELECT 
        country_code,
        revenue,
        SUM(revenue) OVER (ORDER BY revenue DESC) as cumulative_revenue,
        (SELECT SUM(revenue) FROM country_revenue) as total_revenue,
        ROUND(SUM(revenue) OVER (ORDER BY revenue DESC) / (SELECT SUM(revenue) FROM country_revenue) * 100, 2) as cumulative_pct
    FROM country_revenue
)
SELECT 
    COUNT(*) as countries_in_pareto_80,
    ROUND(SUM(revenue), 2) as pareto_80_revenue,
    (SELECT SUM(revenue) FROM country_revenue) as total_revenue,
    ROUND(SUM(revenue) / (SELECT SUM(revenue) FROM country_revenue) * 100, 2) as pareto_80_pct
FROM country_ranked
WHERE cumulative_pct <= 80;

-- =====================================================================
-- 6️⃣ AVERAGE SHIPPING TIME (ORDER → SHIP) BY COUNTRY & PLATFORM
-- =====================================================================

-- Note: Using order_date vs ship_ts to calculate shipping time
SELECT 
    f.country_code,
    f.purchase_platform,
    COUNT(f.order_id) as orders,
    ROUND(AVG(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as avg_shipping_days,
    ROUND(MIN(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as min_shipping_days,
    ROUND(MAX(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as max_shipping_days,
    ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY 
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as median_shipping_days
FROM fact_orders f
WHERE f.order_date IS NOT NULL 
    AND f.order_date != ''
    AND f.ship_ts IS NOT NULL 
    AND f.ship_ts != ''
    AND f.country_code IS NOT NULL
    AND f.country_code != ''
    AND f.purchase_platform IS NOT NULL
    AND EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp)) >= 0
GROUP BY f.country_code, f.purchase_platform
ORDER BY avg_shipping_days DESC;

-- Shipping Time by Country (Overall)
SELECT 
    f.country_code,
    COUNT(f.order_id) as orders,
    ROUND(AVG(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as avg_shipping_days,
    ROUND(MIN(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as min_shipping_days,
    ROUND(MAX(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as max_shipping_days
FROM fact_orders f
WHERE f.order_date IS NOT NULL 
    AND f.order_date != ''
    AND f.ship_ts IS NOT NULL 
    AND f.ship_ts != ''
    AND f.country_code IS NOT NULL
    AND f.country_code != ''
    AND EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp)) >= 0
GROUP BY f.country_code
ORDER BY avg_shipping_days DESC
LIMIT 20;

-- Shipping Time by Platform (Overall)
SELECT 
    f.purchase_platform,
    COUNT(f.order_id) as orders,
    ROUND(AVG(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as avg_shipping_days,
    ROUND(MIN(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as min_shipping_days,
    ROUND(MAX(
        EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp))
    ), 2) as max_shipping_days
FROM fact_orders f
WHERE f.order_date IS NOT NULL 
    AND f.order_date != ''
    AND f.ship_ts IS NOT NULL 
    AND f.ship_ts != ''
    AND EXTRACT(DAY FROM (f.ship_ts::timestamp - f.order_date::timestamp)) >= 0
GROUP BY f.purchase_platform
ORDER BY avg_shipping_days DESC;

-- =====================================================================
-- BONUS: COMPREHENSIVE BUSINESS DASHBOARD
-- =====================================================================

-- KPI Summary with NULL handling
SELECT 
    'Total Orders' as metric,
    COUNT(f.order_id)::text as value,
    'orders' as unit
FROM fact_orders f
WHERE f.order_id IS NOT NULL AND f.order_id != ''
UNION ALL
SELECT 'Total Revenue', 
    ROUND(SUM(f.order_amount_usd::numeric), 2)::text, 
    'USD'
FROM fact_orders f
WHERE f.order_amount_usd IS NOT NULL AND f.order_amount_usd != ''
UNION ALL
SELECT 'Total Customers', 
    COUNT(DISTINCT f.customer_id)::text, 
    'customers'
FROM fact_orders f
WHERE f.customer_id IS NOT NULL AND f.customer_id != ''
UNION ALL
SELECT 'Avg Order Value', 
    ROUND(AVG(f.order_amount_usd::numeric), 2)::text, 
    'USD'
FROM fact_orders f
WHERE f.order_amount_usd IS NOT NULL AND f.order_amount_usd != ''
UNION ALL
SELECT 'Countries', 
    COUNT(DISTINCT f.country_code)::text, 
    'countries'
FROM fact_orders f
WHERE f.country_code IS NOT NULL AND f.country_code != ''
UNION ALL
SELECT 'Products', 
    COUNT(DISTINCT f.product_id)::text, 
    'products'
FROM fact_orders f
WHERE f.product_id IS NOT NULL AND f.product_id != '';

-- =====================================================================
-- END OF ADVANCED ANALYTICS QUERIES
-- =====================================================================
