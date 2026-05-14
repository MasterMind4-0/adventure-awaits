import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from systems.shop import shop
from utils import talk, format_name, wait, calculate_chance, player_var_change, player_mc

tags = {
    'is_quest': False
}

possible_item_pools = [
    'potions',
    'weapons',
    'armors'
]

def traveling_trader():
    trader = format_name('Traveling Merchant')

    talk('A merchant, with their backpack filled to the brim with ites, comes towards you.')
    talk(f'{trader}: Well hello there! Care to view my stores?')
    talk(f'The merchant wiped sweat off his brow.')
    choice = player_mc(['Yes', 'No'], 'View the merchant\'s stock?', leave_option=False)
    if choice == '0':
        talk('The merchant smiles,')
        talk(f'{trader}: Fabulous! Take your pick!')
        shop(random.choice(possible_item_pools), 'Traveling Merchant', 'Traveling Merchant').shop_menu()
    else:
        talk('The trader walks away in solom.')