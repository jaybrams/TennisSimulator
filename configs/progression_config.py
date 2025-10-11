# Age-based training multipliers
AGE_MODIFIERS = {
    "Prospect": (14, 18, 1.2),     # Ages 14-18 get a 1.2x XP gain
    "Peak": (19, 23, 1.5),         # Ages 19-23 get a 1.5x XP gain
    "Prime": (24, 29, 1.0),         # Ages 24-29 get a 1.0x XP gain
    "Veteran": (30, 34, -0.5),     # At age 30, skills start to decay
    "Retiree": (35, 40, -1.0)      # Decay accelerates
}