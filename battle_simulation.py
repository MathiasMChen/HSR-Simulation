import math

from character_template import Character
from enemy import Enemy

class Battle():

    # Initialize time length, moving unit list, target enemy, and initial skill point
    def __init__(self, timestamp: float, unitlist: list[Character], target: Enemy, sp: int=3) -> None:
        self.timestamp = timestamp
        self.skill_point = sp
        unitlist.append(target)
        self.unitlist = unitlist
        self.target = target
    
    # Simulate battle progress with given initialization.
    # Output: a list: 
    #   The element at index 0 is the expected total damagedealt.                                       Type: float.
    #   The element at index 1 indicates whether the target is defeated.                                Type: bool.
    #   The element at index 2 indicates the time left when target is defeated. -inf if not defeated.   Type: float.
    def progress(self, unitlist: list = None, target: Enemy = None) -> list:
        unitlist = self.unitlist
        target = self.target

        # Initialize output
        dmg_exp = 0 # Expected damage
        kill_time = -float('inf')   # Time remaining when enemy is defeated
        kill = False    # Index indicating enemy is defeated or not

        # While still time left
        while self.timestamp > 0:

            # Skip time countdown if an ultimate is ready
            skip = False
            for i in unitlist:
                if i.info['type'] != 'enemy' and i.ultimate_ready():

                    # Unit i casts ultimate
                    unit_to_move = i
                    damage_exp = unit_to_move.move(self, target,True)
                    skip = True
                    break

            # No ultimates are ready, begin time countdown
            if not skip:

                # Calculate the shortest time needed for the next unit to move
                timestamp_collapse = min([i.basic_stats['until_turn']/i.basic_stats['speed'] for i in unitlist])

                # If time exceeds remaining time, pop out
                if self.timestamp < timestamp_collapse:
                    break
                
                # Otherwise, every unit's runway is decremented
                for i in unitlist:
                    i.basic_stats['until_turn'] -= i.basic_stats['speed'] * timestamp_collapse

                    # Identify the moving unit with runway length 0
                    if i.basic_stats['until_turn'] <= 2 * (10 ** -12):
                        unit_to_move = i
                    
                
                # Decrement time length
                self.timestamp -= timestamp_collapse

                # The unit with runway length 0 moves
                damage_exp = unit_to_move.move(self, target)

            # If the move deals damage
            if damage_exp:
                
                # Add damage of this turn to dmg_exp
                dmg_exp += damage_exp

                # If a character deals damage to the enemy
                if unit_to_move.info['type'] != 'enemy':

                    # Trigger enemy on-hit
                    for i in target.on_hit:

                        # Some skills adding on-hit effects do not inflict the effects themselves. Skip the effect if this is the case.
                        if target.on_hit[i]['after']:
                            target.on_hit[i]['after'] = False
                            continue

                        # Get origin character information
                        character = target.on_hit[i]['origin']

                        # Calculate
                        damage_on_hit = target.on_hit[i]['effect'](character, target)

                        # If the on-hit effect deals damage
                        if damage_on_hit:

                            # Add damage of the effect to dmg_exp
                            dmg_exp += damage_on_hit

            # Print time left to console or notebook
            #print(f'Remaining time: {math.floor(self.timestamp)}\n')

            # Record timestamp if target is defeated
            if not kill and target.basic_stats['remaining_hp'] <= 2 * (10 ** -12):
                kill_time = math.floor(self.timestamp)
                kill = True
                break
        dmg_exp = math.floor(dmg_exp)
                
        return [dmg_exp, kill, kill_time]

    # Start of turn
    def turn_start(self, char: Character, ultimate: bool = False) -> None:

        # Skip if the turn is an ultimate turn
        if ultimate:
            return
        
        # Iterate over all existing buffs that decrements start of turn, and remove expired buffs (remaining turn = 0)
        for i in ['buff','refreshing']:
            buffs = list(char.buffs[i].keys())
            for j in buffs:
                if char.buffs[i][j]['turn'] == float('inf') or char.buffs[i][j]['decrement'] != 'start_turn':
                    continue
                if char.buffs[i][j]['turn'] == 1:
                    for k in char.buffs[i][j]['stats']:
                        char.basic_stats[k] -= char.buffs[i][j]['stats'][k] * char.buffs[i][j]['stack']
                    char.buffs[i].pop(j)
                else:
                    char.buffs[i][j]['turn'] -= 1
        
        char.calc_stats()

    # End of turn
    def turn_end(self, char: Character, ultimate: bool = False) -> None:

        # Skip if the turn is an ultimate turn
        if ultimate:
            return
        
        # Reset runway length
        char.basic_stats['until_turn'] += 10000
        # Iterate over all existing buffs that decrements end of turn, and remove expired buffs (remaining turn = 0)
        for i in ['buff','refreshing']:
            buffs = list(char.buffs[i].keys())
            for j in buffs:
                if char.buffs[i][j]['turn'] == float('inf') or char.buffs[i][j]['decrement'] != 'end_turn':
                    continue
                if char.buffs[i][j]['turn'] == 1:
                    for k in char.buffs[i][j]['stats']:
                        char.basic_stats[k] -= char.buffs[i][j]['stats'][k] * char.buffs[i][j]['stack']
                    char.buffs[i].pop(j)
                else:
                    char.buffs[i][j]['turn'] -= 1

        char.calc_stats()
