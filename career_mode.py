import os
from datetime import date
from game_session import GameSession

# --- Game Configuration ---
PLAYER_DATA_FILE = os.path.join("data", "players.csv")
START_DATE = date(2025, 12, 1)

if __name__ == "__main__":
    session = GameSession(start_date=START_DATE, player_data_file=PLAYER_DATA_FILE)
    session.run()