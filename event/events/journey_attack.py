import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_var_change, player_mc

tags = {
    'is_quest': False
}

possible_attackers = [
    'bear',
    'thug',
    'goblin'
]
intro_sentence = [
    'As you were walking along a weaving path in a forest,',
    'You were simply just walking about on the beaten road when, suddenly,'
]

def journey_attack():
    attacker = random.choice(possible_attackers)
    attacker_name = format_name(attacker)
    introduction = random.choice(intro_sentence)

    talk(introduction)

    if calculate_chance(.3):
        talk('You notice a figure hiding near you, you get the jump on the creature.')
        battle(attacker, True).fight_start()
    else:
        talk(f'a {attacker_name} pounces at you.')
        battle(attacker).fight_start()


