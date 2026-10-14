import pandas as pd
from pathlib import Path

# Locate the data folder
data_folder = Path(__file__).parent / "data" / "raw"

# Find the fund master CSV automatically
matches = list(data_folder.glob("*fund_master.csv"))

if not matches:
    print("Fund master CSV not found!")
else:
    file_path = matches[0]

    print("Loading file:", file_path.name)

    df = pd.read_csv(file_path)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    for column in df.columns:
        print(f"\nUnique values in {column}:")
        print(df[column].dropna().unique()[:15])
        print("\n" + "=" * 50)
print("FUND MASTER SUMMARY")
print("=" * 50)

columns_to_explore = [
    "fund_house",
    "category",
    "sub_category",
    "risk_category"
]

for column in columns_to_explore:
    unique_values = sorted(df[column].dropna().unique().tolist())

    print(f"\n{column.upper()}")
    print("Number of unique values:", len(unique_values))

    for value in unique_values:
        print("-", value)