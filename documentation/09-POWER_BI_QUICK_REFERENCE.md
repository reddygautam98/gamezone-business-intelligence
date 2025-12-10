# 🚀 Power BI Dashboard - Quick Reference Guide

**Version:** 1.0  
**Date:** December 10, 2025  
**Purpose:** Quick-start checklist and lookup guide

---

## ⚡ 30-Minute Quick Start

### **Minute 0-5: Setup Connection**
```
1. Open Power BI Desktop
2. Get Data → PostgreSQL Database
3. Server: 127.0.0.1
4. Database: gamezone_analytics
5. Click OK, enter credentials
```

### **Minute 5-10: Import Tables**
```
✓ Select all 7 tables
✓ Click Load (not Edit)
✓ Wait for import to complete
✓ Verify table names in Data pane
```

### **Minute 10-15: Create Relationships**
```
✓ View → Data Model
✓ Create 6 relationships (Many-to-One)
✓ From fact_orders to each dimension table
✓ Verify no errors in relationship diagram
```

### **Minute 15-20: Add First Page**
```
✓ Insert → New Page
✓ Rename: "Executive Summary"
✓ Add 4 KPI cards
✓ Add 1 line chart (revenue trend)
```

### **Minute 20-30: Create Key Measures**
```
DAX Formula 1: Total Revenue
=SUM(fact_orders[order_amount_usd])

DAX Formula 2: Total Orders
=COUNTA(fact_orders[order_id])

DAX Formula 3: Average Order Value
=DIVIDE([Total Revenue], [Total Orders], 0)
```

✅ **You now have a working dashboard!**

---

## 📊 5-Page Dashboard Overview

| Page | Purpose | Key Visuals | Time |
|------|---------|------------|------|
| **Executive Summary** | KPIs & trends | 5 cards + 2 charts | 2 hrs |
| **Product Analytics** | Product performance | 5 visuals (matrix, scatter, etc.) | 3 hrs |
| **Customer Intelligence** | Geographic analysis | Map, heatmap, trends | 3 hrs |
| **Marketing Attribution** | Channel performance | Bar charts, matrix, trends | 2 hrs |
| **Platform Performance** | Web vs Mobile | Comparison cards, pie charts | 2 hrs |

**Total Build Time: 12-15 hours**

---

## 🔧 Essential DAX Formulas

### **Formula 1: Total Revenue**
```dax
Total Revenue = SUM(fact_orders[order_amount_usd])
```
**Used in:** Executive Summary, Product Analytics, Revenue cards

### **Formula 2: Average Order Value**
```dax
Average Order Value = DIVIDE([Total Revenue], [Total Orders])
```
**Used in:** KPI cards, Product comparison

### **Formula 3: Unique Customers**
```dax
Unique Customers = DISTINCTCOUNT(dim_customer[customer_id])
```
**Used in:** Customer Intelligence page

### **Formula 4: Revenue Share**
```dax
Revenue Share % = DIVIDE([Total Revenue], 
    CALCULATE([Total Revenue], ALL(dim_products)))
```
**Used in:** Product rankings, channel performance

### **Formula 5: Month-over-Month Growth**
```dax
MoM Growth % = DIVIDE(
    [Current Month Revenue] - [Previous Month Revenue],
    [Previous Month Revenue])
```
**Used in:** Trend analysis, executive summary

---

## 📐 Visual Types Cheat Sheet

| Chart Type | Best For | Configuration |
|-----------|----------|----------------|
| **Card** | KPIs | Single measure, bold font |
| **Line** | Trends over time | Date on X, measure on Y |
| **Bar** | Comparisons | Category on axis, value on other |
| **Pie/Donut** | Proportions | Category in legend, value total |
| **Matrix/Table** | Details | Rows = categories, columns = metrics |
| **Map** | Geography | Location field + saturation measure |
| **Scatter** | Correlation | X & Y axes + bubble size |
| **Area** | Stacked totals | Time on X, stacked values on Y |

---

## 🎨 Color Palette Quick Reference

```
✅ Primary Blue:    #1f77b4  (Main revenue metrics)
✅ Primary Orange:  #ff7f0e  (Secondary metrics)
✅ Primary Green:   #2ca02c  (Growth/positive)
✅ Primary Red:     #d62728  (Alerts/warnings)
✅ Primary Purple:  #9467bd  (Accent colors)

Light variants:
  #aec7e8, #ffbb78, #98df8a, #ff9896, #c5b0d5
```

---

## 🔗 Data Relationships Map

```
fact_orders (21,680 records)
    ├─→ dim_products (8 products)
    ├─→ dim_customer (19,713 customers)
    ├─→ dim_date (772 dates)
    ├─→ dim_country (150 countries)
    ├─→ dim_platform (2 platforms)
    └─→ dim_marketing_channel (5 channels)

All relationships: Many-to-One
Relationship type: Active
```

---

## 📋 Slicer Setup Checklist

- [ ] **Date Slicer** (Top of dashboard)
  - Field: dim_date[order_date]
  - Type: Between dates
  - Default: Last 12 months

- [ ] **Product Slicer** (Page 2)
  - Field: dim_products[product_name]
  - Type: List (buttons)
  - Multi-select: Yes

- [ ] **Country Slicer** (Page 3)
  - Field: dim_country[country_name]
  - Type: Dropdown
  - Search: Enabled

- [ ] **Channel Slicer** (Page 4)
  - Field: dim_marketing_channel[channel_name]
  - Type: Buttons
  - Default: All channels

- [ ] **Platform Slicer** (Page 5)
  - Field: dim_platform[platform_name]
  - Type: Buttons (toggle)
  - Default: Both

---

## 🎯 Common Formatting Rules

### **Number Formatting**
```
Revenue:            Currency ($) with 0 decimals
Orders:             Whole number (0 decimals)
Average Order:      Currency ($) with 2 decimals
Percentages:        0-1 decimals with % symbol
Customer Count:     Whole number (0 decimals)
```

### **Font Sizes**
```
Page Title:         24pt Bold
Section Header:     18pt Bold
Visual Title:       14pt Semi-bold
Data Labels:        11pt Regular
Tooltips:           10pt Regular
```

### **Visual Size Guidelines**
```
KPI Cards:          200px width × 100px height
Line Charts:        50% page width × 40% height
Bar Charts:         33% page width × 50% height
Matrix/Table:       100% page width × 40% height
Maps:               60% page width × 50% height
Pie Charts:         25% page width × 50% height
```

---

## 🚀 Deployment Steps

### **Step 1: Save File**
```powershell
File → Save As
Filename: GameZone_Dashboard_[Date]
Format: Power BI (.pbix)
Location: OneDrive/BI_Reports/
```

### **Step 2: Publish to Service**
```
Home → Publish
Workspace: "GameZone Analytics"
Click: Select
Wait for publishing confirmation
```

### **Step 3: Configure Refresh**
```
Power BI Service → Settings
Add PostgreSQL credentials
Schedule: Daily, 2:00 AM UTC
Notification: Email on failure
```

### **Step 4: Share Report**
```
Click: Share
Add users/groups
Permissions: View (not Edit)
Email notification: Enabled
```

---

## 📱 Mobile View Optimization

**Key Changes:**
```
✓ Remove complex visuals (maps on mobile)
✓ Stack cards vertically (not horizontally)
✓ Use larger touch targets for slicers
✓ Simplify legends (vertical layout)
✓ Test on actual mobile device
```

**Recommended Layout:**
```
Mobile Screen (540px width)
├─ Date slicer (full width)
├─ KPI Cards (1 per row, stacked)
├─ Charts (full width, adjusted height)
└─ Table (horizontal scroll enabled)
```

---

## ❌ Common Mistakes to Avoid

| Mistake | Impact | Solution |
|---------|--------|----------|
| Not creating relationships | Visuals show blanks | Create Many-to-One relationships |
| Too many visuals per page | Dashboard slow | Max 6-8 visuals per page |
| Wrong data types | Calculations fail | Verify data types before analysis |
| Missing measures | Static visuals | Create DAX measures first |
| No slicer synchronization | Confused users | Set all slicers to same filters |
| Hardcoded dates | Dashboard outdated | Use relative date filters |

---

## ⚡ Performance Optimization Tips

### **Reduce Load Time**
```
1. Import Mode (not DirectQuery)
2. Limit visuals: 6-8 per page max
3. Aggregate older data (>2 years)
4. Enable query folding in Power Query
5. Cache frequently used measures
```

### **Improve Query Speed**
```
1. Use aggregation tables
2. Implement incremental refresh
3. Minimize DAX complexity
4. Remove unused columns
5. Set appropriate data types
```

---

## 🔍 Testing Checklist

- [ ] All KPI values correct (verify against SQL)
- [ ] Date slicer filters all pages
- [ ] Product filter shows only selected products
- [ ] Geographic map displays all countries
- [ ] Revenue totals match expected values
- [ ] No N/A or error values visible
- [ ] Dashboard loads in <5 seconds
- [ ] Mobile view displays properly
- [ ] Refresh schedule working
- [ ] Color scheme consistent
- [ ] Tooltips showing information
- [ ] Drill-through works (if configured)

---

## 📞 Quick Help Reference

### **Problem: Connection Failed**
```
Solution:
1. Check PostgreSQL is running
2. Verify server: 127.0.0.1:5432
3. Test credentials in pgAdmin first
4. Check firewall allows connection
5. Restart Power BI Desktop
```

### **Problem: Blank Values in Visuals**
```
Solution:
1. Check relationships are configured
2. Verify data isn't filtered out
3. Check for null values in source
4. Test with SQL query first
5. Verify DAX formula includes BLANK handling
```

### **Problem: Dashboard Loads Slowly**
```
Solution:
1. Remove or hide unused visuals
2. Increase data aggregation
3. Switch to DirectQuery if needed
4. Clear Power BI cache
5. Check PostgreSQL query performance
```

### **Problem: Data Not Refreshing**
```
Solution:
1. Check refresh schedule in Power BI Service
2. Verify credentials are saved
3. Check for errors in Power Query
4. Test manual refresh
5. Check PostgreSQL connection
```

---

## 📚 Additional Resources

### **Documentation Files**
- [07-POWER_BI_DASHBOARD_GUIDE.md](07-POWER_BI_DASHBOARD_GUIDE.md) - Full implementation (2000+ lines)
- [08-POWER_BI_VISUAL_CONFIGURATION.md](08-POWER_BI_VISUAL_CONFIGURATION.md) - Visual specs (800+ lines)
- [analytics_queries_strategic.sql](analytics_queries_strategic.sql) - SQL reference queries

### **External Links**
- Power BI Desktop: https://powerbi.microsoft.com/desktop/
- DAX Function Reference: https://dax.guide/
- Power BI Community: https://community.powerbi.com/
- Microsoft Learn: https://learn.microsoft.com/power-bi/

---

## 📊 Success Metrics

**Dashboard is successful when:**
```
✅ KPIs updated daily
✅ 90%+ user adoption
✅ <5 second load time
✅ 100% data accuracy verified
✅ Users making decisions based on dashboard
✅ Executive leadership using for planning
✅ Mobile view working on all devices
✅ 99%+ refresh success rate
```

---

## 🎓 Learning Path

### **Beginner (Days 1-2)**
- [ ] Complete Quick Start section
- [ ] Build Executive Summary page
- [ ] Master 3 basic DAX formulas
- [ ] Understand 6 relationships

### **Intermediate (Days 3-5)**
- [ ] Build Product Analytics page
- [ ] Learn 5+ advanced DAX formulas
- [ ] Configure slicers for filtering
- [ ] Add conditional formatting

### **Advanced (Days 6+)**
- [ ] Build all 5 dashboard pages
- [ ] Implement drill-through
- [ ] Create bookmarks for navigation
- [ ] Optimize performance
- [ ] Deploy and share with team

---

**Power BI Dashboard Quick Reference - Version 1.0**  
**Last Updated:** December 10, 2025  
**Status:** ✅ Ready for Use

