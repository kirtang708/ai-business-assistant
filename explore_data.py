import pandas as pd

df = pd.read_csv("train.csv")

print("Columns:", df.columns.tolist())
print("\nShape (rows, columns):", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nData types:")
print(df.dtypes)
