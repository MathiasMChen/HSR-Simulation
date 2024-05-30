# HSR-Simulation
 
Contains simple Honkai: Star Rail battle simulations.

Brief introduction:

Characters in HSR have three systems affecting their stats: their unique traces, skillsets, and eidolons; lightcones; and relics. They can offer base stats as well as various buffs in battle.

Battle in HSR follows a turn-based format, while every unit has different "speed" values to determine the length of time between its two moves.

In a unit's turn, it has two choices of action: basic attack, or use skill.

During combat, allied units can accumulate energy. When the energy reaches its maximum, the unit can use its ultimate for an instant extra move, casting its ultimate ability, and reset the energy.

Units can inflict various buffs or debuffs on themselves, their teammates, and enemies. Every buff has a unique duration counted in turn, some require the hit enemy to meet certain conditions when doing damage (I call them on-hit buffs), some require conditions on the player side to be met (I call them conditional buffs), and some can change effects when the stats of a unit change (I call them refreshing buffs).

When doing damage, every buff and debuff is taken into account, and we yield a number after calculation, indicating the raw damage.

Units have chances to do critical damage. The chance and damage are determined by the unit's 'crit_rate' and 'crit_dmg' attributes. Note that the 'crit_dmg' here refers to the extra damage when the hit is a critical hit. Thus, a 50% value indicates a critical damage of 150% of the raw damage.

Taking into account critical damage, we yield two more damage values: damage when crit, and expectation of damage.

**Output: an array, the first number is raw damage, the second is the expectation of damage, and the third is critical damage.**

For instance, if the raw damage is 10000, crit_rate is 80%, and crit_dmg is 200%, our expectation would be 10000 * (1 + 80% * 200%) = 26000, and our critical damage would be 10000 * (1 + 200%) = 30000. Thus, our output is [10000, 26000, 30000]. Note that crit_rate exceeding 100% behaves the same as 100%, as both indicate there is 100% for the damage to be critical.

***Outcome: Calculate team damage against an arbitrarily selected in-game boss during a given time length, counted in turn. The enemy does not take action during its turn, ensuring every member of the player's team does not die or take debuff, but the turn count will collapse for debuffs on the enemy.***

## STEP I: Build a foundation database logistics, including base stats and abilities of characters, lightcones, and relics

Related files: character_buffs.py, character.py, relic.py, lightcones.py.

character_buffs.py stores buffs that characters can inflict on themselves, allies, or enemies.

character.py stores the logistics of setups and abilities of different characters, one for each class.

relic.py stores relic buffs.

lightcones.py stores lightcone buffs.

All files contain the minimal data needed to check program viability. (1 character, 2 sets of relics, 1 lightcone.)

## STEP II: Connect these databases to form a character profile

Related files: character.py.

character_template.py connects the four databases above to form a complete character.

## STEP III: Create a battle simulation environment

Related file: battle_simulations.py

battle_simulations.py contains all the logistics needed for a battle to perform. In the future, timestamp-related things will fall in this file.

**MILESTONE I: Calculate single character damage to a single target on a single hit with manual input (buffs from allies, status of enemy). Single timestamp.**

## STEP IV: Create more methods in the battle simulation environment to allow time flow.

Related file: battle_simulations.py

*I'm currently here!*

**MILESTONE II: Calculate single character damage to a single target in a time interval with manual input (buffs from allies, status of enemy). Taking into account energy.**

## STEP V: Complete database

Related files: character_buffs.py, relic.py, lightcones.py.

Update these files with complete data from HSR.

## STEP VI: Allows team build

**MILESTONE III: Calculate team damage to a single target in a time interval.**

## STEP V: Build an enemy database

**MILESTONE IV: Calculate team damage to any in-game enemy boss.**

### More to be developed
