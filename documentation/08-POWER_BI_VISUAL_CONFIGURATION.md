# 🎨 Power BI Dashboard - Visual Configuration Templates

**Version:** 1.0  
**Date:** December 10, 2025  
**Purpose:** Detailed visual design specifications and configurations

---

## 📐 Visual Configuration Repository

### **Template 1: Executive Summary KPI Cards**

#### **Configuration Details:**

**Card Properties:**
```
Visual Type:        Card
Data Labels:        On (Bold, 14pt)
Decimal Places:     2
Display Units:      Millions (for revenue)
Title:              Enabled (12pt, Gray)
Title Text:
  - "Total Revenue"
  - "Total Orders"
  - "Avg Order Value"
  - "Active Products"
```

**Formatting Applied:**
```
Background:         White
Border:             Light gray (1px)
Shadow:             Subtle
Font Color:         Dark blue (#1f77b4)
Title Color:        Medium gray
Alignment:          Center
Padding:            15px
```

**Sample Values:**
```
Card 1: $6,103,275.79 (Revenue)
Card 2: 21,680 (Orders)
Card 3: $281.68 (Average Order)
Card 4: 8 (Products)
```

---

### **Template 2: Revenue Trend Line Chart**

#### **Data Configuration:**

**Axis (X):**
- Field: dim_date[order_date]
- Granularity: Month
- Type: Date/Time
- Sort: Ascending

**Values (Y):**
- Measure: SUM(fact_orders[order_amount_usd])
- Format: Currency ($)
- Decimals: 0

**Visual Properties:**
```
Chart Type:         Line Chart
Line Style:         Solid
Line Width:         2.5px
Data Points:        Visible (4px circles)
Trend Line:         Enabled
Trend Line Type:    Linear
Confidence Interval: 95%
```

**Legend:**
```
Position:           Top
Background:         None
Title:              Hidden
```

**Tooltips:**
```
Enabled:            Yes
Title:              "Date"
Show Values:        Revenue, Month
Format:             Currency, Readable date
```

**Formatting:**
```
Color (Line):       #1f77b4 (Blue)
Color (Points):     #1f77b4
Color (Trend):      #d62728 (Red)
Background:         #f8f8f8 (Light gray)
Grid Lines:         Enabled (Light)
```

---

### **Template 3: Top 5 Products Bar Chart**

#### **Data Configuration:**

**Axis (Y):**
- Field: dim_products[product_name]
- Sorting: By revenue (descending)
- Top N: 5 (dynamic top 5 filter)

**Values (X):**
- Measure: SUM(fact_orders[order_amount_usd])
- Format: Currency ($)
- Decimals: 0

**Visual Properties:**
```
Chart Type:         Horizontal Bar Chart
Bar Style:          Standard
Spacing:            10% (between bars)
Data Labels:        On (Right side)
Data Label Format:  Currency, Bold
Label Position:     Outside end
```

**Color:**
```
Single Color:       Off
By Field:           fact_orders[order_amount_usd]
Color Scale:        Green → Yellow → Red
Minimum:            $500K
Center:             $1M
Maximum:            $2M
```

**Sorting:**
```
Sort By:            fact_orders[order_amount_usd]
Order:              Descending
```

**Tooltips:**
```
Show:               Product name, Revenue, Orders, Rank
Format:             Readable format
```

---

### **Template 4: Platform Distribution Donut Chart**

#### **Data Configuration:**

**Legend:**
- Field: dim_platform[platform_name]

**Values:**
- Measure: COUNT(fact_orders[order_id])
- Format: Number
- Decimals: 0

**Visual Properties:**
```
Chart Type:         Donut Chart
Donut Size:         50% (ring width)
Data Labels:        On
Label Style:        Percentage (with value)
Label Position:     Outside
Category Labels:    Enabled
Legend Title:       "Platform"
Legend Position:    Right
```

**Color:**
```
Color By:           Platform
Palette:
  - Web:      #1f77b4 (Blue)
  - Mobile:   #2ca02c (Green)
```

**Center Text:**
```
Title:              "Total Orders"
Subtitle:           "21,680"
Font Size:          14pt
Color:              #1f77b4
```

**Tooltips:**
```
Show:               Platform, Orders, Percentage
Format:             Number, Percentage
```

---

### **Template 5: Marketing Channel Performance Matrix/Table**

#### **Data Configuration:**

**Rows:**
- Field: dim_marketing_channel[channel_name]
- Sorting: By revenue (descending)

**Column Values:**
```
Column 1: COUNT(fact_orders[order_id])
  ├─ Header:        "Orders"
  ├─ Format:        Whole number
  └─ Color:         Data bars (blue)

Column 2: SUM(fact_orders[order_amount_usd])
  ├─ Header:        "Revenue"
  ├─ Format:        Currency
  └─ Color:         Data bars (green), gradient

Column 3: DIVIDE(SUM, COUNT) [AOV]
  ├─ Header:        "Avg Order Value"
  ├─ Format:        Currency
  └─ Color:         None

Column 4: Market Share %
  ├─ Header:        "% of Total"
  ├─ Format:        Percentage (1 decimal)
  └─ Color:         Data bars (orange)
```

**Visual Properties:**
```
Table Type:         Matrix
Font Size:          11pt
Alternating Row:    Enabled (Light gray background)
Grid Lines:         Horizontal (Light)
Headers:            Bold, Dark gray background
Subtotals:          Enabled (bottom)
Column Width:       Auto
Row Height:         Standard
```

**Conditional Formatting:**
```
Data Bars:
  - Enabled for Orders (Blue)
  - Enabled for Revenue (Green)
  - Enabled for % Share (Orange)
Value Threshold:
  - Green:         > 80%
  - Yellow:        50-80%
  - Red:           < 50%
```

---

### **Template 6: Geographic Heatmap**

#### **Data Configuration:**

**Location:**
- Field: dim_country[country_code]
- Type: Country/Region

**Saturation:**
- Measure: SUM(fact_orders[order_amount_usd])
- Format: Currency
- Aggregation: Sum

**Visual Properties:**
```
Map Type:           Filled Map
Zoom Level:         Fit to data
Projection:         Mercator
```

**Color Scheme:**
```
Minimum:            #e8f4f8 (Light blue)
Center:             #90c9dd (Medium blue)
Maximum:            #003d5c (Dark blue)
Diverging:          Disabled
Invert:             Disabled
```

**Data Labels:**
```
Show Country Names:  Enabled
Font Size:          10pt
Font Color:         #000000
```

**Tooltips:**
```
Show:               Country, Revenue, Orders, Customers
Format:             Currency, Numbers, Readable
```

**Formatting:**
```
Default Color:      #f0f0f0 (for missing data)
Borders:            Light gray (1px)
Hover Effect:       Outline (2px dark blue)
```

---

### **Template 7: Product Performance Scatter Plot**

#### **Data Configuration:**

**X-Axis (Size):**
- Field: COUNT(fact_orders[order_id])
- Label: "Order Volume"
- Type: Continuous

**Y-Axis:**
- Measure: SUM(fact_orders[order_amount_usd])
- Label: "Total Revenue"
- Type: Continuous

**Bubble Size:**
- Measure: DISTINCTCOUNT(dim_customer[customer_id])
- Min Size: 30px
- Max Size: 150px

**Legend:**
- Field: dim_products[product_name]
- Position: Right
- Show All Items: Yes

**Visual Properties:**
```
Chart Type:         Scatter Chart
Bubble Opacity:     80%
Point Size:         Medium
Hover Effect:       Highlight + Data labels
X-Axis Scale:       Linear
Y-Axis Scale:       Linear
```

**Color:**
```
Color By:           Product
Palette:            Default (8 distinct colors)
```

**Tooltips:**
```
Show:               Product, Orders, Revenue, Customers
Format:             Names, Numbers, Currency
```

**Reference Lines:**
```
Line 1 (Median Orders):   Enabled (Dashed, Gray)
Line 2 (Median Revenue):  Enabled (Dashed, Gray)
Label:              "Median"
```

---

### **Template 8: Monthly Trend Stacked Area Chart**

#### **Data Configuration:**

**X-Axis (Time):**
- Field: dim_date[order_date]
- Granularity: Month
- Format: "YYYY-MMM"

**Y-Axis:**
- Measure: SUM(fact_orders[order_amount_usd])
- Format: Currency ($)
- Decimals: 0

**Legend (Stacked By):**
- Field: dim_products[product_name]
- Top Items: Top 5 by revenue

**Visual Properties:**
```
Chart Type:         Stacked Area Chart
Area Opacity:       75%
Smoothing:          Enabled (Catmull-Rom)
Data Points:        Small (3px)
Legend Position:    Top
Legend Title:       "Product"
```

**Color Palette:**
```
Product 1 (Nintendo):    #1f77b4 (Blue)
Product 2 (Monitor):     #ff7f0e (Orange)
Product 3 (PlayStation): #2ca02c (Green)
Product 4 (Lenovo):      #d62728 (Red)
Product 5 (Other):       #9467bd (Purple)
Others:                  #7f7f7f (Gray)
```

**Tooltips:**
```
Show:               Month, Product, Revenue, % of Total
Format:             Month name, Product name, Currency, %
```

---

## 🎯 Color Palette Standards

### **Brand Colors**

**Primary Palette:**
```
Primary Blue:       #1f77b4  (Used for main metrics)
Primary Orange:     #ff7f0e  (Used for secondary metrics)
Primary Green:      #2ca02c  (Used for positive indicators)
Primary Red:        #d62728  (Used for alerts/warnings)
Primary Purple:     #9467bd  (Used for accent)
```

**Supporting Colors:**
```
Light Blue:         #aec7e8
Light Orange:       #ffbb78
Light Green:        #98df8a
Light Red:          #ff9896
Light Purple:       #c5b0d5

Dark Blue:          #08519c
Dark Orange:        #e67e22
Dark Green:         #1a7d1a
Dark Red:           #8b0000
Dark Purple:        #663399
```

**Neutral Colors:**
```
Dark Gray:          #333333 (Text)
Medium Gray:        #666666 (Secondary text)
Light Gray:         #cccccc (Borders)
Very Light Gray:    #f0f0f0 (Backgrounds)
White:              #ffffff
```

---

## 📐 Typography Standards

### **Font Family**
- Primary: Segoe UI
- Fallback: Arial
- Monospace: Consolas (for numbers/codes)

### **Font Sizes**

**Page Title:**
```
Size:               24pt
Weight:             Bold
Color:              #333333
Spacing:            Bottom 20px
```

**Section Header:**
```
Size:               18pt
Weight:             Bold
Color:              #1f77b4
Spacing:            Bottom 15px
```

**Visual Title:**
```
Size:               14pt
Weight:             Semi-bold
Color:              #333333
Spacing:            Bottom 10px
```

**Data Labels:**
```
Size:               11pt
Weight:             Regular
Color:              #333333
```

**Tooltips:**
```
Size:               10pt
Weight:             Regular
Color:              #333333
```

---

## 📏 Layout & Spacing

### **Page Layout**

**Margins:**
```
Top:                20px
Bottom:             20px
Left:               20px
Right:              20px
```

**Visual Spacing:**
```
Between Visuals:    20px minimum
Around Title:       15px
Padding Inside:     10px
```

### **Visual Grid**

**Page Grid:**
```
Columns:            12 (12-column layout)
Rows:               Auto (based on content)
Grid Size:          20px
Alignment:          Snapping enabled
```

**Responsive Design:**
```
Desktop (1920px):   Full width, 2-3 visuals per row
Tablet (1024px):    2 visuals per row
Mobile (540px):     1 visual per row
```

---

## 🔄 Slicer Configuration Templates

### **Date Range Slicer**

**Configuration:**
```
Field:              dim_date[order_date]
Type:               Between (Date Range)
Style:              Between dates picker
Default Range:      Last 12 months
Show All Option:    Enabled
Multi-Select:       Enabled
Search:             Enabled
```

**Properties:**
```
Width:              250px
Height:             50px
Background:         #ffffff
Border:             1px solid #cccccc
Font Size:          11pt
```

---

### **Product Filter Slicer**

**Configuration:**
```
Field:              dim_products[product_name]
Type:               List (Buttons)
Style:              Buttons with selection
Search:             Enabled
Multi-Select:       Enabled
Select All:         Enabled (default: all selected)
```

**Properties:**
```
Layout:             Horizontal
Button Style:       Rounded corners
Selected Color:     #1f77b4
Unselected Color:   #f0f0f0
Width:              Auto
Height:             40px (per button row)
```

---

### **Channel Slicer**

**Configuration:**
```
Field:              dim_marketing_channel[channel_name]
Type:               List (Dropdown)
Style:              Dropdown
Search:             Enabled
Multi-Select:       Enabled
All Option:         Enabled
```

**Properties:**
```
Width:              200px
Height:             35px
Font Size:          11pt
```

---

## 🎬 Animation & Interactivity

### **Page Transitions**

**Transition Effects:**
```
Enabled:            Yes
Duration:           500ms
Easing:             Ease-in-out
Effect Type:        Fade
```

### **Visual Hover Effects**

**Hover Behavior:**
```
Show Tooltip:       On hover (delay: 200ms)
Highlight Related:  Enabled
Fade Others:        Enabled (opacity: 40%)
Outline:            2px highlight
```

---

## 📊 Conditional Formatting Guide

### **Data Bar Formatting**

**Type 1: Revenue Bars (Green)**
```
Visual Type:        Data bars
Direction:          Left to right
Color:              #2ca02c (Green)
Minimum Value:      0
Maximum Value:      Automatic
Bar Opacity:        80%
Text Color:         Auto (based on background)
```

**Type 2: Performance Bars (Color Scale)**
```
Visual Type:        Background color
Minimum Color:      #ff9896 (Light Red) - Below 50%
Middle Color:       #ffbb78 (Light Orange) - 50-80%
Maximum Color:      #98df8a (Light Green) - Above 80%
Text Color:         #333333
```

---

## 🔐 Access & Permissions

### **Report Permissions**

**Admin Level:**
```
View:               ✅ Yes
Edit:               ✅ Yes
Share:              ✅ Yes
Delete:             ✅ Yes
Manage Alerts:      ✅ Yes
```

**Viewer Level:**
```
View:               ✅ Yes
Edit:               ❌ No
Share:              ❌ No
Delete:             ❌ No
Manage Alerts:      ✅ Yes (own alerts)
```

---

## 📱 Mobile Optimization

### **Mobile Layout Adjustments**

**Visual Resizing:**
```
KPI Cards:          Full width, stacked vertically
Charts:             Full width, adjusted height
Tables:             Horizontal scroll enabled
Maps:               Zoom to fit
```

**Typography Adjustments:**
```
Title:              20pt (vs 24pt desktop)
Headers:            14pt (vs 18pt)
Labels:             10pt (vs 11pt)
```

**Interaction Adjustments:**
```
Slicers:            Dropdown style (vs buttons)
Drill-through:      Single tap enabled
Tooltips:           Long press to show
```

---

**Power BI Visual Configuration Templates - Version 1.0**  
**Last Updated:** December 10, 2025  
**Status:** ✅ Ready for Implementation

