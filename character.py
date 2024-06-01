from character_template import Character
import character_buffs
from damage_calculation import damage
from enemy import Enemy

class Seele(Character):        
    
    dummy = character_buffs.seele_buffs()
    
    def __init__(self, eidolons: int=0, lightcone: str='in_the_night', r: int=1, relic1: str='genius', relic2: str='genius', planar: str='arena') -> None:
        super().__init__('Seele', eidolons, lightcone, r)

        # Base stats
        self.basic_stats['base_attack'] += 640
        self.basic_stats['base_speed'] += 115
        self.basic_stats['attack'] += 640
        self.basic_stats['speed'] += 115
        self.info['dmg_type'] = 'quantum'
        
        # Base traces
        self.basic_stats['crit_dmg'] += 24
        self.basic_stats['attack_rate'] += 28

        # Initialize buffs
        self.buffs_init(lightcone, r, relic1, relic2, planar)

        # Eidolons
        if eidolons >= 1: # Eidolon 1
            self.buffs['on_hit']['eidolon_1'] = self.dummy.eidolon_1()
            if eidolons >= 3: # Eidolon 3
                self.basic_stats['skill_lvl'] += 2
                self.basic_stats['talent_lvl'] += 2
                if eidolons >= 5: # Eidolon 5
                    self.basic_stats['ultimate_lvl'] += 2
                    self.basic_stats['basic_lvl'] += 1

    def move_logic(self, battle, target: Enemy) -> list:
        if battle.skill_point >= 1:
            battle.skill_point -= 1
            return self.skill(target)
        else:
            battle.skill_point += 1
            return self.basic(target)
    
    def ultimate_ready(self) -> bool:
        return self.basic_stats['cur_energy'] >= self.basic_stats['energy']

    def ultimate_logic(self, battle, target: Enemy) -> list:
        return self.ultimate(target)
    
    def start_of_turn(self, battle, target: Enemy) -> None:
        return
    
    def end_of_turn(self, battle, target: Enemy) -> None:
        return

    def basic(self, target: Enemy) -> float:

        # Reminder
        #print('Seele casts basic!')

        # Do damage to Enemy
        rate = 40 + 10 * self.basic_stats['basic_lvl']
        dmg_exp = damage(self, target, rate, 'basic')
        
        # Do toughness damage
        if self.info['dmg_type'] in target.basic_stats['weakness']:
            target.basic_stats['toughness'] -= 30 * self.basic_stats['break_rate'] / 100

        # Calculate energy
        self.basic_stats['cur_energy'] += 20 * self.basic_stats['energy_regen_rate'] / 100
        
        self.basic_stats['until_turn'] -= 2000 # Trace 3

        return dmg_exp
    
    def skill(self, target: Enemy) -> float:

        # Reminder
        #print('Seele casts skill!')

        # Add buffs
        seele_skill = self.dummy.skill(self)
        type = seele_skill['type']
        if 'seele_skill' not in self.buffs[type]:
            self.buffs[type]['seele_skill'] = seele_skill
            for i in seele_skill['stats']:
                self.basic_stats[i] += seele_skill['stats'][i] * seele_skill['stack']
        else:
            self.buffs[type]['seele_skill']['turn'] = self.buffs[type]['seele_skill']['max_turn']
            if self.buffs[type]['seele_skill']['stack'] < self.buffs[type]['seele_skill']['max_stack']:
                self.buffs[type]['seele_skill']['stack'] += 1
                self.basic_stats['speed_rate'] += 25
        self.calc_stats()
        # Do damage to Enemy
        rate = 110 + 11 * self.basic_stats['skill_lvl']
        dmg_exp = damage(self, target, rate, 'skill')
        
        # Do toughness damage
        if self.info['dmg_type'] in target.basic_stats['weakness']:
            target.basic_stats['toughness'] -= 60 * self.basic_stats['break_rate'] / 100

        # Calculate energy
        self.basic_stats['cur_energy'] += 30 * self.basic_stats['energy_regen_rate'] / 100
        
        return dmg_exp

    def talent(self) -> None:

        # Add buffs
        seele_talent = self.dummy.talent(self)
        type = seele_talent['type']
        if 'seele_talent' not in self.buffs[type]:
            self.buffs[type]['seele_talent'] = seele_talent
            for i in seele_talent['stats']:
                self.basic_stats[i] += seele_talent['stats'][i] * seele_talent['stack']

    def ultimate(self, target: Enemy) -> float:
        
        # Reminder
        #print('Seele casts ultimate!')

        # Add buffs
        self.talent()

        # Do damage to Enemy
        rate = 255 + 17 * self.basic_stats['ultimate_lvl']
        dmg_exp = damage(self, target, rate, 'ultimate')

        # Do toughness damage
        if self.info['dmg_type'] in target.basic_stats['weakness']:
            target.basic_stats['toughness'] -= 90 * self.basic_stats['break_rate'] / 100

        self.basic_stats['cur_energy'] = 5 * self.basic_stats['energy_regen_rate'] / 100

        if self.info['eidolon'] >= 6: # Eidolon 6
            target.on_hit['seele_eidolon_6'] = self.dummy.eidolon_6(self)
        
        return dmg_exp
    

