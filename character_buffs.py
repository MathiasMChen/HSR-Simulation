from damage_calculation import damage
from enemy import Enemy

class seele_buffs():
    def eidolon_1_helper(self, target: Enemy) -> bool:
        return target.basic_stats['remaining_hp'] / target.basic_stats['max_hp'] <= 0.8
    
    def eidolon_6_helper(self, seele, target: Enemy) -> float:

        # Reminder
        #print('Seele E6 on-hit triggers!')

        # Do damage to enemy
        rate = (255 + 17 * seele.basic_stats['ultimate_lvl']) * 0.15
        dmg_exp = damage(seele, target, rate, 'ultimate')

        return dmg_exp

    def eidolon_1(self) -> dict:
        return  {
                    'source': 'character',
                    'name': 'seele_eidolon_1',
                    'type': 'on_hit',
                    'condition': self.eidolon_1_helper,
                    'stats': {'crit_rate': 15},
                    'stack': 1,
                    'max_stack': 1,
                    'turn': 0,
                    'max_turn': 0
                }
    
    def eidolon_6(self, seele) -> dict:
        return  {
                    'effect': self.eidolon_6_helper, 
                    'origin': seele,
                    'after': True,
                    'turn': 1
                }



    def skill(self, seele) -> dict:
        return  {
                    'source': 'character',
                    'name': 'seele_skill',
                    'type': 'buff', 
                    'decrement': 'end_turn',
                    'stats': {
                        'speed_rate': 25
                    },
                    'stack': 1,
                    'max_stack': 2 if seele.info['eidolon'] >= 2 else 1, # Eidolon 2
                    'turn': 3,
                    'max_turn': 3
                }

    def talent(self, seele) -> dict:
        return  {
                    'source': 'character',
                    'name': 'seele_talent',
                    'type': 'buff',
                    'decrement': 'end_turn',
                    'stats': {
                        'dmg_boost': 80 + 4 * (seele.basic_stats['talent_lvl'] - 10), 
                        'res_pen': 20 # Trace 2
                    },
                    'stack': 1,
                    'turn': 1
                }