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
    def __init__(self, timestamp, sp=3) -> None:
        self.timestamp = timestamp
        self.skill_point = sp
    
    # Repeatedly call move() in character until time collapsed or enemy defeated
    def progress(self, unitlist: list, target):

        # Store damage in the form of [base damage, expected damage, critical damage]
        dmg = [0,0,0]

        # While still time left
        while self.timestamp > 0:

            # Skip time countdown if an ultimate is ready
            skip = False
            for i in unitlist:
                if i.info['type'] != 'enemy' and i.ultimate_ready():

                    # Unit i casts ultimate
                    unit_to_move = i
                    damage = unit_to_move.move(self, target,True)
                    skip = True
                    break

            # No ultimates are ready, begin time countdown
            if not skip:

                # Calculate the shortest time needed for the next unit to move
                timestamp_collapse = min([i.basic_stats['until_turn']/i.basic_stats['speed'] for i in unitlist])

                # If time exceeds remaining time, pop out
                if self.timestamp < timestamp_collapse:
                    return [math.floor(i) for i in dmg]
                
                # Otherwise, every unit's runway is decremented
                for i in unitlist:
                    i.basic_stats['until_turn'] -= i.basic_stats['speed'] * timestamp_collapse

                    # Identify the moving unit with runway length 0
                    if i.basic_stats['until_turn'] <= 2 * (10 ** -12):
                        unit_to_move = i
                    
                
                # Decrement time length
                self.timestamp -= timestamp_collapse

                # The unit with runway length 0 moves
                damage = unit_to_move.move(self, target)

            if damage[0] != None:
                
                # Add damage of this turn to dmg
                for i in range(len(dmg)):
                    dmg[i] += damage[i]
                
                # Decrement target hp based on expected damage
                target.basic_stats['remaining_hp'] -= damage[1]

                if unit_to_move.info['type'] != 'enemy':
                    # Inflict target on-hit if deals damage
                    for i in target.on_hit:
                        if target.on_hit[i]['after']:
                            target.on_hit[i]['after'] = False
                            continue
                        character = target.on_hit[i]['origin']
                        damage_on_hit = target.on_hit[i]['effect'](character, target)
                        if damage_on_hit[0] != None:
                            for i in range(len(dmg)):
                                dmg[i] += damage_on_hit[0][i]
                            target.basic_stats['remaining_hp'] -= damage_on_hit[0][1]
                            print(damage_on_hit[0])
                        if damage_on_hit[1] != []:
                            for k in damage_on_hit[1]:
                                for j in k['stats']:
                                    character.basic_stats[j] -= k['stats'][j] * k['stack']
                            character.calc_stats()

            # Print time left to console or notebook
            print(math.floor(self.timestamp))

            # Break out if target is defeated
            if target.basic_stats['remaining_hp'] <= 2 * (10 ** -12):
                break
        return [math.floor(i) for i in dmg]

