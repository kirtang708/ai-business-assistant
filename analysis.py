import sqlite3
import pandas as pd

conn = sqlite3.connect("retail.db")

# 1. Total revenue by Category
print("=== Revenue by Category ===")
query1 = """
SELECT Category, ROUND(SUM(Sales), 2) as Total_Sales
FROM sales
GROUP BY Category
ORDER BY Total_Sales DESC
"""
print(pd.read_sql(query1, conn))

# 2. Total revenue by Region
print("\n=== Revenue by Region ===")
query2 = """
SELECT Region, ROUND(SUM(Sales), 2) as Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC
"""
print(pd.read_sql(query2, conn))

# 3. Monthly revenue trend
print("\n=== Monthly Revenue Trend ===")
query3 = """
SELECT strftime('%Y-%m', "Order Date") as Month, ROUND(SUM(Sales), 2) as Total_Sales
FROM sales
GROUP BY Month
ORDER BY Month
"""
monthly = pd.read_sql(query3, conn)
print(monthly)

# 4. Month-over-month % change (computed in Python, not SQL)
print("\n=== Month-over-Month % Change ===")
monthly["Pct_Change"] = monthly["Total_Sales"].pct_change() * 100
print(monthly)

conn.close()
