from damage_calculation import damage, expectation, crit

class seele():
    def eidolon_1_helper(self,target):
        return target.basic_stats['remaining_hp'] / target.basic_stats['max_hp'] <= 0.8
    
    def eidolon_6_helper(self, Seele, target):

        # Reminder
        print('Seele E6 on-hit triggers!')

        # Do damage to enemy
        rate = (255 + 17 * Seele.basic_stats['ultimate_lvl']) * 0.15
        [dmg, applied_buffs] = damage(Seele, target, rate)
        dmg_E = dmg * expectation(Seele, conditional_crit_dmg=Seele.basic_stats['ultimate_crit_dmg'])
        dmg_crit = dmg * crit(Seele, conditional_crit_dmg=Seele.basic_stats['ultimate_crit_dmg'])

        return [[dmg, dmg_E, dmg_crit], applied_buffs]

    def eidolon_1(self):
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
    
    def eidolon_6(self, seele):
        return  {
                    'effect': self.eidolon_6_helper, 
                    'origin': seele,
                    'after': True,
                    'turn': 1
                }



    def skill(self, ally):
        return  {
                    'source': 'character',
                    'name': 'seele_skill',
                    'type': 'buff', 
                    'decrement': 'end_turn',
                    'stats': {
                        'speed_rate': 25
                    },
                    'stack': 1,
                    'max_stack': 2 if ally.info['eidolon'] >= 2 else 1, # Eidolon 2
                    'turn': 3,
                    'max_turn': 3
                }

    def talent(self, ally):
        return  {
                    'source': 'character',
                    'name': 'seele_talent',
                    'type': 'buff',
                    'decrement': 'end_turn',
                    'stats': {
                        'dmg_boost': 80 + 4 * (ally.basic_stats['talent_lvl'] - 10), 
                        'res_pen': 20 # Trace 2
                    },
                    'stack': 1,
                    'turn': 1
                }