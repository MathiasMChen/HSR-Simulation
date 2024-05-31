import math

# Start of turn, decrement remaining buff durations by 1 and remove any expired buffs
def turn_start(self, ultimate = False):
    # Skip if the turn is an ultimate turn
    if ultimate:
        return
    
    # Iterate over all existing buffs that decrements start of turn
    buffs = list(self.buffs.keys())
    for i in buffs:
        if self.buffs[i]['decrement'] == 'end_turn':
            continue
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
        self.basic_stats['until_turn'] += 10000
    
    # Iterate over all existing buffs that decrements end of turn
    buffs = list(self.buffs.keys())
    for i in buffs:
        if self.buffs[i]['decrement'] == 'start_turn':
            continue
        if self.buffs[i]['turn'] == 1:
            for j in self.buffs[i]['stats']:
                self.basic_stats[j] -= self.buffs[i]['stats'][j] * self.buffs[i]['stack']
            self.buffs.pop(i)
        else:
            self.buffs[i]['turn'] -= 1
    
    # Remove one-time on-hit and conditional buffs
    for i in applied_buffs:
        for j in i['stats']:
            self.basic_stats[j] -= i['stats'][j] * i['stack']
    self.calc_stats()

class Battle():

    # Initialize desired time length and skill point
    def __init__(self, timestamp, unitlist: list, target, sp=3) -> None:
        self.timestamp = timestamp
        self.skill_point = sp
        self.unitlist = unitlist
        self.target = target
    
    # Repeatedly call move() in character until time collapsed or enemy defeated
    def progress(self, unitlist: list = None, target = None):
        unitlist = self.unitlist
        target = self.target

        dmg_exp = 0
        kill_time = -float('inf')
        kill = False
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

            if damage_exp:
                
                # Add damage of this turn to dmg
                dmg_exp += damage_exp

                if unit_to_move.info['type'] != 'enemy':
                    # Inflict target on-hit if deals damage
                    for i in target.on_hit:
                        if target.on_hit[i]['after']:
                            target.on_hit[i]['after'] = False
                            continue
                        character = target.on_hit[i]['origin']
                        damage_on_hit = target.on_hit[i]['effect'](character, target)
                        if damage_on_hit[1]:
                            dmg_exp += damage_on_hit[1]
                        if damage_on_hit[0]:
                            for k in damage_on_hit[0]:
                                for j in k['stats']:
                                    character.basic_stats[j] -= k['stats'][j] * k['stack']
                            character.calc_stats()

            # Print time left to console or notebook
            #print(math.floor(self.timestamp))

            # Record timestamp if target is defeated
            if not kill and target.basic_stats['remaining_hp'] <= 2 * (10 ** -12):
                kill_time = self.timestamp
                kill = True
                break
                
        return [dmg_exp, kill, kill_time]

