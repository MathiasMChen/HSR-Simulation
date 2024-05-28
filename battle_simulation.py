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
