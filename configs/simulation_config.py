# simulation_config.py

# --- OVR Balancing Constants (The Core Game Feel) ---
WEIGHTING_FACTOR = 0.35
VARIANCE_SIGMA_POINT = 20

# --- Serve Phase Constants (Fault Check) ---
VARIANCE_SIGMA_FAULT = 5
FSSR_BASELINE_FLOOR = 45
FSSR_SA_WEIGHT = 0.4
POWER_PENALTY_RATE = 0.12
POWER_THRESHOLD = 50

# --- Second Serve Double Fault Tiers (SSFR) ---
DOUBLE_FAULT_TIERS = {
    30: 24.0,
    50: 19.0,
    70: 15.5,
    85: 13.5,
    100: 9.0,
}

# --- Clutch/DF Constants ---
CLUTCH_MODIFIER_RATE = 0.07
MIN_DF_RATE = 1.0

# --- Ace Check Constants ---
ACE_CEILING_FACTOR = 0.35
MIN_DEF_FLOOR = 0.05

# --- Shot Quality Scaling Constants (Scale x10) ---
WEIGHTING_SERVE_SP = 6.5
WEIGHTING_SERVE_SA = 4.4
SHOT_QUALITY_BASELINE = 500
SHOT_QUALITY_CEILING = 1250

# --- Rally Phase ESS (Effective Skill Score) Weighting (Scaled x10) ---
# Striker: GS (60) + STR (40)
WEIGHTING_RALLY_GS_OFFENSE = 6.0
WEIGHTING_STR_OFFENSE = 4.0
# Defender: GS (60) + REF (40)
WEIGHTING_RALLY_GS_DEFENSE = 6.0
WEIGHTING_REF_DEFENSE = 4.0

# --- Rally Success Constants ---
RALLY_SUCCESS_THRESHOLD = 0.65 # 65% success chance is the baseline for a return
MAX_RALLY_LENGTH = 35

# --- Stamina and Fatigue Constants ---
# Determines resistance to match-long fatigue. Higher value = more resistance.
MATCH_STAMINA_SCALAR = 60
# Determines rate of fatigue during a single rally.
# Formula: (105 - STA) / 10000 = penalty per shot.
RALLY_FATIGUE_SCALAR = 105
RALLY_FATIGUE_DIVISOR = 10000

# --- OVR Weighted Average Configuration ---
OVR_WEIGHTS = {
    'gs': 0.25,      # Groundstroke at 25%
    'ref': 0.20,     # Reflex at 20%
    'strg': 0.20,    # Strength at 20%
    'sp': 0.125,     # Serve Power at 12.5%
    'sa': 0.125,     # Serve Accuracy at 12.5%
    'clt': 0.05,     # Clutch at 5%
    'sta': 0.05,     # Stamina at 5%
}

TIER_RANGES = {
    "Elite": (86, 100),
    "Pro": (71, 85),
    "Challenger": (51, 70),
    "Futures": (31, 50),
    "Beginner": (1, 30),
}