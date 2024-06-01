def genius_condition(target):
    return 'quantum' in target.basic_stats['weakness']

genius = [{
    'type': 'permanant', 
    'stats': {'dmg_boost': 10},
    'stack': 1
}, {
    'type': 'permanant', 
    'stats': {'dmg_boost': 10, 'def_pen': 10},
    'stack': 1
}, {
    'source': 'relic',
    'name': 'genius_4',
    'type': 'on_hit',
    'condition': genius_condition,
    'stats': {'def_pen': 10},
    'stack': 1,
    'max_stack': 1,
    'turn': 0,
    'max_turn': 0
}]

# Planar Ornaments

def space_condition(wearer):
    return wearer.basic_stats['speed'] >= 120

space = [{
    'type': 'permanant', 
    'stats': {'attack_rate': 12},
    'stack': 1
}, {
    'source': 'relic',
    'name': 'space',
    'type': 'conditional',
    'condition': space_condition,
    'stats': {'attack_rate': 12},
    'stack': 1,
    'max_stack': 1,
    'turn': 0,
    'max_turn': 0
}]

def salsotto_condition(wearer):
    return wearer.basic_stats['crit_rate'] >= 50

salsotto = [{
    'type': 'permanant', 
    'stats': {'crit_rate': 8},
    'stack': 1
}, {
    'source': 'relic',
    'name': 'salsotto',
    'type': 'conditional',
    'condition': salsotto_condition,
    'stats': {'ultimate_dmg': 15, 'followup_dmg': 15},
    'stack': 1,
    'max_stack': 1,
    'turn': 0,
    'max_turn': 0
}]
def arena_condition(wearer):
    return wearer.basic_stats['crit_rate'] >= 70

arena = [{
    'type': 'permanant', 
    'stats': {'crit_rate': 8},
    'stack': 1
}, {
    'source': 'relic',
    'name': 'arena', 
    'type': 'conditional',
    'condition': arena_condition,
    'stats':  {'basic_dmg': 20, 'skill_dmg': 20},
    'stack': 1, 
    'max_stack': 1,
    'turn': 0,
    'max_turn': 0
}]



