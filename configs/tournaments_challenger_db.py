# configs/tournaments_challenger_db.py

"""
Defines the master database of all possible Challenger tour tournaments.
These are all 'Rotating' and will be randomly selected to fill the calendar each week.

Challenger Levels: 175, 125, 100, 75, 50
"""

MENS_CHALLENGER_TOUR_DB = [
    # ======================================================
    # Challenger 175 Pool (5 Tournaments)
    # ======================================================
    {'id': 'CH175_01', 'name': 'Phoenix', 'city': 'Phoenix', 'country': 'USA', 'level': 175, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH175_02', 'name': 'Turin', 'city': 'Turin', 'country': 'ITA', 'level': 175, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH175_03', 'name': 'Bordeaux', 'city': 'Bordeaux', 'country': 'FRA', 'level': 175, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH175_04', 'name': 'Cagliari', 'city': 'Cagliari', 'country': 'ITA', 'level': 175, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH175_05', 'name': 'Aix-en-Provence', 'city': 'Aix-en-Provence', 'country': 'FRA', 'level': 175,
     'surface': 'Clay', 'draw_size': 32},

    # ======================================================
    # Challenger 125 Pool (10 Tournaments)
    # ======================================================
    {'id': 'CH125_01', 'name': 'Vancouver', 'city': 'Vancouver', 'country': 'CAN', 'level': 125, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH125_02', 'name': 'Busan', 'city': 'Busan', 'country': 'KOR', 'level': 125, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH125_03', 'name': 'Canberra', 'city': 'Canberra', 'country': 'AUS', 'level': 125, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH125_04', 'name': 'Szczecin', 'city': 'Szczecin', 'country': 'POL', 'level': 125, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH125_05', 'name': 'Genoa', 'city': 'Genoa', 'country': 'ITA', 'level': 125, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH125_06', 'name': 'Orleans', 'city': 'Orleans', 'country': 'FRA', 'level': 125, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH125_07', 'name': 'Monterrey', 'city': 'Monterrey', 'country': 'MEX', 'level': 125, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH125_08', 'name': 'Nottingham', 'city': 'Nottingham', 'country': 'GBR', 'level': 125, 'surface': 'Grass',
     'draw_size': 32},
    {'id': 'CH125_09', 'name': 'Ilkley', 'city': 'Ilkley', 'country': 'GBR', 'level': 125, 'surface': 'Grass',
     'draw_size': 32},
    {'id': 'CH125_10', 'name': 'Parma', 'city': 'Parma', 'country': 'ITA', 'level': 125, 'surface': 'Clay',
     'draw_size': 32},

    # ======================================================
    # Challenger 100 Pool (15 Tournaments)
    # ======================================================
    {'id': 'CH100_01', 'name': 'Sarasota', 'city': 'Sarasota', 'country': 'USA', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_02', 'name': 'Prague', 'city': 'Prague', 'country': 'CZE', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_03', 'name': 'Lisbon', 'city': 'Lisbon', 'country': 'POR', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_04', 'name': 'Bengaluru', 'city': 'Bengaluru', 'country': 'IND', 'level': 100, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH100_05', 'name': 'Taipei', 'city': 'Taipei', 'country': 'TPE', 'level': 100, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH100_06', 'name': 'Bratislava', 'city': 'Bratislava', 'country': 'SVK', 'level': 100,
     'surface': 'Hard (Indoor)', 'draw_size': 32},
    {'id': 'CH100_07', 'name': 'Alicante', 'city': 'Alicante', 'country': 'ESP', 'level': 100, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH100_08', 'name': 'Tallahassee', 'city': 'Tallahassee', 'country': 'USA', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_09', 'name': 'Prostejov', 'city': 'Prostejov', 'country': 'CZE', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_10', 'name': 'Surbiton', 'city': 'Surbiton', 'country': 'GBR', 'level': 100, 'surface': 'Grass',
     'draw_size': 32},
    {'id': 'CH100_11', 'name': 'Cary', 'city': 'Cary', 'country': 'USA', 'level': 100, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH100_12', 'name': 'Cassino', 'city': 'Cassino', 'country': 'ITA', 'level': 100, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH100_13', 'name': 'Quimper', 'city': 'Quimper', 'country': 'FRA', 'level': 100, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH100_14', 'name': 'Heilbronn', 'city': 'Heilbronn', 'country': 'GER', 'level': 100, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH100_15', 'name': 'Yokohama', 'city': 'Yokohama', 'country': 'JPN', 'level': 100, 'surface': 'Hard',
     'draw_size': 32},

    # ======================================================
    # Challenger 75 Pool (20 Tournaments)
    # ======================================================
    {'id': 'CH75_01', 'name': 'Morelos', 'city': 'Morelos', 'country': 'MEX', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_02', 'name': 'Split', 'city': 'Split', 'country': 'CRO', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_03', 'name': 'Lille', 'city': 'Lille', 'country': 'FRA', 'level': 75, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH75_04', 'name': 'Guangzhou', 'city': 'Guangzhou', 'country': 'CHN', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_05', 'name': 'Oeiras', 'city': 'Oeiras', 'country': 'POR', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_06', 'name': 'San Benedetto', 'city': 'San Benedetto', 'country': 'ITA', 'level': 75,
     'surface': 'Clay', 'draw_size': 32},
    {'id': 'CH75_07', 'name': 'Winnipeg', 'city': 'Winnipeg', 'country': 'CAN', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_08', 'name': 'Liberec', 'city': 'Liberec', 'country': 'CZE', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_09', 'name': 'Manacor', 'city': 'Manacor', 'country': 'ESP', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_10', 'name': 'Bangkok', 'city': 'Bangkok', 'country': 'THA', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_11', 'name': 'Cleveland', 'city': 'Cleveland', 'country': 'USA', 'level': 75,
     'surface': 'Hard (Indoor)', 'draw_size': 32},
    {'id': 'CH75_12', 'name': 'Ostrava', 'city': 'Ostrava', 'country': 'CZE', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_13', 'name': 'Shymkent', 'city': 'Shymkent', 'country': 'KAZ', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_14', 'name': 'Blois', 'city': 'Blois', 'country': 'FRA', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_15', 'name': 'Chicago', 'city': 'Chicago', 'country': 'USA', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_16', 'name': 'Ambato', 'city': 'Ambato', 'country': 'ECU', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH75_17', 'name': 'Drummondville', 'city': 'Drummondville', 'country': 'CAN', 'level': 75,
     'surface': 'Hard (Indoor)', 'draw_size': 32},
    {'id': 'CH75_18', 'name': 'Pune', 'city': 'Pune', 'country': 'IND', 'level': 75, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH75_19', 'name': 'Glasgow', 'city': 'Glasgow', 'country': 'GBR', 'level': 75, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH75_20', 'name': 'Santiago', 'city': 'Santiago', 'country': 'CHI', 'level': 75, 'surface': 'Clay',
     'draw_size': 32},

    # ======================================================
    # Challenger 50 Pool (10 Tournaments)
    # ======================================================
    {'id': 'CH50_01', 'name': 'Nonthaburi', 'city': 'Nonthaburi', 'country': 'THA', 'level': 50, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH50_02', 'name': 'Florianopolis', 'city': 'Florianopolis', 'country': 'BRA', 'level': 50,
     'surface': 'Clay', 'draw_size': 32},
    {'id': 'CH50_03', 'name': 'Lugano', 'city': 'Lugano', 'country': 'SUI', 'level': 50, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH50_04', 'name': 'Segovia', 'city': 'Segovia', 'country': 'ESP', 'level': 50, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH50_05', 'name': 'Troisdorf', 'city': 'Troisdorf', 'country': 'GER', 'level': 50, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH50_06', 'name': 'Rome', 'city': 'Rome', 'country': 'USA', 'level': 50, 'surface': 'Hard (Indoor)',
     'draw_size': 32},
    {'id': 'CH50_07', 'name': 'Buenos Aires', 'city': 'Buenos Aires', 'country': 'ARG', 'level': 50, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH50_08', 'name': 'Kigali', 'city': 'Kigali', 'country': 'RWA', 'level': 50, 'surface': 'Clay',
     'draw_size': 32},
    {'id': 'CH50_09', 'name': 'New Delhi', 'city': 'New Delhi', 'country': 'IND', 'level': 50, 'surface': 'Hard',
     'draw_size': 32},
    {'id': 'CH50_10', 'name': 'Wako', 'city': 'Wako', 'country': 'JPN', 'level': 50, 'surface': 'Hard',
     'draw_size': 32},
]