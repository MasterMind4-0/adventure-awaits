import config
import colors
import random
from events import alley_way
from utils import talk, format_name

class tavern:
    def __init__(self, tavern_display_name: str):
        self.player_leaving = False
        self.bartender_namels = [
            "Vicar",
            "Warin",
            "Gaillart",
            "Ernold"
        ]
        self.bartender_greetingls = [
            'How are you doing today?',
            'What can I get you?',
            "We don't have virgin here for the record.", 
            "I feel sorry for people who don't drink. When they wake up in the morning, that's as good as they're going to feel all day."
        ]
        self.bartender_buydrinkls = [
            'That there is a good drink.',
            'You vomit outside, not on me, got it?',
            'Your order.'
        ]
        self.bartender_leavels = [
            'Pleasure doing business.',
            'Hope to see you again.',
            'Until you order again.',
            "Hey! You didn't vomit on me!",
            "Be sure to head my way when your head clears again."
        ]

        # Picking special drink and also the normal ones
        drinksls = list(config.entities['drinks'].keys())
        spec_drinksls = list(config.entities['spec_drinks'].keys())

        self.tavern_drinks = random.sample(drinksls, k=3)
        self.tavern_special_drink = random.choice(spec_drinksls)

        self.tavern_display_name = tavern_display_name

    
    def entering_tavern(self):
        talk(f'You enter, the smell of ale-soaked bread crusts fill your nose.')
        talk(f'{format_name('Bartender')}: Welcome to {self.tavern_display_name}!')
        while True:
            if self.player_leaving:
                break
            choice = self.tavern_menu()

            match choice:
                case '1':
                    self.bartender_menu()
                case '2':
                    self.quest_board_menu()
                case '3':
                    self.room_menu()
                case '4':
                    self.gossip()
                case '5':
                    break
        return
    
    def tavern_menu(self):
        while True:
            print(f'''
            {colors.TITLE}{self.tavern_display_name}{colors.END}

            Coin: {colors.GOLD}{config.coin}{colors.END}

            1. Bartender
            2. Quest Board
            3. Rooms
            4. Gossip
            5. Leave
            ''')
            choice = input()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            talk('Invalid answer. Try again.', True)
    
    def bartender_menu(self):
        self.bartender_display_name = random.choice(self.bartender_namels)
        bartender_greeting = random.choice(self.bartender_greetingls)
        bartender_leave = random.choice(self.bartender_leavels)
        self.rootdict_drinks = config.entities['drinks']
        self.rootdict_spec_drinks = config.entities['spec_drinks']

        talk(f'{format_name('Bartender')}: Name\'s {self.bartender_display_name}.', True, 1)
        talk(f'{format_name(self.bartender_display_name)}: {bartender_greeting}', True, 1.5)
        while True:
            print(f'''
            ---~~~### {colors.TITLE}{self.tavern_display_name}{colors.END} ###~~~---

            Coins: {colors.GOLD}{config.coin}{colors.END}

            Drinks:
                1. {self.rootdict_drinks[self.tavern_drinks[0]]['display_name']} ({colors.GOLD}{self.rootdict_drinks[self.tavern_drinks[0]]['price']}{colors.END})
                2. {self.rootdict_drinks[self.tavern_drinks[1]]['display_name']} ({colors.GOLD}{self.rootdict_drinks[self.tavern_drinks[1]]['price']}{colors.END})
                3. {self.rootdict_drinks[self.tavern_drinks[2]]['display_name']} ({colors.GOLD}{self.rootdict_drinks[self.tavern_drinks[2]]['price']}{colors.END})
            
            Tavern\'s Special:
                SPEC. {self.rootdict_spec_drinks[self.tavern_special_drink]['display_name']} ({colors.GOLD}{self.rootdict_spec_drinks[self.tavern_special_drink]['price']}{colors.END})
                        {self.rootdict_spec_drinks[self.tavern_special_drink]['description']}
            ''')
            choice = input()
            if choice.lower() in ['1', '2', '3', 'spec']:
                break
            talk('Invalid answer. Try again.', True)
        self.purchased_drink(choice)
    
    def purchased_drink(self, drink_chose: str):
        bartender_buydrink = random.choice(self.bartender_buydrinkls)

        match drink_chose:
            case '1':
                drink = self.rootdict_drinks[self.tavern_drinks[0]]
            case '2':
                drink = self.rootdict_drinks[self.tavern_drinks[1]]
            case '3':
                drink = self.rootdict_drinks[self.tavern_drinks[2]]
            case _:
                drink = self.rootdict_spec_drinks[self.tavern_special_drink]
        if config.coin < drink['price']:
            talk(f'{format_name(self.bartender_display_name)}: Hey there, this ain\'t a charity, you got to have enough money for this liquor here.')
            self.bartender_menu()
        
        talk(f'{format_name(self.bartender_display_name)}: {bartender_buydrink}')

        talk(f'You take your drink, peering into the liquid that swirls around the glass.')
        talk(f'{format_name(config.name)}: Well, bottoms up, I suppose.')
        talk(f'{format_name(self.bartender_display_name)}: Bottoms up.', True, 1)

        compared_value = random.random()
        drunk_chance = drink['drunk_effective'] - config.player_stats['constitution']
        wasted = False

        if compared_value < drunk_chance:
            wasted = True
        if config.dev_mode:
            print(f'{colors.DEV}Drunk chance: {drunk_chance}\nCompared value: {compared_value}{colors.END}')

        if wasted:
            talk(f'Your head suddenly thumps.')
            talk(f'{format_name(config.name)}: That\'sssss goooood sssssstuuff! *hick*')
            talk(f'{format_name(self.bartender_display_name)}: Yeah, thanks ya\' drunk basta...')
            talk(f'Your eye lids close and the world sleeps... For a moment.')
            alley_way(True)
            self.player_leaving = True
        else:
            try: # Basically, if var drink doesn't have the key 'con_exp' (aka, is a normal drink; not special) then it will pass do to an error
                config.player_stats['constitution'] += drink['con_exp']
            except:
                pass
                    
            talk('You bring the glass back down, it thumps to the table.')
            talk(f'{format_name(config.name)}: That\'s good stuff.')
            talk(f'{format_name(self.bartender_display_name)}: Aye, care for more?')
        return