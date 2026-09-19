import colors
import time
import config
import random
from utils import talk, format_name, display_inventory, player_inventory_change

class shop:
    def __init__(self, pool_category: str, shop_name: str, trader_name: str = 'Trader', item_pool: list = None):
        self.shop_name = shop_name
        self.trader_name = trader_name
        self.trader_formatted = format_name(self.trader_name)

        match pool_category:
            case 'enemies':
                raise ValueError('Enemies are not a valid category')
            case _:
                self.pool_category = pool_category

        if item_pool:
            self.item_pool = item_pool
        else:
            self.item_pool = self.generate_random_item_pool()
    
    def shop_menu(self):

        trader_intros = [
            'What can I do you for?',
            'What will it be today?',
            'Anything catching your eye?',
            "Don't bargin, I am not going to give in.",
            "I don't do discounts."
        ]

        talk(f'{self.trader_formatted}: {random.choice(trader_intros)}')
        while True:
            # If self.chosen_items is empty
            if not self.chosen_items:
                talk(f'{self.trader_formatted}: Well, you won\'t believe it but you cleared me of all my stock!')
                talk(f'{self.trader_formatted}: I appreciate the business, until we see each other once again!')
                break

            print(f'''
            ---~~~### {colors.TITLE}{self.shop_name}{colors.END} ###~~~---
            
            {self.get_shop_items()}

            Coins: {colors.GOLD}{config.coin}{colors.END}

            Inventory:
                {display_inventory()}

            L for leaving
            ''')
            choice = input()
            if choice.lower() == 'l':
                break
            self.purchased_item(int(choice) - 1)
    
    def purchased_item(self, choice):
        item_dict_link = config.entities[self.pool_category][self.chosen_items[choice]]

        talk(f'{self.trader_formatted}: Ah! That\'s a good one!')
        talk(f'{self.trader_formatted}: It\'ll be {item_dict_link["price"]} coins.')
        if config.coin < item_dict_link['price']:
            talk(f"{config.name}: Um... I don\'t think I can actually afford that...")
            talk(f'{self.trader_formatted}: Yeah, come back when you got the money.')
            # Implement trading option if you don't have enough money
        else:
            self.chosen_items.remove(item_dict_link['name'])

            player_inventory_change(coins=-item_dict_link['price'])
            player_inventory_change(items=item_dict_link['name'])

            talk(f'{self.trader_formatted}: Pleasure doing business!')
        return

    def generate_random_item_pool(self):
        viable_items = []
        #chosen_item_amount = random.randint(3, 6)
        chosen_item_amount = 2

        for item in config.entities[self.pool_category].keys():
            if config.entities[self.pool_category][item]['in_shop']:
                viable_items.append(item)
        
        self.chosen_items = random.sample(viable_items, k=chosen_item_amount)

    def get_shop_items(self):
        printed_output = ""

        for item in self.chosen_items:
            printed_output += f'{self.chosen_items.index(item) + 1}. {config.entities[self.pool_category][item]["display_name"]} ({config.entities[self.pool_category][item]["price"]})\n\t    '

        return printed_output