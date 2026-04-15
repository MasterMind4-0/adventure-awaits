import time
import random
import config
import events
import colors
from systems.battle import battle
from systems.tavern import tavern
from utils import talk, wait, display_inventory

config.name = input('What is your character\'s name?\n')
if config.name.lower() != 'dev':
    config.coin = 0
    config.inventory = []
    config.player_armor = config.entities['armors']['no_armor']
    config.player_weapon = config.entities['weapons']['shortsword']
    config.dev_mode = False
talk(f'{config.name} is quite a good one.')

def change_equipment():
    while True:
        print(f'''
        Change..?

        1. Weapon
        2. Armor

        3. Return to previous menu
        ''')
        choice = input()
        print(display_inventory())
        match choice:
            case '1':
                to_be_swapped = input('New weapon: ').lower().replace(' ', '_')
                category = 'weapons'
                break

            case '2':
                to_be_swapped = input('New armor: ').lower().replace(' ', '_')
                category = 'armors'
                break

            case '3':
                return

            case _:
                talk('ERROR. Try again.')

    while True:
        if to_be_swapped in config.entities[category].keys() and to_be_swapped in config.inventory:
            if category == 'armors':
                config.player_armor = config.entities[category][to_be_swapped]
            elif category == 'weapons':
                config.player_weapon = config.entities[category][to_be_swapped]
            break
        else:
            talk(f'{to_be_swapped} isn\'t in your inventory!')
            break

while True:
    print(f'''
    ---~~~### {colors.TITLE}{config.name}{colors.END} ###~~~---

    Health: {colors.HEALTH}{config.player_health}{colors.END}
    Coins: {colors.GOLD}{config.coin}{colors.END}

    Inventory:
        {display_inventory()}

    Equipped Weapon: {colors.EQUITABLE}{config.player_weapon['display_name']}{colors.END}
    Equipped Armor: {colors.EQUITABLE}{config.player_armor['display_name']}{colors.END}

    1. Continue traveling
    2. Change equipment
    ''')
    choice = input()
    match choice:
        case '1':
            wait()
            random.choice(events.eventsls)()
        case '2':
            change_equipment()
