from randombool import rand

def break_overall(character, target) -> None:
    #print(f'{character.info['name']} breaks enemy\'s toughness!')
    target.basic_stats['recover'] += 1
    target.basic_stats['break'] = True
    target.basic_stats['toughness_resist'] = 0
    target.basic_stats['until_turn'] += 2500

def break_dmg(character, target) -> float:
    dmg_base_ratio = target.basic_stats['max_toughness'] / 120 + 0.5
    base_break_dmg = 3767.5533
    break_effect_ratio = (1 + character.basic_stats['break_effect'] / 100)
    dmg = base_break_dmg * dmg_base_ratio
    dmg *= break_effect_ratio
    return dmg

def break_recover(target) -> None:
    #print('Enemy recovers from break.')
    target.basic_stats['break'] = False
    target.basic_stats['toughness_resist'] = 10
    target.basic_stats['toughness'] = target.basic_stats['max_toughness']

def quantum_break_helper(character, target) -> list:
    if target.dot['quantum_break']['stack'] < target.dot['quantum_break']['max_stack']:
        target.dot['quantum_break']['stack'] += 1
    return 0

def quantum(character, target) -> float:
    break_overall(character,target)
    instant_damage = break_dmg(character, target) * 0.5
    margin = 150 * (100+character.basic_stats['effect_hit_rate']) * (100-target.basic_stats['effect_res_rate']) / 10000
    if rand(margin):
        #print(f'Quantum break effect applied with {round(margin,1)}% chance.')
        target.basic_stats['until_turn'] += 2000 * (1 + character.basic_stats['break_effect'] / 100)
        target.dot['quantum_break'] = {
            'name': 'quantum_break',
            'damage': break_dmg,
            'origin': character,
            'ratio': 0.6,
            'stack': 1,
            'max_stack': 5,
            'turn': 1
        }
        target.on_hit['quantum_break'] = {
            'effect': quantum_break_helper, 
            'origin': character,
            'after': True,
            'turn': 1
        }
    else:
        margin *= 1
        #print(f'Quantum break effect resisted with {100-round(margin,1)}% chance.')
    target.basic_stats['remaining_hp'] -= instant_damage
    #print(f'Enemy Remaining HP: {target.basic_stats['remaining_hp']} / {target.basic_stats['max_hp']}')
    return instant_damage