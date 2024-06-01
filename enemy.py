import break_effects

class Enemy:
    def __init__(self) -> None:
        self.info = {
            'type': 'enemy'
        }
        self.debuffs = {}
        self.dot = {}
        self.on_hit = {}
        self.basic_stats = {
            'remaining_hp': 200000,
            'max_hp': 200000,
            'res': 0,
            'def_red': 0,
            'dmg_taken': 0,
            'toughness_resist': 10,
            'effect_res_rate': 30,
            'def': 1000,
            'weakness': ['quantum', 'fire', 'lightning', 'wind', 'imaginary', 'ice', 'physical'],
            'speed': 70,
            'until_turn': 10000,
            'toughness': 210,
            'max_toughness': 210,
            'recover': 0,
            'break': False
        }
    def move(character, battle, self):
        #print('Enemy moves.')
        
        dmg = 0
        dot_lst = list(self.dot.keys())
        for i in dot_lst:
            dmg += self.dot[i]['damage'](self.dot[i]['origin'], self) * self.dot[i]['stack'] * self.dot[i]['ratio']
            if self.dot[i]['turn'] == 1:
                self.dot.pop(i)
            else:
                self.dot[i]['turn'] -= 1

        debuffs_lst = list(self.debuffs.keys())
        for i in debuffs_lst:
            if self.debuffs[i]['turn'] == 1:
                self.debuffs.pop(i)
            else:
                self.debuffs[i]['turn'] -= 1
        on_hit_lst = list(self.on_hit.keys())
        for i in on_hit_lst:
            if self.on_hit[i]['turn'] == 1:
                self.on_hit.pop(i)
            else:
                self.on_hit[i]['turn'] -= 1        
        
        if self.basic_stats['recover'] >= 1:
            self.basic_stats['recover'] -= 1
        if self.basic_stats['recover'] == 0 and self.basic_stats['break']:
            break_effects.break_recover(self)
        if dmg > 0:
            self.basic_stats['remaining_hp'] -= dmg
            #print('Enemy suffers dot damage.')
            #print(f'Enemy Remaining HP: {self.basic_stats['remaining_hp']} / {self.basic_stats['max_hp']}')
        self.basic_stats['until_turn'] += 10000
        return dmg

    def toughness_break(self, character):
        result = break_effects.quantum(character, self)
        return result
