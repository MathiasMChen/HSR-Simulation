from enemy import Enemy
import lightcones
import relic

class Character:
    def __init__(self, name: str, eidolons: int, lightcone: str, r: int) -> None:
        if eidolons < 0 or eidolons > 6:
            raise ValueError("Eidolon has to be an integer between 0 and 6.") 
        
        # Initialize basic info 
        self.info = {
            'type': 'character',
            'name': name,
            'eidolon': eidolons,
            'lightcone': lightcone,
            'echo': r,
            'dmg_type': None
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
            'break_effect': 0,
            'dmg_boost': 100,
            'effect_hit_rate': 0,
            'energy': 110,
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
            'followup_dmg': 0,
            'basic_crit_rate': 0,
            'skill_crit_rate': 0,
            'ultimate_crit_rate': 0,
            'followup_crit_rate': 0,
            'basic_crit_dmg': 0,
            'skill_crit_dmg': 0,
            'ultimate_crit_dmg': 0,
            'followup_crit_dmg': 0,
            'def_pen': 0,
            'break_rate': 100
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
        self.buffs = {
            'permanant': {},
            'buff': {},
            'conditional': {},
            'on_hit': {},
            'refreshing': {}
        }

    # Initialize buffs
    def buffs_init(self, lightcone: str, r: int, relic1: str, relic2: str, planar: str) -> None:
        # Initialize lightcone buffs (if any)
        a = getattr(lightcones, lightcone)(self, r,True)
        self.buffs[a['type']][lightcone] = a

        # Initialize relic buffs (if any)
        relic_1 = getattr(relic, relic1)
        if relic2 == relic1:
            for i in relic_1: 
                self.buffs[i['type']][relic1] = i
        else:
            relic_2 = getattr(relic, relic2)
            self.buffs[relic_1[0]['type']][relic1] = relic_1[0]
            self.buffs[relic_2[0]['type']][relic2] = relic_2[0]

        
        planar_1 = getattr(relic, planar)
        for i in planar_1:
            self.buffs[i['type']][planar] = i

        # Add buffs to stats
        for i in self.buffs['permanant'].values():
            for j in i['stats']:
                self.basic_stats[j] += i['stats'][j] * i['stack']
        for i in self.buffs['refreshing'].values():
            for j in i['stats']:
                self.basic_stats[j] += i['stats'][j] * i['stack']
    
    # Calculate dynamic attack and speed based on three parts, and calculate refreshing buffs situation
    def calc_stats(self) -> None:
        self.basic_stats['attack'] = self.basic_stats['base_attack'] * self.basic_stats['attack_rate']/100 + self.basic_stats['fixed_attack']
        self.basic_stats['speed'] = self.basic_stats['base_speed'] * self.basic_stats['speed_rate']/100 + self.basic_stats['fixed_speed']
        for i in self.buffs['refreshing']:
            p = self.buffs['refreshing'][i]
            q = p['turn']
            for m in p['stats']:
                self.basic_stats[m] -= p['stats'][m] * p['stack']
            if p['source'] == 'lightcone':
                k = p['func'](self, self.info['echo'], False)
                self.buffs['refreshing'][i] = k
                k['turn'] = q
            if p['source'] == 'relic':
                k = p['func'](self)
                self.buffs['refreshing'][i] = k
                k['turn'] = q
            for m in k['stats']:
                self.basic_stats[m] += k['stats'][m] * k['stack']
        
    # Set relic main stats for attackers
    def set_attack_relic_mainstats(self, shawl: str='crit_dmg', boot: str='fixed_speed', sphere: str='dmg_boost', rope: str='attack_rate') -> None:
        self.basic_stats['fixed_attack'] += 352.7
        self.basic_stats[shawl] += self.relic_mainstats_ref[shawl]
        self.basic_stats[boot] += self.relic_mainstats_ref[boot]
        self.basic_stats[sphere] += self.relic_mainstats_ref[sphere]
        self.basic_stats[rope] += self.relic_mainstats_ref[rope]
        self.calc_stats()

    # Set relic substats for attackers
    def set_attack_relic_substats(self, fixed_attack: int=0, attack_rate: int=0, fixed_speed: int=0, crit_rate: int=0, crit_dmg: int=0) -> None:
        self.basic_stats['fixed_attack'] += fixed_attack * 21
        self.basic_stats['attack_rate'] += attack_rate * 4.32
        self.basic_stats['fixed_speed'] += fixed_speed * 2.6
        self.basic_stats['crit_rate'] += crit_rate * 3.24
        self.basic_stats['crit_dmg'] += crit_dmg * 6.48
        self.calc_stats()

    def move(self, battle, target: Enemy, ultimate: bool = False) -> float:
        # Start turn, calculating buffs and stats
        battle.turn_start(self, ultimate)
        self.start_of_turn(battle, target)
        self.calc_stats()

        skip = False
        if target.basic_stats['toughness'] <= 0:
            skip = True

        # Move according to preset logic
        if not ultimate:
            result = self.move_logic(battle, target)
        else:
            result = self.ultimate_logic(battle, target)

        # If target toughness breaks    
        if target.basic_stats['toughness'] <= 0 and not skip:
            result_break = target.toughness_break(self)
            result += result_break

        # End turn
        battle.turn_end(self,ultimate)
        self.end_of_turn(battle, target)

        return result
    
