import csv
import random
import os
from datetime import date, timedelta
from collections import defaultdict

from players import Player
from stats_tracker import StatsTracker
from configs.tournaments_m_db import MENS_PRO_TOUR_DB
from configs.tournaments_challenger_db import MENS_CHALLENGER_TOUR_DB


class GameSession:
    """
    Manages the state and progression of a single career mode save file.
    """

    def __init__(self, start_date: date, player_data_file: str):
        print("Initializing new game session...")

        # Find the Monday of the start week to align the calendar
        start_weekday = start_date.weekday()
        actual_start_monday = start_date - timedelta(days=start_weekday)

        self.start_date = actual_start_monday
        self.current_date = actual_start_monday

        self.all_players = self._load_all_players(player_data_file)
        print(f"Loaded {len(self.all_players)} players into the game world.")

        self.human_player = None
        if self.all_players:
            pro_players = [p for p in self.all_players if 71 <= p.overall <= 85]
            if pro_players:
                self.human_player = random.choice(pro_players)
                print(f"Human player set to: {self.human_player.name}")

        self.year_schedule = self.generate_annual_schedule(self.start_date.year)
        print(f"Generated schedule for {self.start_date.year}.")

    def _load_all_players(self, filename: str) -> list[Player]:
        """Loads a flat list of all Player objects from the specified CSV file."""
        players = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    players.append(Player(
                        player_id=int(row['player_id']),
                        name=f"{row['first_name']} {row['last_name']}", country=row['country'],
                        birth_date=row['birth_date'], sab=row['sab'],
                        sp=int(row['sp']), sa=int(row['sa']), gs=int(row['gs']),
                        ref=int(row['ref']), sta=int(row['sta']), strg=int(row['strg']), clt=int(row['clt'])
                    ))
        except FileNotFoundError:
            print(f"Error: Player data file not found at '{filename}'.")
        return players

    def _generate_generic_futures(self, week: int, country: str) -> dict:
        """Helper to create a single generic Futures tournament."""
        level = random.choice([15, 25])
        surface = random.choice(['Hard', 'Clay', 'Hard (Indoor)'])
        return {
            'id': f"FUT_{country}_{week}_{level}", 'name': f"{country} F{week}", 'city': 'Generic',
            'country': country, 'level': level, 'weeks': [week], 'surface': surface, 'status': 'Generated',
            'draw_size': 32
        }

    def generate_annual_schedule(self, year: int) -> dict:
        """Generates a 52-week schedule for a given year."""
        schedule = defaultdict(list)

        for tourney in MENS_PRO_TOUR_DB:
            if '_P' not in tourney['id']:
                for week in tourney['weeks']:
                    schedule[week].append(tourney)

        for week in range(1, 53):
            num_challengers = random.randint(3, 5)
            challenger_pool = random.sample(MENS_CHALLENGER_TOUR_DB, k=num_challengers)
            for tourney in challenger_pool:
                t_copy = tourney.copy()
                t_copy['weeks'] = [week]
                schedule[week].append(t_copy)

        all_countries = list(set(t['country'] for t in MENS_PRO_TOUR_DB if t['country']))
        for week in range(1, 53):
            num_futures = random.randint(4, 7)
            for _ in range(num_futures):
                country = random.choice(all_countries)
                schedule[week].append(self._generate_generic_futures(week, country))

        return schedule

    def run(self):
        """Starts and runs the main game loop based on the 'Office as the Hub' model."""
        self._exit_game = False
        while not self._exit_game:
            current_week = self.current_date.isocalendar()[1]
            self._display_weekly_header()

            if current_week in self.human_player.schedule:
                self._handle_scheduled_week(current_week)
            else:
                self._handle_free_week()

            if not self._exit_game:
                self.current_date += timedelta(weeks=1)
                print("\n" + "=" * 55)

        print("Exiting game.")

    def _handle_scheduled_week(self, week_num):
        """Logic for a week where the player is scheduled for a tournament."""
        tournament_id = self.human_player.schedule[week_num]
        print(f"You are scheduled to play in: {tournament_id}")

        while True:
            choice = input("Options: [P]lay Tournament, [W]ithdraw, [O]ffice: ").lower()
            if choice == 'p':
                self._handle_play_tournament()
                break
            elif choice == 'w':
                self._handle_withdraw(week_num)
                break
            elif choice == 'o':
                self._handle_office()
                self._display_weekly_header()
                print(f"You are scheduled to play in: {tournament_id}")
            else:
                print("Invalid choice.")

    def _handle_free_week(self):
        """Logic for a week where the player has no scheduled tournament."""
        while True:
            choice = input("Weekly Options: [T]rain, [R]est, [O]ffice, [Q]uit: ").lower()
            if choice == 't':
                self._handle_training()
                break
            elif choice == 'r':
                self._handle_rest()
                break
            elif choice == 'o':
                self._handle_office()
                self._display_weekly_header()
            elif choice in ['q', 'quit', 'exit']:
                self._exit_game = True
                break
            else:
                print("Invalid choice.")

    def _display_weekly_header(self):
        """Displays the current date and player status."""
        week_num = self.current_date.isocalendar()[1]
        print(f"\nCurrent Date: {self.current_date.strftime('%A, %B %d, %Y')} (Week {week_num})")

        energy_bar = '█' * int(self.human_player.energy / 10)
        energy_padding = '-' * (10 - int(self.human_player.energy / 10))
        form_str = f"+{self.human_player.match_form:.1f}" if self.human_player.match_form > 0 else f"{self.human_player.match_form:.1f}"
        print(
            f"Player Status: Energy [{energy_bar}{energy_padding}] {self.human_player.energy:.0f}% | Match Form: [{form_str}]")

    def _handle_office(self):
        """Acts as the hub for all long-term planning. Does not advance the week."""
        while True:
            print("\n--- The Office ---")
            print("Options: [R]egister for Tournament, [V]iew Schedule, [W]ithdraw, [E]xit Office")
            choice = input("Enter your choice: ").lower()
            if choice == 'r':
                self._handle_tournament_registration()
            elif choice == 'v':
                self._display_player_schedule()
            elif choice == 'w':
                self._handle_early_withdraw()
            elif choice == 'e':
                break
            else:
                print("Invalid choice.")

    def _handle_tournament_registration(self):
        """Handles the logic for registering for future tournaments."""
        while True:
            try:
                week_str = input("\nEnter week number to plan for (4-26 weeks ahead), or [c]ancel: ").lower()
                if week_str == 'c': break

                target_week_num = int(week_str)

                # --- NEW: Logical Week Calculation ---
                current_iso = self.current_date.isocalendar()
                current_week = current_iso.week

                # Calculate the difference in weeks, accounting for year change
                if target_week_num < current_week:  # Assumes next year
                    week_difference = (52 - current_week) + target_week_num
                else:
                    week_difference = target_week_num - current_week

                if not 4 <= week_difference <= 26:
                    print("Invalid week. You can only register for tournaments 4 to 26 weeks in the future.")
                    continue

                tournaments = sorted(self.year_schedule.get(target_week_num, []), key=lambda t: t['level'],
                                     reverse=True)
                if not tournaments:
                    print(f"No tournaments found for Week {target_week_num}.")
                    continue

                print(f"\n--- Tournaments for Week {target_week_num} ---")
                for i, tourney in enumerate(tournaments):
                    print(
                        f"  {i + 1}. [{tourney['level']}] {tourney['name']} ({tourney['city']}) | {tourney['surface']}")

                choice_str = input("Select a tournament to register for, or [c]ancel: ").lower()
                if choice_str == 'c': continue

                choice_idx = int(choice_str) - 1
                if 0 <= choice_idx < len(tournaments):
                    chosen_tourney = tournaments[choice_idx]
                    is_conflict = False
                    for week in chosen_tourney['weeks']:
                        if week in self.human_player.schedule:
                            is_conflict = True
                            print(f"Registration failed: You are already scheduled for an event in Week {week}.")
                            break
                    if not is_conflict:
                        for week in chosen_tourney['weeks']:
                            self.human_player.schedule[week] = chosen_tourney['id']
                        print(f"\nSuccessfully registered for {chosen_tourney['name']}!")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Invalid input. Please enter a number.")

            another = input("Register for another tournament? (y/n): ").lower()
            if another != 'y':
                break

    def _display_player_schedule(self):
        """Prints a list of the player's upcoming scheduled tournaments."""
        print("\n--- Your Upcoming Schedule ---")
        if not self.human_player.schedule:
            print("You have no tournaments scheduled.")
            return

        # Sort the schedule by week number before printing
        sorted_weeks = sorted(self.human_player.schedule.keys())

        # The logic to prevent duplicates has been removed.
        for week in sorted_weeks:
            tourney_id = self.human_player.schedule[week]
            print(f"  Week {week}: {tourney_id}")

    def _handle_early_withdraw(self):
        print("\nFunctionality to withdraw from future tournaments will be added here.")

    def _handle_play_tournament(self):
        print("\n[ACTION]: Simulating tournament week...")
        player = self.human_player
        player.energy -= 30
        player.match_form += 3
        if random.random() < 0.20:
            print("Your Match Form has reset to the baseline after the tournament.")
            player.match_form = random.uniform(-1, 1)
        player.energy = max(0, player.energy)
        player.match_form = min(10, player.match_form)
        # TODO: If player loses early in a multi-week event, free up their subsequent weeks.

    def _handle_training(self):
        print("\n[ACTION]: Simulating a week of focused training...")
        player = self.human_player
        player.energy += 15
        player.match_form += 1
        player.energy = min(100, player.energy)
        player.match_form = min(10, player.match_form)

    def _handle_rest(self):
        print("\n[ACTION]: Simulating a week of rest and recovery...")
        player = self.human_player
        player.energy += 30
        player.match_form -= 1
        player.energy = min(100, player.energy)
        player.match_form = max(-10, player.match_form)

    def _handle_withdraw(self, week_num):
        print("\n[ACTION]: You have withdrawn from the tournament. This week is now free.")
        del self.human_player.schedule[week_num]
        # TODO: Add penalties for late withdrawal (fan anger, sponsorship loss, etc.)

    def display_week_schedule(self, week_num: int):
        """Prints a formatted schedule for a given week."""
        print(f"\n--- WEEK {week_num} SCHEDULE ---")
        if week_num not in self.year_schedule or not self.year_schedule[week_num]:
            print("  - No Pro or Challenger events scheduled.")
            return
        sorted_tournaments = sorted(self.year_schedule[week_num], key=lambda t: t['level'], reverse=True)
        for tourney in sorted_tournaments:
            print(f"  - [{tourney['level']}] {tourney['name']} | {tourney['surface']}")