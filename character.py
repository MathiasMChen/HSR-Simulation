from character_template import Character
import character_buffs
from damage_calculation import damage, expectation, crit
import battle_simulation

class Seele(Character):        
    
    dummy = character_buffs.seele()
    
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

        # Initialize buffs
        self.buffs_init(lightcone, r, relic1, relic2, planar)

        # Eidolons
        if eidolons >= 1: # Eidolon 1
            self.on_hit['eidolon_1'] = self.dummy.eidolon_1()
            if eidolons >= 3: # Eidolon 3
                self.basic_stats['skill_lvl'] += 2
                self.basic_stats['talent_lvl'] += 2
                if eidolons >= 5: # Eidolon 5
                    self.basic_stats['ultimate_lvl'] += 2
                    self.basic_stats['basic_lvl'] += 1
        
    def basic(self, target) -> int:

        # Start turn, calculating buffs and stats
        battle_simulation.turn_start(self)
        self.calc_stats()

        # Do damage to Enemy
        rate = 40 + 10 * self.basic_stats['basic_lvl']
        [dmg, applied_buffs] = damage(self, target, rate, extra_dmg_boost=self.basic_stats['basic_dmg'])
        dmg_E = dmg * expectation(self)
        dmg_crit = dmg * crit(self)

        # Calculate energy
        self.basic_stats['cur_energy'] += 20 * self.basic_stats['energy_regen_rate']

        # End turn
        battle_simulation.turn_end(self,applied_buffs)

        self.basic_stats['until_turn'] -= 2000 # Trace 3
        return [dmg, dmg_E, dmg_crit]
    
    def skill(self, target) -> int:

        # Start turn, calculating buffs and stats
        battle_simulation.turn_start(self)
        self.calc_stats()

        # Add buffs
        seele_skill = self.dummy.skill()
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
        [dmg, applied_buffs] = damage(self, target, rate, extra_dmg_boost=self.basic_stats['skill_dmg'])
        dmg_E = dmg * expectation(self)
        dmg_crit = dmg * crit(self)

        # Calculate energy
        self.basic_stats['cur_energy'] += 30 * self.basic_stats['energy_regen_rate'] / 100

        # End turn
        battle_simulation.turn_end(self,applied_buffs)
        return [dmg, dmg_E, dmg_crit]

    def talent(self) -> None:

        # Add buffs
        seele_talent = self.dummy.talent(self)
        if 'seele_talent' not in self.buffs:
            seele_talent['stats']['res_pen'] = 20 # Trace 2
            self.buffs['seele_talent'] = seele_talent
            for i in seele_talent['stats']:
                self.basic_stats[i] += seele_talent['stats'][i] * seele_talent['stack']

    def ultimate(self, target) -> int:

        # Add buffs
        self.talent()

        # Do damage to Enemy
        rate = 255 + 17 * self.basic_stats['ultimate_lvl']
        [dmg, applied_buffs] = damage(self, target, rate)
        dmg_E = dmg * expectation(self, conditional_crit_dmg=self.basic_stats['ultimate_crit_dmg'])
        dmg_crit = dmg * crit(self, conditional_crit_dmg=self.basic_stats['ultimate_crit_dmg'])

        battle_simulation.turn_end(self,applied_buffs,True)
        if self.info['eidolon'] >= 6: # Eidolon 6
            target.inflicts['on_hit'].append({'effect': self.eidolon_6, 'turn': 1})
        # Taking into consideration only single enemy so no extra turn code
        # Will add if considering multiple
        return [dmg, dmg_E, dmg_crit]
    
    def eidolon_6(self, target) -> None:
        return 15
