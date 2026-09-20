import time
import random
import config
import event.events_main as events
import colors
from systems.battle import battle
from systems.tavern import tavern
from utils import talk, wait, display_inventory, player_mc

last_event = None



print('''
------------------------------------------------------------------------------------------------------------
   _____       .___                    __                            _____                 .__  __          
  /  _  \    __| _/__  __ ____   _____/  |_ __ _________   ____     /  _  \__  _  _______  |__|/  |_  ______
 /  /_\  \  / __ |\  \/ // __ \ /    \   __\  |  \_  __ \_/ __ \   /  /_\  \ \/ \/ /\__  \ |  \   __\/  ___/
/    |    \/ /_/ | \   /\  ___/|   |  \  | |  |  /|  | \/\  ___/  /    |    \     /  / __ \|  ||  |  \___ \ 
\____|__  /\____ |  \_/  \___  >___|  /__| |____/ |__|    \___  > \____|__  /\/\_/  (____  /__||__| /____  >
        \/      \/           \/     \/                        \/          \/             \/              \/ 
------------------------------------------------------------------------------------------------------------
''')

config.name = input('What is your character\'s name?\n')
if config.name.lower() != 'dev':
    config.coin = 0
    config.inventory = []
    config.player_armor = config.entities['armors']['no_armor']
    config.player_weapon = config.entities['weapons']['shortsword']
    config.dev_mode = False
talk(f'{config.name} is quite a good one.')

def change_equipment():
    if not config.inventory:
        talk('You\'re inventory is empty!')
        return
    
    while True:
        if config.player_health > config.player_max_health:
            config.player_health = config.player_max_health
        choice = player_mc(['Weapon', 'Armor'], "Change..?", "Return")
        print(display_inventory())
        match choice:
            case '0':
                to_be_swapped = input('New weapon: ').lower().replace(' ', '_')
                category = 'weapons'
                break

            case '1':
                to_be_swapped = input('New armor: ').lower().replace(' ', '_')
                category = 'armors'
                break

            case 'l':
                return

            case _:
                talk('ERROR. Try again.')

    while True:
        if to_be_swapped in config.entities[category].keys() and to_be_swapped in config.inventory:
            if category == 'armors':
                
                config.inventory.remove(to_be_swapped)
                config.inventory.append(config.player_armor['name'])
                config.player_armor = config.entities[category][to_be_swapped]
            elif category == 'weapons':
                config.inventory.remove(to_be_swapped)
                config.inventory.append(config.player_armor['name'])
                config.player_weapon = config.entities[category][to_be_swapped]
            break
        else:
            talk(f'{to_be_swapped} isn\'t in your inventory!')
            break

def get_random_event():
    global last_event
    event_list = events.eventsls

    chosen_event = random.choice(event_list)
    while chosen_event == last_event:
        chosen_event = random.choice(event_list)

    last_event = chosen_event
    return chosen_event


# Main gameplay loop
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
            get_random_event()()
        case '2':
            change_equipment()
