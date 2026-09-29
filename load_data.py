import pandas as pd
import sqlite3

# Load the CSV
df = pd.read_csv("train.csv")

# Clean up: convert Order Date to actual datetime
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Create a SQLite database file
conn = sqlite3.connect("retail.db")

# Save the dataframe as a SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)

print("Data loaded into retail.db successfully!")
print("Table 'sales' created with", len(df), "rows.")

conn.close()
