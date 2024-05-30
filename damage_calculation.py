# Calculate damage
def damage(self, target, dmg_rate, fixed_dmg = 0, extra_dmg_boost = 0, attribute = 'attack') -> int:

    # Apply on-hit and conditional buffs
    applied_buffs = []
    for i in self.on_hit:
        k = self.on_hit[i]
        if k['condition'](target):
            for j in k['stats']:
                self.basic_stats[j] += k['stats'][j] * k['stack']
            if k['turn'] > 0:
                if k['name'] in self.buffs:
                    self.buffs[k['name']]['turn'] = k['turn']
                else:
                    k.pop('condition')
                    self.buffs[k['name']] = k
            else:
                applied_buffs.append(k)

    for i in self.conditional_buffs:
        p = self.conditional_buffs[i]
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

    return [dmg, applied_buffs]
    
# Calculate damage expectation rate
def expectation(self, conditional_rate = 0, conditional_crit_dmg = 0):
    return 1 + (self.basic_stats['crit_rate'] + conditional_rate) * (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 10000

# Calculate crit damage rate
def crit(self, conditional_crit_dmg = 0):
    return 1 + (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 100
