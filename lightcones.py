def in_the_night(wearer, target, r: int, first_time: bool) -> dict:
    if first_time:
        wearer.basic_stats['base_attack'] += 582
        wearer.basic_stats['crit_rate'] += 15 + r * 3
    speed = wearer.basic_stats['speed']
    index = min(6, (speed - 100) // 10) if speed >= 100 else 0
    return {
        'name': 'in_the_night',
        'type': 'lightcone',
        'func': in_the_night,
        'basic_dmg': (r+5),
        'skill_dmg': (r+5),
        'ultimate_crit_dmg': (2 * r+10),
        'change': ['speed'],
        'turn': float('inf'),
        'stack': index
    }