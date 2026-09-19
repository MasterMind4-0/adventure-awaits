import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_inventory_change, player_mc

tags = {
    'is_quest': False
}
possible_attackers = []
for enemy in config.entities['enemies'].keys():
    if 'Forest' in config.entities['enemies'][enemy]['tags']:
        possible_attackers.append(enemy)


intro_sentence = [
    'As you were walking along a weaving path in a forest,',
    'You were simply just walking about on the beaten road when, suddenly,'
]

def journey_attack():
    attacker = random.choice(possible_attackers)
    attacker_name = format_name(config.entities['enemies'][attacker]['display_name'])
    introduction = random.choice(intro_sentence)

    talk(introduction)

    if calculate_chance(.3):
        talk('You notice a figure hiding near you, you get the jump on the creature.')
        battle(attacker, True).fight_start()
    else:
        talk(f'A {attacker_name} pounces at you.')
        battle(attacker).fight_start()