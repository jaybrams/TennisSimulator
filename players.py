# players.py
from configs.simulation_config import OVR_WEIGHTS, MATCH_STAMINA_SCALAR

class Player:
    """Represents a tennis player with various skill attributes."""

    def __init__(self, name, sp, sa, gs, ref, sta, strg, clt, country="USA", player_id=0, ovr=None):
        self.id = player_id
        self.name = name
        self.country = country
        self.serve_power = sp
        self.serve_accuracy = sa
        self.groundstroke = gs
        self.reflex = ref
        self.stamina = sta
        self.strength = strg
        self.clutch = clt
        if ovr is None:
            self.overall = self._calculate_ovr()
        else:
            self.overall = ovr
        # Match-specific state variables
        self.fatigue = 0  # This will accumulate over the match
        self.current_score = "0"
        self.games_won = 0
        self.sets_won = 0

    def get_skill(self, skill_name: str) -> float:
        """Returns the effective skill value, accounting for match fatigue."""
        base_skill = getattr(self, skill_name)

        # Only physical skills are affected by match-long fatigue
        if skill_name not in ['serve_power', 'groundstroke', 'reflex']:
            return base_skill

        # Calculate penalty based on accumulated fatigue and stamina
        # Capped at a max of 40% skill reduction
        fatigue_penalty_raw = self.fatigue / (self.stamina * MATCH_STAMINA_SCALAR)
        fatigue_penalty = min(0.4, fatigue_penalty_raw)

        effective_skill = base_skill * (1.0 - fatigue_penalty)
        return max(1.0, effective_skill)  # Skill can't drop below 1

    def _calculate_ovr(self) -> int:
        """Calculates the weighted average for the player's overall rating."""
        weighted_sum = (
            (self.groundstroke * OVR_WEIGHTS['gs']) +
            (self.reflex * OVR_WEIGHTS['ref']) +
            (self.strength * OVR_WEIGHTS['strg']) +
            (self.serve_power * OVR_WEIGHTS['sp']) +
            (self.serve_accuracy * OVR_WEIGHTS['sa']) +
            (self.clutch * OVR_WEIGHTS['clt']) +
            (self.stamina * OVR_WEIGHTS['sta'])
        )
        return int(weighted_sum)

    def __str__(self):
        return (f"{self.name} [{self.country}] (OVR: {self.overall} | "
                f"SP: {self.serve_power}, SA: {self.serve_accuracy}, GS: {self.groundstroke}, "
                f"REF: {self.reflex}, STR: {self.strength}, STA: {self.stamina}, CLT: {self.clutch})")
