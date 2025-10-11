import csv
import os
from faker import Faker
from collections import defaultdict
from tqdm import tqdm

# --- CONFIGURATION ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'countries_weighted.csv')
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'names.csv')
NUM_NAMES_PER_GENDER_PER_COUNTRY = 50

# --- FAKER LOCALE MAPPING ---
# Maps our 3-letter country codes to Faker's locale codes.
# Not all countries have a Faker locale, so we'll use a default for missing ones.
LOCALE_MAP = {
    'USA': 'en_US', 'ESP': 'es_ES', 'ITA': 'it_IT', 'RUS': 'ru_RU',
    'AUS': 'en_AU', 'NOR': 'no_NO', 'POL': 'pl_PL', 'GRE': 'el_GR',
    'BUL': 'bg_BG', 'DEN': 'dk_DK', 'CAN': 'en_CA', 'FRA': 'fr_FR',
    'JPN': 'ja_JP', 'SUI': 'de_CH', 'GER': 'de_DE',
    'GBR': 'en_GB', 'ARG': 'es_AR', 'CRO': 'hr_HR', 'CHI': 'es_CL',
    'SWE': 'sv_SE', 'CZE': 'cs_CZ', 'BRA': 'pt_BR', 'NED': 'nl_NL'
}
DEFAULT_LOCALE = 'en_US'  # Fallback for countries not in our map


def generate_names_file():
    """Reads country data and generates a CSV of localized, gendered names."""
    countries = []
    try:
        with open(INPUT_FILE, 'r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                countries.append(row['abbreviation'])
    except FileNotFoundError:
        print(f"Error: Input file '{INPUT_FILE}' not found.")
        return

    all_names = []
    print("Generating localized and gendered names...")

    fake_generators = defaultdict(lambda: Faker(DEFAULT_LOCALE))
    for locale_code in set(LOCALE_MAP.values()):
        fake_generators[locale_code] = Faker(locale_code)

    for country_abbr in tqdm(countries, desc="Processing countries"):
        locale = LOCALE_MAP.get(country_abbr, DEFAULT_LOCALE)
        fake = fake_generators[locale]

        for _ in range(NUM_NAMES_PER_GENDER_PER_COUNTRY):
            # Generate a male name
            all_names.append({
                'first_name': fake.first_name_male(),
                'last_name': fake.last_name(),
                'country_abbr': country_abbr,
                'sab': 'M'
            })
            # Generate a female name
            all_names.append({
                'first_name': fake.first_name_female(),
                'last_name': fake.last_name(),
                'country_abbr': country_abbr,
                'sab': 'F'
            })

    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = ['first_name', 'last_name', 'country_abbr', 'sab']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_names)

        print(f"\nSuccessfully created '{OUTPUT_FILE}' with {len(all_names)} names.")
    except IOError:
        print(f"Error: Could not write to file '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    generate_names_file()