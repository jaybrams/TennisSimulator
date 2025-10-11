import csv
import random

# --- CONFIGURATION ---
OUTPUT_FILE = 'data/players.csv'
TIERS = {
    "Elite": (86, 100),
    "Pro": (71, 85),
    "Challenger": (51, 70),
    "Futures": (31, 50),
    "Beginner": (1, 30),
}
PLAYERS_PER_TIER = 20

# --- DATA POOLS ---
FIRST_NAMES = ["John", "Carlos", "Jannik", "Daniil", "Andrey", "Alex", "Casper", "Hubert", "Stefanos", "Taylor",
               "Grigor", "Holger", "Ben", "Felix", "Frances", "Gael", "Matteo", "Denis", "Kei", "Stan"]
LAST_NAMES = ["Isner", "Alcaraz", "Sinner", "Medvedev", "Rublev", "De Minaur", "Ruud", "Hurkacz", "Tsitsipas", "Fritz",
              "Dimitrov", "Rune", "Shelton", "Auger-Aliassime", "Tiafoe", "Monfils", "Berrettini", "Shapovalov",
              "Nishikori", "Wawrinka"]
COUNTRIES = {
    "USA": "United States", "ESP": "Spain", "ITA": "Italy", "RUS": "Russia", "AUS": "Australia",
    "NOR": "Norway", "POL": "Poland", "GRE": "Greece", "BUL": "Bulgaria", "DEN": "Denmark",
    "CAN": "Canada", "FRA": "France", "JPN": "Japan", "SUI": "Switzerland", "SRB": "Serbia",
    "GER": "Germany", "GBR": "Great Britain", "ARG": "Argentina", "CRO": "Croatia", "CHI": "Chile"
}


def generate_players():
    """Generates a list of 100 random players and saves them to a CSV file."""
    players_data = []
    player_id_counter = 1

    print("Generating player data...")

    for tier, (min_skill, max_skill) in TIERS.items():
        for _ in range(PLAYERS_PER_TIER):
            country_abbr = random.choice(list(COUNTRIES.keys()))

            player = {
                'player_id': player_id_counter,
                'first_name': random.choice(FIRST_NAMES),
                'last_name': random.choice(LAST_NAMES),
                'country': country_abbr,
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
            player_id_counter += 1

    # Write the data to the CSV file
    try:
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            fieldnames = players_data[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(players_data)

        print(f"Successfully created '{OUTPUT_FILE}' with {len(players_data)} players.")

    except IOError:
        print(f"Error: Could not write to file '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    generate_players()