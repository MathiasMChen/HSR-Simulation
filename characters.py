from enemy import Enemy
import lightcones
import random
import relic
import character
from pprint import pprint

class Character:
    def __init__(self, name: str, eidolons: int, lightcone: str, r: int):
        if eidolons < 0 or eidolons > 6:
            raise ValueError("Eidolon has to be an integer between 0 and 6.") 
        
        # Initialize basic info 
        self.info = {
            'name': name,
            'eidolon': eidolons,
            'lightcone': lightcone,
            'echo': r,
        }

        # Initialize basic stats
        self.basic_stats = {
            'base_attack': 0,
            'base_speed': 0,
            'attack_rate': 100,
            'speed_rate': 100,
            'fixed_attack': 0,
            'fixed_speed': 0,
            'attack': 0,
            'speed': 0,
            'crit_rate': 5,
            'crit_dmg': 50,
            'break_effect': 100,
            'dmg_boost': 100,
            'effect_hit_rate': 0,
            'energy': 0,
            'cur_energy': 0,
            'energy_regen_rate': 100,
            'basic_lvl': 6,
            'skill_lvl': 10,
            'talent_lvl': 10,
            'ultimate_lvl': 10,
            'res_pen': 0,
            'until_turn': 10000,
            'basic_dmg': 0,
            'skill_dmg': 0,
            'ultimate_dmg': 0,
            'basic_crit_dmg': 0,
            'skill_crit_dmg': 0,
            'ultimate_crit_dmg': 0,
            'def_pen': 0,
        }

        # Initial relic main stats data
        self.relic_mainstats_ref = {
            'crit_rate': 32.4,
            'crit_dmg': 64.8,
            'attack_rate': 43.2,
            'fixed_speed': 25,
            'dmg_boost': 38.88,
            'energy_regen_rate': 19.44
        }

        # Store on-hit buffs
        self.on_hit = {}
        self.buffs = {}
        self.conditional_buffs = {}
        self.refreshing_buffs = {}

    # Start of turn, decrement remaining buff durations by 1 and remove any expired buffs
    def turn_start(self):
        buffs = list(self.buffs.keys())
        for i in buffs:
            if self.buffs[i]['turn'] == 1:
                for j in self.buffs[i]['stats']:
                    self.basic_stats[j] -= self.buffs[i]['stats'][j] * self.buffs[i]['stack']
                self.buffs.pop(i)
            else:
                self.buffs[i]['turn'] -= 1
    
    # End of turn
    def turn_end(self, applied_buffs, ultimate = False):

        # Reset runway length if not ultimate
        if not ultimate:
            self.basic_stats['until_turn'] = 10000
        
         # Remove one-time on-hit and conditional buffs
        for i in applied_buffs:
            for j in i['stats']:
                self.basic_stats[j] -= i['stats'][j] * i['stack']
        self.calc_stats()

    # Calculate dynamic attack and speed based on three parts, and calculate refreshing buffs situation
    def calc_stats(self):
        self.basic_stats['attack'] = self.basic_stats['base_attack'] * self.basic_stats['attack_rate']/100 + self.basic_stats['fixed_attack']
        self.basic_stats['speed'] = self.basic_stats['base_speed'] * self.basic_stats['speed_rate']/100 + self.basic_stats['fixed_speed']
        for i in self.refreshing_buffs:
            p = self.refreshing_buffs[i]
            q = p['turn']
            for m in p['stats']:
                self.basic_stats[m] -= p['stats'][m] * p['stack']
            if p['source'] == 'lightcone':
                k = p['func'](self, self.info['echo'], False)
                self.refreshing_buffs[i] = k
                k['turn'] = q
            if p['source'] == 'relic':
                k = p['func'](self)
                self.refreshing_buffs[i] = k
                k['turn'] = q
            for m in k['stats']:
                self.basic_stats[m] += k['stats'][m] * k['stack']
        
    # Set relic main stats for attackers
    def set_attack_relic_mainstats(self, shawl: str='crit_dmg', boot: str='fixed_speed', sphere: str='dmg_boost', rope: str='attack_rate'):
        self.basic_stats['fixed_attack'] += 352.7
        self.basic_stats[shawl] += self.relic_mainstats_ref[shawl]
        self.basic_stats[boot] += self.relic_mainstats_ref[boot]
        self.basic_stats[sphere] += self.relic_mainstats_ref[sphere]
        self.basic_stats[rope] += self.relic_mainstats_ref[rope]
        self.calc_stats()

    # Set relic substats for attackers
    def set_attack_relic_substats(self, fixed_attack: int=0, attack_rate: int=0, fixed_speed: int=0, crit_rate: int=0, crit_dmg: int=0):
        self.basic_stats['fixed_attack'] += fixed_attack * 19
        self.basic_stats['attack_rate'] += attack_rate * 3.89
        self.basic_stats['fixed_speed'] += fixed_speed * 2.3
        self.basic_stats['crit_rate'] += crit_rate * 2.92
        self.basic_stats['crit_dmg'] += crit_dmg * 5.83
        self.calc_stats()

    # Calculate damage
    def damage(self, target: Enemy, dmg_rate, fixed_dmg = 0, extra_dmg_boost = 0, attribute = 'attack') -> int:

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
        
    # Calculate damage expectation
    def expectation(self, conditional_rate = 0, conditional_crit_dmg = 0):
        return 1 + (self.basic_stats['crit_rate'] + conditional_rate) * (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 10000

    # Calculate crit damage
    def crit(self, conditional_crit_dmg = 0):
        return 1 + (self.basic_stats['crit_dmg'] + conditional_crit_dmg) / 100

class Seele(Character):
    def __init__(self, eidolons: int, lightcone: str, r: int, relic1, relic2, planar) -> None:
        super().__init__('Seele', eidolons, lightcone, r)

        # Base stats
        self.basic_stats['base_attack'] += 640
        self.basic_stats['base_speed'] += 115
        self.basic_stats['attack'] += 640
        self.basic_stats['speed'] += 115
        
        # Base traces
        self.basic_stats['crit_dmg'] += 24
        self.basic_stats['attack_rate'] += 28

        # Initialize lightcone buffs (if any)
        a = getattr(lightcones, lightcone)(self, r,True)
        if a['type'] == 'conditional':
            self.conditional_buffs[lightcone] = a
        if a['type'] == 'buff':
            self.buffs[lightcone] = a
        if a['type'] == 'on_hit':
            self.on_hit[lightcone] = a
        if a['type'] == 'refreshing':
            self.refreshing_buffs[lightcone] = a

        # Initialize relic buffs (if any)
        relic_1 = getattr(relic, relic1)
        if 'type' not in relic_1[0]:
            for i in relic_1[0]:
                self.basic_stats[i] += relic_1[0][i]
        elif relic_1[0]['type'] == 'on_hit':
            self.on_hit[relic_1[0]['name']] = relic_1[0]
        if relic2 == relic1:
            if 'type' not in relic_1[1]:
                for i in relic_1[1]:
                    self.basic_stats[i] += relic_1[1][i]
            elif relic_1[1]['type'] == 'on_hit':
                self.on_hit[relic2] = relic_1[1]
            elif relic_1[1]['type'] == 'conditional':
                self.conditional_buffs[relic2] = relic_1[1]
            elif relic_1[1]['type'] == 'buff':
                self.buffs[relic2] = relic_1[1]
            elif relic_1['type'] == 'refreshing':
                self.refreshing_buffs[relic2] = relic_1[1]
        else:
            relic_2 = getattr(relic, relic2)
            if 'type' not in relic_2[0]:
                for i in relic_2[0]:
                    self.basic_stats[i] += relic_2[0][i]
            elif relic_2[0]['type'] == 'on_hit':
                self.on_hit[relic_2[0]['name']] = relic_1[0]
        planar_1 = getattr(relic, planar)
        for i in planar_1[0]:
            self.basic_stats[i] += planar_1[0][i]
        self.conditional_buffs[planar] = planar_1[1]

        # Add buffs to stats
        for i in self.buffs:
            for j in self.buffs[i]['stats']:
                self.basic_stats[j] += self.buffs[i]['stats'][j] * self.buffs[i]['stack']
        for i in self.refreshing_buffs:
            for j in self.refreshing_buffs[i]['stats']:
                self.basic_stats[j] += self.refreshing_buffs[i]['stats'][j] * self.refreshing_buffs[i]['stack']


        # Eidolons
        if eidolons >= 1: # Eidolon 1
            self.on_hit['eidolon_1'] = character.seele_eidolon_1(self)
            if eidolons >= 3: # Eidolon 3
                self.basic_stats['skill_lvl'] += 2
                self.basic_stats['talent_lvl'] += 2
                if eidolons >= 5: # Eidolon 5
                    self.basic_stats['ultimate_lvl'] += 2
                    self.basic_stats['basic_lvl'] += 1
        
    def basic(self, target) -> int:

        # Start turn, calculating buffs and stats
        self.turn_start()
        self.calc_stats()

        # Do damage to Enemy
        rate = 40 + 10 * self.basic_stats['basic_lvl']
        [dmg, applied_buffs] = self.damage(target, rate, extra_dmg_boost=self.basic_stats['basic_dmg'])
        dmg_E = dmg * self.expectation()
        dmg_crit = dmg * self.crit()

        # Calculate energy
        self.basic_stats['cur_energy'] += 20 * self.basic_stats['energy_regen_rate']

        # End turn
        self.turn_end(applied_buffs)

        self.basic_stats['until_turn'] -= 2000 # Trace 3
        return [dmg, dmg_E, dmg_crit]
    
    def skill(self, target) -> int:

        # Start turn, calculating buffs and stats
        self.turn_start()
        self.calc_stats()

        # Add buffs
        seele_skill = character.seele_skill(self)
        seele_skill['max_stack'] = 2 if self.info['eidolon'] >= 1 else 1 # Eidolon 2
        if 'seele_skill' not in self.buffs:
            self.buffs['seele_skill'] = seele_skill
            for i in seele_skill['stats']:
                self.basic_stats[i] += seele_skill['stats'][i] * seele_skill['stack']
        else:
            self.buffs['seele_skill']['turn'] = self.buffs['seele_skill']['max_turn']
            if self.buffs['seele_skill']['stack'] < self.buffs['seele_skill']['max_stack']:
                self.buffs['seele_skill']['stack'] += 1
                self.basic_stats['speed_rate'] += 25
        self.calc_stats()
        # Do damage to Enemy
        rate = 110 + 11 * self.basic_stats['skill_lvl']
        [dmg, applied_buffs] = self.damage(target, rate, extra_dmg_boost=self.basic_stats['skill_dmg'])
        dmg_E = dmg * self.expectation()
        dmg_crit = dmg * self.crit()

        # Calculate energy
        self.basic_stats['cur_energy'] += 30 * self.basic_stats['energy_regen_rate'] / 100

        # End turn
        self.turn_end(applied_buffs)
        return [dmg, dmg_E, dmg_crit]

    def talent(self) -> None:

        # Add buffs
        seele_talent = character.seele_talent(self)
        if 'seele_talent' not in self.buffs:
            seele_talent['stats']['res_pen'] = 20 # Trace 2
            self.buffs['seele_talent'] = seele_talent
            for i in seele_talent['stats']:
                self.basic_stats[i] += seele_talent['stats'][i] * seele_talent['stack']

    def ultimate(self, target: Enemy) -> int:

        # Add buffs
        self.talent()

        # Do damage to Enemy
        rate = 255 + 17 * self.basic_stats['ultimate_lvl']
        [dmg, applied_buffs] = self.damage(target, rate)
        dmg_E = dmg * self.expectation(conditional_crit_dmg=self.basic_stats['ultimate_crit_dmg'])
        dmg_crit = dmg * self.crit(conditional_crit_dmg=self.basic_stats['ultimate_crit_dmg'])

        self.turn_end(applied_buffs, True)
        if self.info['eidolon'] >= 6: # Eidolon 6
            target.inflicts['on_hit'].append({'effect': self.eidolon_6, 'turn': 1})
        # Taking into consideration only single enemy so no extra turn code
        # Will add if considering multiple
        return [dmg, dmg_E, dmg_crit]
    
    def eidolon_6(self, target: Enemy) -> None:
        return 15