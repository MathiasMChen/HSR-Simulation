class seele():
    def eidolon_1_helper(self,target):
        return target.basic_stats['remaining_hp'] / target.basic_stats['max_hp'] <= 0.8

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

    def skill(self):
        return  {
                    'source': 'character',
                    'name': 'seele_skill',
                    'type': 'buff',
                    'stats': {'speed_rate': 25},
                    'stack': 1,
                    'max_stack': 1,
                    'turn': 2,
                    'max_turn': 2
                }

    def talent(self, target):
        return  {
                    'source': 'character',
                    'name': 'seele_skill',
                    'type': 'buff',
                    'stats': {'dmg_boost': 80 + 4 * (target.basic_stats['talent_lvl'] - 10)},
                    'stack': 1,
                    'turn': 1
                }
