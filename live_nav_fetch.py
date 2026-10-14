import requests
import pandas as pd
from pathlib import Path

# Folder for raw NAV data
DATA_FOLDER = Path(__file__).parent / "data" / "raw"
DATA_FOLDER.mkdir(parents=True, exist_ok=True)

# Six mutual fund schemes
FUNDS = {
    "HDFC_Top_100": 125497,
    "SBI_Bluechip": 119551,
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841
}

for fund_name, scheme_code in FUNDS.items():

    print("\n" + "=" * 50)
    print(f"Fetching {fund_name} | Code: {scheme_code}")

    url = f"https://api.mfapi.in/mf/{scheme_code}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()

        # Verify scheme information returned by the API
        print("Scheme metadata:", result.get("meta", {}))

        nav_data = result.get("data", [])

        if not nav_data:
            print("No NAV records returned.")
            continue

        df = pd.DataFrame(nav_data)
        df["scheme_code"] = scheme_code

        output_file = DATA_FOLDER / f"{fund_name}_NAV.csv"
        df.to_csv(output_file, index=False)

        print("Total NAV records:", len(df))
        print("\nFirst 3 records:")
        print(df.head(3))
        print("\nSaved to:", output_file)

    except requests.RequestException as error:
        print(f"API request failed: {error}")

    except (ValueError, KeyError) as error:
        print(f"Could not process response: {error}")

print("\nAll scheme requests completed.")