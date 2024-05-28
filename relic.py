def genius_condition(target):
    return 'quantum' in target.basic_stats['weakness']

genius = [{'def_pen': 10}, {
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

def arena_condition(wearer):
    return wearer.basic_stats['crit_rate'] >= 70

arena = [{'crit_rate': 8}, {
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