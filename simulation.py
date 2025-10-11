import random
from players import Player
from stats_tracker import StatsTracker
from configs.simulation_config import (
    VARIANCE_SIGMA_POINT, VARIANCE_SIGMA_FAULT, ACE_CEILING_FACTOR,
    POWER_PENALTY_RATE, POWER_THRESHOLD, DOUBLE_FAULT_TIERS,
    CLUTCH_MODIFIER_RATE, MIN_DF_RATE, FSSR_BASELINE_FLOOR, FSSR_SA_WEIGHT,
    MIN_DEF_FLOOR, WEIGHTING_SERVE_SP, WEIGHTING_SERVE_SA,
    WEIGHTING_RALLY_GS_OFFENSE, WEIGHTING_STR_OFFENSE,
    WEIGHTING_RALLY_GS_DEFENSE, WEIGHTING_REF_DEFENSE,
    RALLY_SUCCESS_THRESHOLD, SHOT_QUALITY_CEILING, MAX_RALLY_LENGTH,
    RALLY_FATIGUE_SCALAR, RALLY_FATIGUE_DIVISOR
)


# ----------------------------------------------------------------------
# Core Skill Checks (Updated for Fatigue via .get_skill())
# ----------------------------------------------------------------------

def serve_fault_check(server: Player) -> bool:
    sa = server.get_skill('serve_accuracy')
    sp = server.get_skill('serve_power')
    sa_component = FSSR_BASELINE_FLOOR + (sa * FSSR_SA_WEIGHT)
    power_difference = sp - POWER_THRESHOLD
    power_penalty = power_difference * POWER_PENALTY_RATE
    base_success_chance = sa_component - power_penalty
    base_success_chance = max(1, min(99, base_success_chance))
    actual_success_chance = random.gauss(mu=base_success_chance, sigma=VARIANCE_SIGMA_FAULT)
    actual_success_chance = max(0.0, min(100.0, actual_success_chance))
    return random.uniform(0, 100) > actual_success_chance


def second_serve_df_check(server: Player) -> bool:
    sa = server.get_skill('serve_accuracy')
    clt = server.clutch
    max_df_rate = 100.0
    for sa_threshold, df_rate in DOUBLE_FAULT_TIERS.items():
        if sa <= sa_threshold:
            max_df_rate = df_rate
            break
    clutch_modifier = (clt - 50) * CLUTCH_MODIFIER_RATE
    df_rate_final = max_df_rate - clutch_modifier
    df_rate_final = max(MIN_DF_RATE, min(99.0, df_rate_final))
    return random.uniform(0, 100) < df_rate_final


def serve_ace_check(server: Player, receiver: Player, is_second_serve: bool = False) -> bool:
    sp = server.get_skill('serve_power')
    sa = server.get_skill('serve_accuracy')
    ref = receiver.get_skill('reflex')
    server_attack_score = ((sp + sa) / 200.0) ** 2 * 100
    receiver_defense_multiplier = max(MIN_DEF_FLOOR, (100.0 - ref) / 100.0)
    ace_chance = server_attack_score * receiver_defense_multiplier * ACE_CEILING_FACTOR
    if is_second_serve:
        ace_chance /= 5.0
    ace_chance = max(0.001, ace_chance)
    return random.uniform(0, 100) < ace_chance


# ----------------------------------------------------------------------
# Shot Quality & Rally Logic (Updated for Stamina/Fatigue)
# ----------------------------------------------------------------------

def calculate_rally_quality(striker: Player, rally_length: int) -> float:
    gs = striker.get_skill('groundstroke')
    strg = striker.strength
    penalty_per_shot = (RALLY_FATIGUE_SCALAR - striker.stamina) / RALLY_FATIGUE_DIVISOR
    rally_penalty = min(0.3, rally_length * penalty_per_shot)
    bqs = (gs * WEIGHTING_RALLY_GS_OFFENSE) + (strg * WEIGHTING_STR_OFFENSE)
    bqs *= (1.0 - rally_penalty)
    asq = random.gauss(mu=bqs, sigma=VARIANCE_SIGMA_POINT)
    return max(1.0, min(SHOT_QUALITY_CEILING, asq))


def calculate_serve_quality(server: Player, is_second_serve: bool = False) -> float:
    sp = server.get_skill('serve_power')
    sa = server.get_skill('serve_accuracy')
    bqs = (sp * WEIGHTING_SERVE_SP) + (sa * WEIGHTING_SERVE_SA)
    if is_second_serve:
        bqs *= 0.80
    asq = random.gauss(mu=bqs, sigma=VARIANCE_SIGMA_POINT)
    return max(1.0, min(SHOT_QUALITY_CEILING, asq))


def rally_success_check(receiver: Player, incoming_shot_quality: float) -> bool:
    gs = receiver.get_skill('groundstroke')
    ref = receiver.get_skill('reflex')
    receiver_defensive_skill = (gs * WEIGHTING_RALLY_GS_DEFENSE) + (ref * WEIGHTING_REF_DEFENSE)
    skill_challenge = incoming_shot_quality - receiver_defensive_skill
    success_chance = RALLY_SUCCESS_THRESHOLD - (skill_challenge / SHOT_QUALITY_CEILING)
    success_chance = max(0.01, min(0.99, success_chance))
    setattr(receiver, 'last_success_chance', success_chance)
    return random.random() < success_chance


# ----------------------------------------------------------------------
# Point Simulation Logic (Now returns a data dictionary)
# ----------------------------------------------------------------------

def simulate_point(server: Player, receiver: Player) -> dict:
    """Simulates a single point, returning a dictionary of data."""
    current_striker, current_receiver = server, receiver
    first_serve_fault = False

    if serve_ace_check(current_striker, current_receiver, is_second_serve=False):
        return {'winner': current_striker, 'rally_length': 0, 'outcome': 'Ace', 'first_serve_fault': False}

    if not serve_fault_check(current_striker):
        first_serve_fault = True
        if second_serve_df_check(current_striker):
            return {'winner': current_receiver, 'rally_length': 0, 'outcome': 'Double Fault', 'first_serve_fault': True}
        if serve_ace_check(current_striker, current_receiver, is_second_serve=True):
            return {'winner': current_striker, 'rally_length': 0, 'outcome': 'Ace', 'first_serve_fault': True}
        incoming_shot_quality = calculate_serve_quality(current_striker, is_second_serve=True)
    else:
        incoming_shot_quality = calculate_serve_quality(current_striker, is_second_serve=False)

    current_striker, current_receiver = current_receiver, current_striker
    rally_length = 0
    while True:
        rally_length += 1
        if not rally_success_check(current_receiver, incoming_shot_quality):
            return {'winner': current_striker, 'rally_length': rally_length, 'outcome': 'Forced Error',
                    'first_serve_fault': first_serve_fault}

        new_shot_quality = calculate_rally_quality(current_receiver, rally_length)
        current_striker, current_receiver = current_receiver, current_striker
        incoming_shot_quality = new_shot_quality

        if rally_length >= MAX_RALLY_LENGTH:
            return {'winner': current_striker, 'rally_length': rally_length, 'outcome': 'Forced Error',
                    'first_serve_fault': first_serve_fault}


def simulate_point_logged(server: Player, receiver: Player) -> dict:
    """Simulates a point with logging, returning a dictionary of data."""
    log = []
    current_striker, current_receiver = server, receiver
    first_serve_fault = False
    log.append(f"\n===== NEW POINT: {server.name} SERVES =====")

    if serve_ace_check(current_striker, current_receiver, is_second_serve=False):
        log.append(f"*** POINT WIN: {current_striker.name} wins via First Serve ACE. ***")
        print('\n'.join(log))
        return {'winner': current_striker, 'rally_length': 0, 'outcome': 'Ace', 'first_serve_fault': False}

    if not serve_fault_check(current_striker):
        log.append(f"-> CHECK: 1ST SERVE: FAULT")
        first_serve_fault = True
        if second_serve_df_check(current_striker):
            log.append(f"*** POINT WIN: {current_receiver.name} wins via Double Fault. ***")
            print('\n'.join(log))
            return {'winner': current_receiver, 'rally_length': 0, 'outcome': 'Double Fault', 'first_serve_fault': True}
        log.append(f"-> CHECK: 2ND SERVE: IN")
        is_second_serve = True
        if serve_ace_check(current_striker, current_receiver, is_second_serve=True):
            log.append(f"*** POINT WIN: {current_striker.name} wins via Second Serve ACE. ***")
            print('\n'.join(log))
            return {'winner': current_striker, 'rally_length': 0, 'outcome': 'Ace', 'first_serve_fault': True}
        incoming_shot_quality = calculate_serve_quality(current_striker, is_second_serve=True)
    else:
        log.append(f"-> CHECK: 1ST SERVE: IN")
        is_second_serve = False
        incoming_shot_quality = calculate_serve_quality(current_striker, is_second_serve=False)

    log.append(f"--- RALLY START (Serve {1 if not is_second_serve else 2} IN) ---")
    log.append(f"STRIKER: {current_striker.name} | ASQ: {incoming_shot_quality:.2f}")
    current_striker, current_receiver = current_receiver, current_striker
    rally_length = 0
    while True:
        rally_length += 1
        if not rally_success_check(current_receiver, incoming_shot_quality):
            success_chance = getattr(current_receiver, 'last_success_chance')
            log.append(f"-> SHOT {rally_length} ({current_receiver.name} returning): {success_chance:.2%} -> FAILURE")
            log.append(f"*** POINT WIN: {current_striker.name} wins via Forced Error. ***")
            print('\n'.join(log))
            return {'winner': current_striker, 'rally_length': rally_length, 'outcome': 'Forced Error',
                    'first_serve_fault': first_serve_fault}

        success_chance = getattr(current_receiver, 'last_success_chance')
        log.append(f"-> SHOT {rally_length} ({current_receiver.name} returning): {success_chance:.2%} -> SUCCESS")
        new_shot_quality = calculate_rally_quality(current_receiver, rally_length)
        current_striker, current_receiver = current_receiver, current_striker
        incoming_shot_quality = new_shot_quality
        log.append(f"STRIKER: {current_striker.name} | ASQ: {incoming_shot_quality:.2f}")

        if rally_length >= MAX_RALLY_LENGTH:
            log.append(f"Rally has reached the {MAX_RALLY_LENGTH}-shot maximum length.")
            log.append(f"*** POINT WIN: {current_striker.name} wins via Rally Length Cap. ***")
            print('\n'.join(log))
            return {'winner': current_striker, 'rally_length': rally_length, 'outcome': 'Forced Error',
                    'first_serve_fault': first_serve_fault}


def simulate_point_wrapper(server, receiver):
    return simulate_point(server, receiver)


# ----------------------------------------------------------------------
# Game, Set, and Match Simulation (with Tiebreak and StatsTracker)
# ----------------------------------------------------------------------

def simulate_tiebreak(player1: Player, player2: Player, initial_server_index: int, tracker: StatsTracker,
                      verbose: bool = True) -> Player:
    """Simulates a single tiebreak to 7 points, win by two."""
    tracker.record_tiebreak()
    p1_points, p2_points = 0, 0
    if verbose:
        print("--- STARTING TIEBREAK ---")

    point_num = 1
    total_rally_length = 0

    while True:
        # Determine the server based on the unique tiebreak rotation
        if point_num == 1:
            server = player1 if initial_server_index == 0 else player2
        elif (point_num - 2) % 4 < 2:  # Points 2,3, 6,7, 10,11...
            server = player2 if initial_server_index == 0 else player1
        else:  # Points 4,5, 8,9, 12,13...
            server = player1 if initial_server_index == 0 else player2

        receiver = player1 if server == player2 else player2

        point_data = simulate_point_wrapper(server, receiver)

        # --- CORRECTED LINE ---
        # Pass the 'server' object along with the point_data
        tracker.record_point(server, point_data)

        total_rally_length += point_data['rally_length']

        if point_data['winner'] == player1:
            p1_points += 1
        else:
            p2_points += 1

        if verbose:
            print(f"Tiebreak Score: {p1_points}-{p2_points}")

        # Check for win condition
        if (p1_points >= 7 and p1_points >= p2_points + 2) or \
                (p2_points >= 7 and p2_points >= p1_points + 2):
            break

        point_num += 1

    player1.fatigue += total_rally_length
    player2.fatigue += total_rally_length

    return player1 if p1_points > p2_points else player2


def simulate_game(server: Player, receiver: Player, tracker: StatsTracker, verbose: bool = True) -> Player:
    """Simulates a full game of tennis, including fatigue accumulation."""
    score_map = {0: "0", 1: "15", 2: "30", 3: "40"}
    server_points, receiver_points = 0, 0
    if verbose: print(f"--- NEW GAME: {server.name} serving (Fatigue: {server.fatigue:.1f}) ---")

    while True:
        point_data = simulate_point_wrapper(server, receiver)

        # --- CORRECTED LINE ---
        # Pass the 'server' object along with the point_data to the tracker.
        tracker.record_point(server, point_data)

        winner, rally_length = point_data['winner'], point_data['rally_length']
        server.fatigue += rally_length
        receiver.fatigue += rally_length
        if winner == server:
            server_points += 1
        else:
            receiver_points += 1

        is_game_over = (server_points >= 4 and server_points >= receiver_points + 2) or \
                       (receiver_points >= 4 and receiver_points >= server_points + 2)

        if verbose and not is_game_over:
            if server_points >= 3 and receiver_points >= 3:
                if server_points == receiver_points:
                    score_string = f"Score: Deuce (40-40) (Rally: {rally_length})"
                elif server_points > receiver_points:
                    score_string = f"Score: Advantage {server.name} (Adv-40) (Rally: {rally_length})"
                else:
                    score_string = f"Score: Advantage {receiver.name} (40-Adv) (Rally: {rally_length})"
            else:
                s_score, r_score = score_map.get(server_points, "40"), score_map.get(receiver_points, "40")
                score_string = f"Score: ({s_score}-{r_score}) (Rally: {rally_length})"
            print(score_string)

        if is_game_over: break

    game_winner = server if server_points > receiver_points else receiver
    tracker.record_service_game(server, game_winner)

    if verbose: print(f"\n--- GAME WON BY: {game_winner.name} ---")
    game_winner.games_won += 1
    return game_winner


def simulate_set(player1: Player, player2: Player, initial_server_index: int, tracker: StatsTracker,
                 verbose: bool = True) -> Player:
    player1.games_won, player2.games_won = 0, 0
    server_index = initial_server_index
    if verbose: print(f"\n------------------ STARTING NEW SET ------------------")
    while True:
        if (player1.games_won >= 6 and player1.games_won >= player2.games_won + 2) or (
                player2.games_won >= 6 and player2.games_won >= player1.games_won + 2):
            break
        if player1.games_won == 6 and player2.games_won == 6:
            tiebreak_winner = simulate_tiebreak(player1, player2, server_index, tracker, verbose)
            tiebreak_winner.games_won += 1
            break
        server, receiver = (player1, player2) if server_index == 0 else (player2, player1)
        game_winner = simulate_game(server, receiver, tracker, verbose=verbose)
        if verbose: print(f"--> Set Score: {player1.name} {player1.games_won} - {player2.games_won} {player2.name}")
        server_index = 1 - server_index
    set_winner = player1 if player1.games_won > player2.games_won else player2
    tracker.record_set(player1.games_won, player2.games_won)
    if verbose: print(f"--- SET WON BY: {set_winner.name} ({player1.games_won}-{player2.games_won}) ---")
    set_winner.sets_won += 1
    return set_winner


def simulate_match(player1: Player, player2: Player, num_sets: int = 3, verbose: bool = True) -> tuple[
    Player, StatsTracker]:
    tracker = StatsTracker(player1, player2)
    player1.sets_won, player2.sets_won = 0, 0
    server_index = 0
    sets_to_win = (num_sets // 2) + 1
    while player1.sets_won < sets_to_win and player2.sets_won < sets_to_win:
        set_winner = simulate_set(player1, player2, server_index, tracker, verbose=verbose)
        if verbose: print(f"\n==> Match Score: {player1.name} {player1.sets_won} - {player2.sets_won} {player2.name}")
        server_index = 1 - server_index
    match_winner = player1 if player1.sets_won == sets_to_win else player2
    if verbose:
        print("\n=======================================================")
        print(f"| 🏆 MATCH COMPLETE! Winner is {match_winner.name} 🏆 |")
        print(f"| Final Score: {player1.sets_won} - {player2.sets_won} |")
        print("=======================================================")
    return match_winner, tracker