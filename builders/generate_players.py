import csv
import random
import os
from datetime import date
from collections import defaultdict
from tqdm import tqdm

# --- CONFIGURATION ---
# Assumes this script is in the 'builders' folder
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FOLDER = os.path.join(PROJECT_ROOT, 'data')

COUNTRIES_FILE = os.path.join(DATA_FOLDER, 'countries_weighted.csv')
NAMES_FILE = os.path.join(DATA_FOLDER, 'names.csv')
OUTPUT_FILE = os.path.join(DATA_FOLDER, 'players.csv')

TOTAL_PLAYERS_TO_GENERATE = 200
GAME_START_DATE = date(2026, 1, 1)

# Defines the skill range for each player tier
TIERS = {
    "Elite": (86, 99), "Pro": (71, 85), "Challenger": (51, 70),
    "Futures": (31, 50), "Beginner": (1, 30),
}

# Defines the probability of a player's tier based on their age
AGE_TIER_PROBABILITY = {
    (16, 18): {"Futures": 0.3, "Challenger": 0.2, "Pro": 0.1, "Elite": 0.0, "Beginner": 0.4},
    (19, 23): {"Challenger": 0.4, "Pro": 0.3, "Elite": 0.1, "Futures": 0.1, "Beginner": 0.1},
    (24, 29): {"Pro": 0.4, "Elite": 0.3, "Challenger": 0.2, "Futures": 0.1, "Beginner": 0.0},
    (30, 35): {"Pro": 0.3, "Challenger": 0.3, "Elite": 0.1, "Futures": 0.1, "Beginner": 0.0},
}

# --- END CONFIGURATION ---

def load_data(file_path, key_columns, value_columns=None):
    """Generic data loader from CSV."""
    data = defaultdict(lambda: defaultdict(list))
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                primary_key = row[key_columns[0]]
                if len(key_columns) > 1:
                    secondary_key = row[key_columns[1]]
                    data[primary_key][secondary_key].append(tuple(row[col] for col in value_columns))
                else:
                    data[primary_key] = {k: v for k, v in row.items()}
    except FileNotFoundError:
        print(f"Error: Data file not found at '{file_path}'.")
    return data


def get_tier_for_age(age: int) -> str:
    """Determines a player's likely tier based on their age."""
    for (min_age, max_age), probs in AGE_TIER_PROBABILITY.items():
        if min_age <= age <= max_age:
            tiers = list(probs.keys())
            weights = list(probs.values())
            return random.choices(tiers, weights, k=1)[0]
    return "Futures"  # Default for ages outside the defined ranges


def generate_world():
    """Generates a complete, realistic world of players and saves them to a CSV file."""
    names_db = load_data(NAMES_FILE, ['country_abbr', 'sab'], ['first_name', 'last_name'])

    # Load countries and their weights for random selection
    countries_db = []
    country_weights = []
    with open(COUNTRIES_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            countries_db.append(row['abbreviation'])
            country_weights.append(int(row['weight']))

    if not names_db or not countries_db:
        print("Could not proceed due to missing names or countries data.")
        return

    players_data = []
    print(f"Generating {TOTAL_PLAYERS_TO_GENERATE} new players...")

    for i in tqdm(range(TOTAL_PLAYERS_TO_GENERATE), desc="Creating world"):
        # 1. Generate core attributes: Age, Country, SAB
        age = random.randint(min(AGE_TIER_PROBABILITY.keys())[0], max(AGE_TIER_PROBABILITY.keys())[1])
        birth_year = GAME_START_DATE.year - age
        birth_date = date(birth_year, random.randint(1, 12), random.randint(1, 28))

        country_abbr = random.choices(countries_db, country_weights, k=1)[0]
        sab = random.choice(['M', 'F'])

        # 2. Determine Tier based on Age
        tier = get_tier_for_age(age)
        min_skill, max_skill = TIERS[tier]

        # 3. Select a name based on Country and SAB
        possible_names = names_db[country_abbr][sab]
        if not possible_names:
            possible_names = names_db['USA'][sab]  # Fallback to USA names

        first_name, last_name = random.choice(possible_names)

        # 4. Generate skills based on Tier
        player = {
            'player_id': i + 1,
            'first_name': first_name,
            'last_name': last_name,
            'country': country_abbr,
            'birth_date': birth_date.isoformat(),
            'sab': sab,
            'tier': tier,
            'sp': random.randint(min_skill, max_skill),
            'sa': random.randint(min_skill, max_skill),
            'gs': random.randint(min_skill, max_skill),
            'ref': random.randint(min_skill, max_skill),
            'sta': random.randint(min_skill, max_skill),
            'strg': random.randint(min_skill, max_skill),
            'clt': random.randint(min_skill, max_skill),
        }
        players_data.append(player)

    # 5. Write all data to players.csv
    try:
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as outfile:
            fieldnames = players_data[0].keys()
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(players_data)

        print(f"\nSuccessfully created '{OUTPUT_FILE}' with {len(players_data)} players.")
    except IOError:
        print(f"Error: Could not write to file '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    generate_world()