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

merchants = [
    ["Fishmonger", "Fish! Fish! Get ya' fish here!"],
    ["Mercer", "Fine silks! Fine silks and cotton from exotic places!"]
]

tradable_merchants = [
    ['Armorer', 'armors'],
    ['Weapon Smith', 'weapons'],
    ['Mage', 'potions']
]

def town_market():
    merchant = random.choice(merchants)
    merchant_phrase = merchant[1]
    merchant_name = format_name(merchant[0])
    
    # Assigning shops encountered
    merchant1 = random.choice(tradable_merchants)
    merchant2 = random.choice(tradable_merchants)
    merchant3 = random.choice(tradable_merchants)
    
    shop1 = shop(merchant1[1], merchant1[0], merchant1[0])
    shop2 = shop(merchant2[1], merchant2[0], merchant2[0])
    shop3 = shop(merchant3[1], merchant3[0], merchant3[0])
    
    talk('You\'re passing through a town and happen to find yourself in the bustling local market.')
    talk(f'{merchant_name}: {merchant_phrase}')
    talk('You walk on, but spot a merchant who may have some use...', 2)
    shop1.shop_menu()
    talk('You walk off, but another drags you in. Fortunately, their stock seems interesting.', 2)
    shop2.shop_menu()
    talk('You finally get through all the merchants...')
    talk('Or so you though, another, cheerful fellow, comes towards you.', 2)
    shop3.shop_menu()
    talk('You decided to take a hidden alley to avoid any further interruption, you manage to make it out. ')