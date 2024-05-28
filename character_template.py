from enemy import Enemy
import lightcones
import relic

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

        # Create dict to store buffs classified by type
        self.on_hit = {}
        self.buffs = {}
        self.conditional_buffs = {}
        self.refreshing_buffs = {}

    # Initialize buffs
    def buffs_init(self, lightcone, r, relic1, relic2, planar):
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
