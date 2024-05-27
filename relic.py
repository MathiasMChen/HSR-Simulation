def genius_condition(wearer, target):
    return {'name': 'genius', 'stack': 1, 'turn': float('inf'), 'func': genius_condition} if 'quantum' not in target.basic_stats['weakness'] else {'name': 'genius', 'stack': 1, 'func': genius_condition, 'turn': float('inf'),'def_pen': 10}

genius = [{'def_pen': 10}, {'name': 'genius', 'stack': 1, 'func': genius_condition, 'turn': float('inf')}]

def arena_condition(wearer, target):
    return {'name': 'arena', 'stack': 1, 'func': arena_condition, 'turn': float('inf')} if wearer.basic_stats['crit_rate'] < 70 else {'name': 'arena', 'stack': 1, 'func': arena_condition, 'basic_dmg': 20, 'skill_dmg': 20, 'turn': float('inf')}

arena = [{'crit_rate': 8}, {'name': 'arena', 'stack': 1, 'func': arena_condition, 'turn': float('inf')}]