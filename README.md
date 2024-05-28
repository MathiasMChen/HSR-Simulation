# HSR-Simulation
 
Contains simple Honkai: Star Rail battle simulations.

**Final outcome: Able to calculate team damage against an arbitary selected in-game boss during given time length. Enemy does not take action during its turn, ensuring every member on player's team does not die or take debuff, but turn count will collapse for debuffs on enemy.**

### STEP I: Build a foundation database logistic, including base stats and abilities of characters, lightcones, and relics.

Related files: character_buffs.py, relic.py, lightcones.py.

character_buffs.py stores buffs that characters can inflict on themselves, allies, or enemies.

character.py stores logistics of setups and abilities of different characters, one for each class.

relic.py stores relic buffs.

lightcones.py stores lightcone buffs.

All files contain the minimal data needed to check program viability.

### STEP II: Connect these databases to form a character profile.

Related files: character.py.

character_template.py connects four databases above to form a complete character.

### STEP III: Create a battle simulation environment.

Related file: battle_simulations.py

battle_simulations.py contains all logistics needed for a battle to perform. In the future, timestamp related things will fall in this file.

**MILESTONE I: Calculate single character damage to a single target on a single hit with manual input (buffs from allies, status of enemy). Single timestamp.**

### STEP IV: Create more method in battle simulation environment to allow timeflow.

Related file: battle_simulations.py

*I'm currently here!*

**MILESTONE II: Calculate single character damage to a single target in a time interval with manual input (buffs from allies, status of enemy). Taking into account energy.**

### STEP V: Complete database

Related files: character_buffs.py, relic.py, lightcones.py.

Update these files with complete data from HSR.

### STEP VI: Allows team build.

**MILESTONE III: Calculate team damage to a single target in a time interval.**

### STEP V: Build an enemy database.

**MILESTONE IV: Calculate team damage to any in-game enemy boss.**

*More to be developed*
