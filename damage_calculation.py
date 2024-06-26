from randombool import rand
from enemy import Enemy

# Calculate damage
def damage(self, target: Enemy, dmg_rate: float, type: str, fixed_dmg: int = 0, attribute: str = 'attack') -> int:

    # Apply on-hit and conditional buffs
    applied_buffs = []
    for i in self.buffs['on_hit']:
        k = self.buffs['on_hit'][i]
        if k['condition'](target):
            for j in k['stats']:
                self.basic_stats[j] += k['stats'][j] * k['stack']
            if k['turn'] > 0:
                if k['name'] in self.buffs[k['buff_type']]:
                    self.buffs[k['name']]['turn'] = k['turn']
                else:
                    k.pop('condition')
                    k['type'] = k['buff_type']
                    k.pop('buff_type')
                    self.buffs['buff'][k['name']] = k
            else:
                applied_buffs.append(k)

    for i in self.buffs['conditional']:
        p = self.buffs['conditional'][i]
        if p['condition'](self):
            for m in p['stats']:
                self.basic_stats[m] += p['stats'][m] * p['stack']
            if p['name'] not in self.buffs:
                if p['turn'] > 0:
                    self.buffs[p['name']] = p
                else:
                    applied_buffs.append(p)
            elif p['turn'] > self.buffs[p['name']]['turn']:
                self.buffs[p['name']]['turn'] = p['turn']
    self.calc_stats()    
    
    type_dct = {
        'basic': [self.basic_stats['basic_dmg'], self.basic_stats['basic_crit_rate'], self.basic_stats['basic_crit_dmg']],
        'skill': [self.basic_stats['skill_dmg'], self.basic_stats['skill_crit_rate'], self.basic_stats['skill_crit_dmg']],
        'ultimate': [self.basic_stats['ultimate_dmg'], self.basic_stats['ultimate_crit_rate'], self.basic_stats['ultimate_crit_dmg']]
    } 

    [extra_dmg_boost, conditional_critical_rate, conditional_critical_dmg] = type_dct[type]

    # Calculate damage
    dmg = dmg_rate / 100 * self.basic_stats[attribute] + fixed_dmg
    dmg *=  (self.basic_stats['dmg_boost'] + extra_dmg_boost) / 100
    defense = max(0, target.basic_stats['def'] * (100-target.basic_stats['def_red']-self.basic_stats['def_pen']) / 100)
    dmg *= (1 - defense / (defense+1000))
    res = (100 - target.basic_stats['res'] + self.basic_stats['res_pen'])/100
    if res > 0.9:
        res = 0.9
    if res < -1:
        res = -1
    dmg *= res
    dmg *= (1 + target.basic_stats['dmg_taken'] / 100)
    dmg *= (1 - target.basic_stats['toughness_resist'] / 100)
    dmg_exp = dmg * expectation(self, conditional_critical_rate, conditional_critical_dmg)
    if rand(self.basic_stats['crit_rate']):
        #print(f'Critical hit with {round(self.basic_stats['crit_rate'],1)}% chance!')
        dmg *= crit(self, conditional_critical_dmg)
    else:
        dmg *= 1
        #print(f'Critical hit failed with {round(self.basic_stats['crit_rate'],1)}% chance!')

    

    target.basic_stats['remaining_hp'] -= dmg
    #print(f'Enemy Remaining HP: {target.basic_stats['remaining_hp']} / {target.basic_stats['max_hp']}')     
    
    # Remove one-time on-hit and conditional buffs
    for i in applied_buffs:
        for j in i['stats']:
            self.basic_stats[j] -= i['stats'][j] * i['stack']

    return dmg_exp
    
# Calculate damage expectation rate
def expectation(self, conditional_rate: float = 0, conditional_crit_dmg: float = 0):
    return 1 + min((self.basic_stats['crit_rate'] + conditional_rate),100) * (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 10000

# Calculate crit damage rate
def crit(self, conditional_crit_dmg: float):
    return 1 + (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 100
