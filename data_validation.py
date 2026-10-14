import pandas as pd
from pathlib import Path

# Locate the raw data folder
data_folder = Path(__file__).parent / "data" / "raw"

# Find the two required datasets
fund_files = list(data_folder.glob("*fund_master.csv"))
nav_files = list(data_folder.glob("*nav_history.csv"))

if not fund_files or not nav_files:
    print("ERROR: Could not find both datasets.")
    print("CSV files found:", [f.name for f in data_folder.glob("*.csv")])

else:
    fund_master = pd.read_csv(fund_files[0])
    nav_history = pd.read_csv(nav_files[0])

    print("Fund master file:", fund_files[0].name)
    print("NAV history file:", nav_files[0].name)

    print("\nFund master shape:", fund_master.shape)
    print("NAV history shape:", nav_history.shape)

    # Check that the required columns exist
    if "amfi_code" not in fund_master.columns:
        print("ERROR: amfi_code column not found in fund master.")

    elif "amfi_code" not in nav_history.columns:
        print("ERROR: amfi_code column not found in NAV history.")

    else:
        # Convert codes to numeric values and ignore invalid entries
        master_codes = set(
            pd.to_numeric(
                fund_master["amfi_code"], errors="coerce"
            ).dropna().astype(int)
        )

        nav_codes = set(
            pd.to_numeric(
                nav_history["amfi_code"], errors="coerce"
            ).dropna().astype(int)
        )

        # Compare the scheme codes
        missing_codes = master_codes - nav_codes
        matching_codes = master_codes & nav_codes

        print("\n" + "=" * 50)
        print("AMFI CODE VALIDATION")
        print("=" * 50)

        print("Unique codes in fund master:", len(master_codes))
        print("Unique codes in NAV history:", len(nav_codes))
        print("Matching scheme codes:", len(matching_codes))
        print("Missing scheme codes:", len(missing_codes))

        if missing_codes:
            print("\nCodes missing from NAV history:")
            print(sorted(missing_codes))
        else:
            print("\nAll fund master codes exist in NAV history.")

        # Save the missing codes for further investigation
        missing_df = pd.DataFrame(
            sorted(missing_codes),
            columns=["missing_amfi_code"]
        )

        output_file = (
            Path(__file__).parent
            / "data"
            / "processed"
            / "missing_amfi_codes.csv"
        )

        missing_df.to_csv(output_file, index=False)

        print("\nMissing-code report saved to:", output_file)