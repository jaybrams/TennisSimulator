# test.py

import random
from players import Player
import simulation # Import the whole module
from simulation import simulate_point_logged
from stats_tracker import StatsTracker

TIER_RANGES = {
    "Elite": (86, 100),
    "Pro": (71, 85),
    "Challenger": (51, 70),
    "Futures": (31, 50),
    "Beginner": (1, 30),
}


def create_player(name: str, tier: str) -> Player:
    """Creates a randomized player with skills based on the specified tier."""
    if tier not in TIER_RANGES:
        raise ValueError(f"Unknown tier provided: {tier}")

    min_skill, max_skill = TIER_RANGES[tier]

    # Randomize all skills to be within the tier's range
    skills = {
        'sp': random.randint(min_skill, max_skill),
        'sa': random.randint(min_skill, max_skill),
        'gs': random.randint(min_skill, max_skill),
        'ref': random.randint(min_skill, max_skill),
        'sta': random.randint(min_skill, max_skill),
        'strg': random.randint(min_skill, max_skill),
        'clt': random.randint(min_skill, max_skill),
    }

    # The Player class now handles the OVR calculation automatically
    return Player(name=name, **skills)

# Helper function to simulate a point, using the logging version
def simulate_point_wrapper(server, receiver):
    return simulate_point_logged(server, receiver)

# single match simulation to review line by line
if __name__ == "__main__":
    simulation.simulate_point_wrapper = simulation.simulate_point_logged

    player_A = create_player("Rafael Nadal (Pro)", "Pro")
    player_B = create_player("Roger Federer (Pro)", "Pro")

    print("\n=======================================================")
    print(f"|      STARTING SINGLE MATCH SIMULATION             |")
    print("=======================================================")
    print(player_A)
    print(player_B)

    # simulate_match now returns the winner AND the tracker object
    winner, match_tracker = simulation.simulate_match(
        player_A,
        player_B,
        num_sets=5,
        verbose=True
    )

    # After the match, display the final stats
    if match_tracker:
        match_tracker.display_summary()

