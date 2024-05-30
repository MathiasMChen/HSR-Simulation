import math
# Start of turn, decrement remaining buff durations by 1 and remove any expired buffs
def turn_start(self, ultimate = False):
    if ultimate:
        return
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
        self.basic_stats['until_turn'] += 10000
    
    # Remove one-time on-hit and conditional buffs
    for i in applied_buffs:
        for j in i['stats']:
            self.basic_stats[j] -= i['stats'][j] * i['stack']
    self.calc_stats()

class Battle():
    def __init__(self, timestamp) -> None:
        self.timestamp = timestamp
        self.skill_point = 3
    
    def progress(self, unitlist: list, target):
        dmg = [0,0,0]
        while self.timestamp > 0:
            skip = False
            for i in unitlist:
                if i.ultimate_ready():
                    unit_to_move = i
                    damage = unit_to_move.move(self, target,True)
                    skip = True
                    break
            if not skip:
                for i in unitlist:
                    if i.basic_stats['until_turn'] > 10000:
                        raise ValueError("Until_turn exceeds 10000.") 
                timestamp_collapse = min([i.basic_stats['until_turn']/i.basic_stats['speed'] for i in unitlist])
                if self.timestamp < timestamp_collapse:
                    return dmg
                for i in unitlist:
                    i.basic_stats['until_turn'] -= i.basic_stats['speed'] * timestamp_collapse
                    if i.basic_stats['until_turn'] <= 2 * (10 ** -12):
                        unit_to_move = i
                damage = unit_to_move.move(self, target)
                self.timestamp -= timestamp_collapse
            for i in range(len(dmg)):
                dmg[i] += damage[i]
            target.basic_stats['remaining_hp'] -= damage[1]
            print([math.floor(i) for i in dmg])
            print(math.floor(self.timestamp))
            if target.basic_stats['remaining_hp'] <= 0:
                break
        return [math.floor(i) for i in dmg]

