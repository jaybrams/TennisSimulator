import csv
import random
import time
import os
from datetime import datetime
from collections import defaultdict
from tqdm import tqdm

import simulation
from players import Player
from stats_tracker import StatsTracker

# --- SIMULATION CONFIGURATION ---
# Define folder structure and file paths
DATA_FOLDER = "data"
SIM_STATS_FOLDER = "sim_stats"
VERBOSE_LOG_FOLDER = "verboselog"

PLAYER_DATA_FILE = os.path.join(DATA_FOLDER, "players.csv")
NUM_SETS = 3
SIMULATIONS_PER_MATCHUP = 5000


# --- END CONFIGURATION ---


def load_players_from_csv(filename: str) -> dict:
    """Loads players from a CSV and groups them by tier."""
    players_by_tier = defaultdict(list)
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                player = Player(
                    player_id=int(row['player_id']),
                    name=f"{row['first_name']} {row['last_name']}", country=row['country'],
                    sp=int(row['sp']), sa=int(row['sa']), gs=int(row['gs']),
                    ref=int(row['ref']), sta=int(row['sta']), strg=int(row['strg']), clt=int(row['clt'])
                )
                players_by_tier[row['tier']].append(player)
    except FileNotFoundError:
        print(f"Error: Player data file not found at '{filename}'.")
        return {}
    return players_by_tier


def main():
    """Main function to run the batch simulation and generate results."""
    simulation.simulate_point_wrapper = simulation.simulate_point

    # Create output directories if they don't exist
    os.makedirs(SIM_STATS_FOLDER, exist_ok=True)
    os.makedirs(VERBOSE_LOG_FOLDER, exist_ok=True)

    players_by_tier = load_players_from_csv(PLAYER_DATA_FILE)
    if not players_by_tier:
        return

    tiers = ["Elite", "Pro", "Challenger", "Futures", "Beginner"]
    matchups_to_run = []
    for i in range(len(tiers)):
        for j in range(i, len(tiers)):
            matchups_to_run.append((tiers[i], tiers[j]))

    all_results = []
    start_time = time.time()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Set up the detailed CSV log file
    csv_filename = os.path.join(VERBOSE_LOG_FOLDER, f"match_results_log_{timestamp}.csv")
    csv_header = ['match_id', 'p1_id', 'p1_tier', 'p2_id', 'p2_tier', 'winner_id', 'final_score', 'num_sets_played']

    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=csv_header)
        csv_writer.writeheader()
        match_id_counter = 1

        print("=======================================================")
        print(f"|  STARTING BATCH SIMULATION ({SIMULATIONS_PER_MATCHUP} MATCHES PER PAIRING)  |")
        print("=======================================================")

        for tier1, tier2 in matchups_to_run:
            matchup_key = f"{tier1} vs. {tier2}"
            agg_stats = defaultdict(float)

            for _ in tqdm(range(SIMULATIONS_PER_MATCHUP), desc=f"Simulating {matchup_key}"):
                p1_obj = random.choice(players_by_tier[tier1])
                p2_obj = random.choice(players_by_tier[tier2])

                # This defines the name variables needed for stats aggregation
                p1_name, p2_name = p1_obj.name, p2_obj.name

                winner, tracker = simulation.simulate_match(p1_obj, p2_obj, num_sets=NUM_SETS, verbose=False)

                csv_writer.writerow({
                    'match_id': match_id_counter, 'p1_id': p1_obj.id, 'p1_tier': tier1,
                    'p2_id': p2_obj.id, 'p2_tier': tier2, 'winner_id': winner.id,
                    'final_score': f"{p1_obj.sets_won}-{p2_obj.sets_won}" if winner.id == p1_obj.id else f"{p2_obj.sets_won}-{p1_obj.sets_won}",
                    'num_sets_played': p1_obj.sets_won + p2_obj.sets_won
                })
                match_id_counter += 1

                if winner.name == p1_name:
                    agg_stats[f'{tier1}_wins'] += 1
                else:
                    agg_stats[f'{tier2}_wins'] += 1

                # Aggregate all stats
                agg_stats['total_points'] += tracker.total_points
                agg_stats['sum_rally_lengths'] += sum(tracker.rally_lengths)
                agg_stats['total_rallies'] += len(tracker.rally_lengths)
                agg_stats['longest_rally'] = max(agg_stats['longest_rally'], tracker.longest_rally)
                agg_stats['tiebreaks'] += tracker.tiebreaks_played
                agg_stats['total_sets'] += len(tracker.games_per_set)
                agg_stats['total_games'] += sum(tracker.games_per_set)
                agg_stats['aces'] += tracker.outcomes.get('Ace', 0)
                agg_stats['double_faults'] += tracker.outcomes.get('Double Fault', 0)
                agg_stats['total_serves_attempted'] += sum(tracker.serves_attempted.values())
                agg_stats['total_first_serve_faults'] += sum(tracker.first_serve_faults.values())
                agg_stats[f'{tier1}_service_games_played'] += tracker.service_games_played.get(p1_name, 0)
                agg_stats[f'{tier2}_service_games_played'] += tracker.service_games_played.get(p2_name, 0)
                agg_stats[f'{tier1}_service_games_won'] += tracker.service_games_won.get(p1_name, 0)
                agg_stats[f'{tier2}_service_games_won'] += tracker.service_games_won.get(p2_name, 0)
                agg_stats[f'{tier1}_1st_serves_in'] += tracker.serves_attempted.get(p1_name,
                                                                                    0) - tracker.first_serve_faults.get(
                    p1_name, 0)
                agg_stats[f'{tier2}_1st_serves_in'] += tracker.serves_attempted.get(p2_name,
                                                                                    0) - tracker.first_serve_faults.get(
                    p2_name, 0)
                agg_stats[f'{tier1}_1st_serve_won'] += tracker.first_serve_points_won.get(p1_name, 0)
                agg_stats[f'{tier2}_1st_serve_won'] += tracker.first_serve_points_won.get(p2_name, 0)
                agg_stats[f'{tier1}_2nd_serves_faced'] += tracker.second_serve_points_faced.get(p1_name, 0)
                agg_stats[f'{tier2}_2nd_serves_faced'] += tracker.second_serve_points_faced.get(p2_name, 0)
                agg_stats[f'{tier1}_2nd_serve_won'] += tracker.second_serve_points_won.get(p1_name, 0)
                agg_stats[f'{tier2}_2nd_serve_won'] += tracker.second_serve_points_won.get(p2_name, 0)

            # Calculate final stats for the matchup
            total_matches = SIMULATIONS_PER_MATCHUP
            final_stats = {
                "Matchup": matchup_key,
                f"{tier1} Win %": f"{(agg_stats[f'{tier1}_wins'] / total_matches) * 100:.1f}%",
                f"{tier2} Win %": f"{(agg_stats[f'{tier2}_wins'] / total_matches) * 100:.1f}%",
                "1st Serve In %": f"{((agg_stats['total_serves_attempted'] - agg_stats['total_first_serve_faults']) / agg_stats['total_serves_attempted']) * 100:.1f}%" if
                agg_stats['total_serves_attempted'] > 0 else "N/A",
                "Ace % (of all points)": f"{(agg_stats['aces'] / agg_stats['total_points']) * 100:.2f}%" if agg_stats[
                                                                                                                'total_points'] > 0 else "N/A",
                "Double Fault % (of all points)": f"{(agg_stats['double_faults'] / agg_stats['total_points']) * 100:.2f}%" if
                agg_stats['total_points'] > 0 else "N/A",
                "Avg Match Duration (Points)": f"{agg_stats['total_points'] / total_matches:.1f}",
                "Avg Games / Set": f"{agg_stats['total_games'] / agg_stats['total_sets']:.2f}" if agg_stats[
                                                                                                      'total_sets'] > 0 else "0",
                "Avg Rally Length": f"{agg_stats['sum_rally_lengths'] / agg_stats['total_rallies']:.2f}" if agg_stats[
                                                                                                                'total_rallies'] > 0 else "0",
                "Longest Rally (in any match)": int(agg_stats['longest_rally']),
                "Tiebreak %": f"{(agg_stats['tiebreaks'] / agg_stats['total_sets']) * 100:.1f}%" if agg_stats[
                                                                                                        'total_sets'] > 0 else "0.0%",
                f"{tier1} Hold %": f"{(agg_stats[f'{tier1}_service_games_won'] / agg_stats[f'{tier1}_service_games_played'] * 100):.1f}%" if
                agg_stats[f'{tier1}_service_games_played'] > 0 else "N/A",
                f"{tier2} Hold %": f"{(agg_stats[f'{tier2}_service_games_won'] / agg_stats[f'{tier2}_service_games_played'] * 100):.1f}%" if
                agg_stats[f'{tier2}_service_games_played'] > 0 else "N/A",
                f"{tier1} 1st Srv Win %": f"{(agg_stats[f'{tier1}_1st_serve_won'] / agg_stats[f'{tier1}_1st_serves_in'] * 100):.1f}%" if
                agg_stats[f'{tier1}_1st_serves_in'] > 0 else "N/A",
                f"{tier2} 1st Srv Win %": f"{(agg_stats[f'{tier2}_1st_serve_won'] / agg_stats[f'{tier2}_1st_serves_in'] * 100):.1f}%" if
                agg_stats[f'{tier2}_1st_serves_in'] > 0 else "N/A",
                f"{tier1} 2nd Srv Win %": f"{(agg_stats[f'{tier1}_2nd_serve_won'] / agg_stats[f'{tier1}_2nd_serves_faced'] * 100):.1f}%" if
                agg_stats[f'{tier1}_2nd_serves_faced'] > 0 else "N/A",
                f"{tier2} 2nd Srv Win %": f"{(agg_stats[f'{tier2}_2nd_serve_won'] / agg_stats[f'{tier2}_2nd_serves_faced'] * 100):.1f}%" if
                agg_stats[f'{tier2}_2nd_serves_faced'] > 0 else "N/A",
            }
            all_results.append(final_stats)

    # Generate final output
    output_string = "\n".join(
        generate_output_string(all_results, len(matchups_to_run) * SIMULATIONS_PER_MATCHUP, time.time() - start_time))
    print(output_string)

    output_filename = os.path.join(SIM_STATS_FOLDER, f"simulation_summary_{timestamp}.txt")
    with open(output_filename, 'w') as f:
        f.write(output_string)

    print(f"\nSummary report saved to '{output_filename}'")
    print(f"Detailed match log saved to '{csv_filename}'")


def generate_output_string(all_results, total_sims, exec_time):
    lines = [
        "=======================================================",
        "|                BATCH SIMULATION RESULTS             |",
        "=======================================================",
        f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Total Matches Simulated: {total_sims}",
        f"Execution Time: {exec_time:.2f} seconds",
        "-" * 55
    ]
    for res in all_results:
        lines.append(f"\n--- {res['Matchup']} ---")
        for key, value in res.items():
            if key != "Matchup":
                lines.append(f"{key:<35}: {value}")
    return lines


if __name__ == '__main__':
    main()