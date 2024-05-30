class Enemy:
    def __init__(self) -> None:
        self.info = {
            'type': 'enemy'
        }
        self.debuffs = {}
        self.on_hit = {}
        self.basic_stats = {
            'remaining_hp': 200000,
            'max_hp': 200000,
            'res': 0,
            'def_red': 0,
            'dmg_taken': 0,
            'toughness_resist': 10,
            'def': 1000,
            'weakness': ['quantum', 'fire', 'lightning', 'wind', 'imaginary', 'ice', 'physical'],
            'speed': 70,
            'until_turn': 10000
        }
    def move(self):
        print('Enemy moves.')
        debuffs = list(self.debuffs.keys())
        for i in debuffs:
            if self.debuffs[i]['turn'] == 1:
                self.debuffs.pop(i)
            else:
                self.debuffs[i]['turn'] -= 1
        on_hit = list(self.on_hit.keys())
        for i in on_hit:
            if self.on_hit[i]['turn'] == 1:
                self.on_hit.pop(i)
            else:
                self.on_hit[i]['turn'] -= 1
        self.basic_stats['until_turn'] += 10000