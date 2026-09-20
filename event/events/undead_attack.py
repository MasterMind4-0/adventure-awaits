import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_inventory_change, player_mc

tags = {
    'is_quest': False,
    'natural': True
}
for enemy in config.entities['enemies'].keys():
    if 'Undead' in config.entities['enemies'][enemy]['tags']:
        chosen_enemy = enemy

def undead_attack():
    talk('You come across a dead body, its skeleton showing through the rotton flesh.')
    choice = player_mc(['Loot the body', 'Bury the body'], leave_option_text='Walk away')
    if choice == '0':
        player_inventory_change(random.randint(6, 14))
        if calculate_chance(.6):
            talk('After you loot the body, it suddenly animates.')
            battle(chosen_enemy).fight_start('It screeches and lunges at you.')
            talk('You wipe the sweat off your brow.')
            talk('You also loot the body and find a couple coins.')
        else:
            talk('You loot the body of its past life\'s belongings.')
    elif choice == '1':
        if calculate_chance(.4):
            talk('The body animates as you come near,')
            battle(chosen_enemy).fight_start('It screeches and lunges at you.')
            talk('Once you kill the undead. You bury the body.')
            talk('You wipe the sweat off your brow as you leave.')
        else:
            talk('You bury the body, say your prayers, and leave.')
    elif choice == 'l':
        talk('You decided to leave, best to leave the dead to the body collectors.')
    return