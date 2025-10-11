# stats_tracker.py
from players import Player
from collections import defaultdict


class StatsTracker:
    """A class to accumulate and calculate statistics for a single match."""

    def __init__(self, player1: Player, player2: Player):
        self.p1 = player1
        self.p2 = player2

        self.total_points = 0  # <-- ADD THIS LINE
        self.points_won = defaultdict(int)
        self.rally_lengths = []
        self.outcomes = defaultdict(int)

        self.serves_attempted = defaultdict(int)
        self.first_serve_faults = defaultdict(int)
        self.second_serve_points_faced = defaultdict(int)

        self.first_serve_points_won = defaultdict(int)
        self.second_serve_points_won = defaultdict(int)

        self.service_games_played = defaultdict(int)
        self.service_games_won = defaultdict(int)

        self.games_per_set = []
        self.tiebreaks_played = 0
        self.longest_rally = 0

    def record_point(self, server: Player, point_data: dict):
        """Records the outcome of a single point."""
        self.total_points += 1  # <-- ADD THIS LINE
        winner = point_data['winner']
        outcome = point_data['outcome']

        self.points_won[winner.name] += 1
        self.outcomes[outcome] += 1
        self.longest_rally = max(self.longest_rally, point_data['rally_length'])
        if point_data['rally_length'] > 0:
            self.rally_lengths.append(point_data['rally_length'])

        # Track serve-specific stats
        if outcome != "Double Fault":
            self.serves_attempted[server.name] += 1
            if not point_data['first_serve_fault']:  # 1st serve was in
                if winner == server:
                    self.first_serve_points_won[server.name] += 1
            else:  # 2nd serve was in
                self.first_serve_faults[server.name] += 1
                self.second_serve_points_faced[server.name] += 1
                if winner == server:
                    self.second_serve_points_won[server.name] += 1

    # ... (the rest of the file is unchanged) ...
    def record_service_game(self, server: Player, winner: Player):
        self.service_games_played[server.name] += 1
        if server == winner:
            self.service_games_won[server.name] += 1

    def record_set(self, p1_games, p2_games):
        self.games_per_set.append(p1_games + p2_games)

    def record_tiebreak(self):
        self.tiebreaks_played += 1

    def calculate_summary(self) -> dict:
        """Calculates final summary statistics for the match."""
        if self.total_points == 0: return {}

        p1_name, p2_name = self.p1.name, self.p2.name

        p1_fs_in = self.serves_attempted[p1_name] - self.first_serve_faults[p1_name]
        p2_fs_in = self.serves_attempted[p2_name] - self.first_serve_faults[p2_name]

        summary = {
            "Total Points": self.total_points,
            "Avg Rally Length": f"{(sum(self.rally_lengths) / len(self.rally_lengths)):.2f}" if self.rally_lengths else "0.00",
            "Longest Rally": self.longest_rally,
            "Tiebreaks Played": self.tiebreaks_played,
            "Avg Games per Set": f"{(sum(self.games_per_set) / len(self.games_per_set)):.2f}" if self.games_per_set else "0.00",
            f"{p1_name} Hold %": f"{(self.service_games_won[p1_name] / self.service_games_played[p1_name] * 100):.1f}%" if
            self.service_games_played[p1_name] > 0 else "N/A",
            f"{p2_name} Hold %": f"{(self.service_games_won[p2_name] / self.service_games_played[p2_name] * 100):.1f}%" if
            self.service_games_played[p2_name] > 0 else "N/A",
            f"{p1_name} 1st Srv Win %": f"{(self.first_serve_points_won[p1_name] / p1_fs_in * 100):.1f}%" if p1_fs_in > 0 else "N/A",
            f"{p2_name} 1st Srv Win %": f"{(self.first_serve_points_won[p2_name] / p2_fs_in * 100):.1f}%" if p2_fs_in > 0 else "N/A",
            f"{p1_name} 2nd Srv Win %": f"{(self.second_serve_points_won[p1_name] / self.second_serve_points_faced[p1_name] * 100):.1f}%" if
            self.second_serve_points_faced[p1_name] > 0 else "N/A",
            f"{p2_name} 2nd Srv Win %": f"{(self.second_serve_points_won[p2_name] / self.second_serve_points_faced[p2_name] * 100):.1f}%" if
            self.second_serve_points_faced[p2_name] > 0 else "N/A",
        }
        return summary