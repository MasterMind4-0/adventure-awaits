import colors
import time
import config
import random
from utils import talk, format_name, display_inventory

class shop:
    def __init__(self, pool_category: str, shop_name: str, trader_name: str = 'Trader', item_pool: list = None):
        self.shop_name = shop_name
        self.trader_name = trader_name

        self.pool_category = pool_category
        if item_pool:
            self.item_pool = item_pool
        else:
            self.item_pool = self.generate_random_item_pool()
    
    def shop_menu(self):
        traded = False
        trader_intros = [
            'What can I do you for?',
            'What will it be today?',
            'Anything catching your eye?',
            "Don't bargin, I am not going to give in.",
            "I don't do sales."
        ]
        trader = format_name(self.trader_name)

        talk(f'{trader}: {random.choice(trader_intros)}')

        while True:
            print(f'''
            ---~~~### {colors.TITLE}{self.shop_name}{colors.END} ###~~~---

            Coins: {colors.GOLD}{config.coin}{colors.END}

            Inventory:
                {display_inventory()}
            ''')

    def generate_random_item_pool(self):
        viable_items = []
        chosen_item_amount = random.randint(3, 6)

        for item in config.entities[self.pool_category].keys():
            if config.entities[self.pool_category][item]['in_shop']:
                viable_items.append(item)
        
        return random.sample(viable_items, k=chosen_item_amount)