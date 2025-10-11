import csv
import re
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
DATA_FOLDER = os.path.join(project_root, 'data')
INPUT_FILE = os.path.join(DATA_FOLDER, 'countries.csv')
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'countries_weighted.csv')

# We'll assign weights based on tiers of tennis-prominent nations.
# This ensures a more realistic distribution of player nationalities.
WEIGHT_TIER_1 = 10  # e.g., USA, Spain, France, etc.
WEIGHT_TIER_2 = 5  # e.g., Canada, Japan, Switzerland, etc.
WEIGHT_TIER_3 = 2  # All other countries

# List of country abbreviations for each tier
TIER_1_NATIONS = {'USA', 'ESP', 'FRA', 'AUS', 'SRB', 'RUS', 'ITA', 'GER'}
TIER_2_NATIONS = {'GBR', 'ARG', 'CRO', 'SUI', 'CAN', 'JPN', 'SWE', 'CZE'}


def get_weight(country_abbr: str) -> int:
    """Assigns a weight to a country based on its tier."""
    if country_abbr in TIER_1_NATIONS:
        return WEIGHT_TIER_1
    elif country_abbr in TIER_2_NATIONS:
        return WEIGHT_TIER_2
    else:
        return WEIGHT_TIER_3


def process_country_data():
    """Reads the input CSV, cleans it, adds weights, and writes to a new file."""
    processed_rows = []

    try:
        with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)
            header = next(reader)  # Skip header

            for row in reader:
                country_name, country_abbr = row

                # Clean the country name by removing anything in parentheses
                clean_name = re.sub(r'\s*\(.*\)\s*', '', country_name).strip()

                # Assign a weight based on the country's abbreviation
                weight = get_weight(country_abbr)

                processed_rows.append({
                    'country_name': clean_name,
                    'abbreviation': country_abbr,
                    'weight': weight
                })

    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return

    # Write the new, clean data to the output file
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['country_name', 'abbreviation', 'weight']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(processed_rows)

        print(f"Successfully created '{OUTPUT_FILE}' with cleaned data and weights.")

    except IOError:
        print(f"Error: Could not write to file '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    process_country_data()