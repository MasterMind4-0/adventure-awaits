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
    print(f'''
    Change..?

    1. Weapon
    2. Armor
    ''')
    choice = input()
    match choice:
        case '1':
            print(display_inventory())
            weapon = input('New weapon: ').lower().replace(' ', '_')

            if weapon in config.entities['weapons'].keys():
                config.player_weapon = config.entities['weapons'][weapon]
        case '2':
            print(display_inventory())
            armor = input('New armor: ').lower().replace(' ', '_')

            if armor in config.entities['armors'].keys():
                config.player_armor = config.entities['armors'][armor]


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
            pass
        case '2':
            change_equipment()


    wait()
    random.choice(events.eventsls)()
