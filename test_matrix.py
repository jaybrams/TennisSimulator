import csv
import random
import os
from collections import defaultdict
from tqdm import tqdm

import simulation
from players import Player

# --- CONFIGURATION ---
PLAYER_DATA_FILE = os.path.join("data", "players.csv")
BASE_OVR = 80  # The OVR of the player we are testing
TESTING_RANGE = 5  # Test against OVRs +/- this amount (e.g., 80 vs 75, 80 vs 76...)
SIMULATIONS_PER_PAIRING = 5000  # Number of matches per OVR pairing
NUM_SETS = 3  # 3 for standard, 5 for Grand Slam


# --- END CONFIGURATION ---

def load_all_players(filename: str) -> list[Player]:
    """Loads a flat list of all Player objects from the specified CSV file."""
    players = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                players.append(Player(
                    player_id=int(row['player_id']),
                    name=f"{row['first_name']} {row['last_name']}", country=row['country'],
                    sp=int(row['sp']), sa=int(row['sa']), gs=int(row['gs']),
                    ref=int(row['ref']), sta=int(row['sta']), strg=int(row['strg']), clt=int(row['clt'])
                ))
    except FileNotFoundError:
        print(f"Error: Player data file not found at '{filename}'.")
    return players


def main():
    """Main function to run the OVR matchup matrix simulation."""
    simulation.simulate_point_wrapper = simulation.simulate_point

    all_players = load_all_players(PLAYER_DATA_FILE)
    if not all_players:
        return

    players_by_ovr = defaultdict(list)
    for p in all_players:
        players_by_ovr[p.overall].append(p)

    opponent_ovrs = range(BASE_OVR - TESTING_RANGE, BASE_OVR + TESTING_RANGE + 1)
    all_results = []

    print("=======================================================")
    print(f"|  STARTING OVR MATCHUP MATRIX ({SIMULATIONS_PER_PAIRING} SIMS EACH)  |")
    print(f"|  Testing Base OVR: {BASE_OVR}                         |")
    print("=======================================================")

    for opp_ovr in opponent_ovrs:
        matchup_key = f"{BASE_OVR} OVR vs. {opp_ovr} OVR"

        base_players = players_by_ovr[BASE_OVR]
        opp_players = players_by_ovr[opp_ovr]

        if not base_players or not opp_players:
            print(f"Skipping {matchup_key}: Not enough players with the required OVR in players.csv.")
            continue

        # In same-OVR matchups, we need at least 2 players to run a valid test
        if BASE_OVR == opp_ovr and len(base_players) < 2:
            print(f"Skipping {matchup_key}: Need at least 2 players with OVR {BASE_OVR} to simulate.")
            continue

        win_counts = {'base': 0, 'opponent': 0}

        for _ in tqdm(range(SIMULATIONS_PER_PAIRING), desc=f"Simulating {matchup_key}"):
            p1 = random.choice(base_players)
            p2 = random.choice(opp_players)

            # --- NEW: Check to prevent a player from playing themself ---
            if p1.id == p2.id:
                # Re-pick p2 until it's a different player
                while p2.id == p1.id:
                    p2 = random.choice(opp_players)

            winner, _ = simulation.simulate_match(p1, p2, num_sets=NUM_SETS, verbose=False)

            if winner.id == p1.id:
                win_counts['base'] += 1
            else:
                win_counts['opponent'] += 1

        base_win_pct = (win_counts['base'] / SIMULATIONS_PER_PAIRING) * 100
        opp_win_pct = (win_counts['opponent'] / SIMULATIONS_PER_PAIRING) * 100
        all_results.append((matchup_key, base_win_pct, opp_win_pct))

    output_string = generate_output_string(all_results)
    print(output_string)


def generate_output_string(results: list) -> str:
    """Formats the final results matrix into a printable string."""
    lines = [
        "\n=======================================================",
        "|            OVR MATCHUP MATRIX RESULTS             |",
        "======================================================="
    ]
    for matchup_key, base_pct, opp_pct in results:
        lines.append(f"- {matchup_key:<18}: {base_pct:.1f}% / {opp_pct:.1f}%")
    lines.append("=======================================================")
    return "\n".join(lines)


if __name__ == '__main__':
    main()