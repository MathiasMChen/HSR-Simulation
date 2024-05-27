class Enemy:
    def __init__(self) -> None:
        self.debuffs = {}
        self.inflicts = {
            'on_hit': []
        }
        self.basic_stats = {
            'res': 0,
            'def_red': 0,
            'dmg_taken': 0,
            'toughness_resist': 10,
            'def': 1000,
            'weakness': ['quantum', 'fire', 'lightning', 'wind', 'imaginary', 'ice', 'physical']
        }