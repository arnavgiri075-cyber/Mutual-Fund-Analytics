import pandas as pd
from pathlib import Path

# Folder containing the original CSV datasets
DATA_FOLDER = Path(__file__).parent / "data" / "raw"

# Find all CSV files
csv_files = sorted(DATA_FOLDER.glob("*.csv"))

print("=" * 70)
print("MUTUAL FUND ANALYTICS - DATA INGESTION")
print("=" * 70)

print(f"\nTotal CSV files found: {len(csv_files)}")

if len(csv_files) != 10:
    print(f"WARNING: Expected 10 CSV files, but found {len(csv_files)}.")

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in: {DATA_FOLDER}"
    )

# Load and inspect each dataset
for file_path in csv_files:
    print("\n" + "=" * 70)
    print(f"DATASET: {file_path.name}")
    print("=" * 70)

    try:
        df = pd.read_csv(file_path)

        print("\nShape (rows, columns):")
        print(df.shape)

        print("\nColumn data types:")
        print(df.dtypes)

        print("\nFirst 5 rows:")
        print(df.head())

        print("\nMissing values per column:")
        print(df.isnull().sum())

        print("\nDuplicate rows:")
        print(df.duplicated().sum())

        print("\nColumn names:")
        print(df.columns.tolist())

    except Exception as error:
        print(f"Could not load {file_path.name}: {error}")

print("\n" + "=" * 70)
print("DATA INGESTION INSPECTION COMPLETED")
print("=" * 70)