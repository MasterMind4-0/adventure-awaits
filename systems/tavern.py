import config
import colors
import random
import event.events_main as events
from utils import talk, format_name, wait, player_gained_exp, player_inventory_change, player_mc, calculate_chance

class tavern:
    def __init__(self, tavern_display_name: str | list):
        self.player_leaving = False
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

        # Tavern drinks
        drinksls = list(config.entities['drinks'].keys())
        spec_drinksls = list(config.entities['spec_drinks'].keys())

        self.tavern_drinks = random.sample(drinksls, k=3)
        self.tavern_special_drink = random.choice(spec_drinksls)

        # Room mechanic
        self.room_price = random.randint(5, 15)
        self.purchased_room = False

        # Quest mechanic
        self.selected_quests = []
        
        if isinstance(tavern_display_name, list):
            self.tavern_display_name = random.choice(tavern_display_name)
        else:
            self.tavern_display_name = tavern_display_name

    def entering_tavern(self):
        talk(f'You enter, the smell of ale-soaked bread crusts fill your nose.')
        talk(f'{format_name("Bartender")}: Welcome to {self.tavern_display_name}!')
        self.tavern_hub()
    
    def tavern_hub(self):
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
                case 'l':
                    self.player_leaving = True
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
            L. Leave
            ''')
            choice = input()
            if choice.lower() in ['1', '2', '3', '4', 'l']:
                return choice
            else:
                talk('Invalid answer. Try again.', True)
    
    def bartender_menu(self):
        bartender_greeting = random.choice(self.bartender_greetingls)
        bartender_leave = random.choice(self.bartender_leavels)
        self.rootdict_drinks = config.entities['drinks']
        self.rootdict_spec_drinks = config.entities['spec_drinks']

        talk(f'{format_name("Bartender")}: {bartender_greeting}', True, 1.5)
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

            L to leave
            ''')
            choice = input()
            if choice.lower() in ['1', '2', '3', 'spec']:
                self.purchased_drink(choice)
            elif choice.lower() == 'l':
                return
            else:
                talk('Invalid answer. Try again.', True)

    def quest_board_menu(self):
        # Generate quests if not already
        if not self.selected_quests:
            viable_quests = []
            #amount_of_possible_quests = random.randint(1, 4)
            amount_of_possible_quests = 1

            for quest in events.eventsdict.keys():
                if events.eventsdict[quest]['tags']['is_quest']:
                    viable_quests.append(quest)
                    if config.dev_mode:
                        print(f'{colors.DEV}Viable quest discovered: {quest}{colors.END}')
            self.selected_quests = random.sample(viable_quests, k=amount_of_possible_quests)

        choice = player_mc(self.selected_quests, 'Which quest?')

        if choice == 'l':
            return
        else:
            for quest in self.selected_quests:
                if choice == str(self.selected_quests.index(quest)):
                    print('\n')
                    events.eventsdict[quest]['call'](from_quest=True)
        
    def room_menu(self):
        if self.purchased_room:
            talk(f'{format_name("Bartender")}: Mate, you\'ve already bought a room! Too much alcohol for you, surely.')
        else:
            while True:
                print(f'''
                ---~~~### {colors.TITLE}{self.tavern_display_name}{colors.END} ###~~~---

                Coins: {colors.GOLD}{config.coin}{colors.END}

                {format_name("Bartender")}: We\'ve only got a handful of rooms. Just for a measly {str(self.room_price)} coins. Quite reasonable.''')
                choice = input("Purchase a room? (fully healed) (Y/N)\n")
                if choice.lower() == 'y':
                    self.purchased_room = True
                    config.player_health = config.player_max_health
                    player_inventory_change(-self.room_price)
                    talk('You spend the night, and awake refreshed.')
                    break
                elif choice.lower() == 'n':
                    talk(f'{format_name("Bartender")}: Shame, let me know if you change your mind later on.')
                    break
                else:
                    talk('Invalid answer. Try again.', True)
        return
    
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
            talk(f'{format_name("Bartender")}: Hey there, this ain\'t a charity, you got to have enough money for this liquor here.')
            self.bartender_menu()
        
        talk(f'{format_name("Bartender")}: {bartender_buydrink}')

        talk(f'You take your drink, peering into the liquid that swirls around the glass.')
        talk(f'{format_name(config.name)}: Well, bottoms up, I suppose.')
        talk(f'{format_name("Bartender")}: Bottoms up.', True, 1)

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
            talk(f'{format_name("Bartender")}: Yeah, thanks ya\' drunk basta...')
            talk(f'Your eye lids close and the world sleeps... For a moment.')
            self.alley_way()
            self.player_leaving = True
        else:
            try: # Basically, if var drink doesn't have the key 'con_exp' (aka, is a normal drink; not special) then it will pass do to an error
                player_gained_exp('constitution', drink['con_exp'], drink['con_exp'], False)
            except:
                pass
            talk('You bring the glass back down, it thumps to the table.')
            talk(f'{format_name(config.name)}: That\'s good stuff.')
            talk(f'{format_name("Bartender")}: Aye, care for more?')
        return

    def alley_way(self):
        talk('You awaken to find yourself in the back alley of the tavern.')
        talk('Seems that you were so blacked out, the tavern keep dragged you out here with the trash.')
        talk('You get up, wobbling.')
        
        if calculate_chance(0.65, 'constitution'): # 65% chance (unmodified, anyway) chance of throwing up.
            talk('You suddenly lurch forward and involuntary tuck your stomach in.')
            talk('You vomit all over yourself and the ground beneath you.')
        elif calculate_chance(0.15):
            unk = format_name('Unknown')
            gang_member = format_name('Thug')
            player_name = format_name(config.name)
            
            talk(f'{unk}: Hey, you there.')
            talk('You gaze upward, seeing a shadowy figure standing in front of you.')
            talk(f'{unk}: You unlucky enough to wind up out here?')
            talk(f'{player_name}: Yeah, looks as if th--')
            talk('The fellow suddenly punches your gut and pins you to a wall. You realize what your dealing with now.')
            talk(f'{gang_member}: So, so unlucky.')
            talk(f'{gang_member}: Now, now. Just hand over what you got.')
            
            choice = player_mc(['Hand over all your gold', 'Hand over some gold', 'fight'], leave_option=False)
            
            match choice:
                case '0':
                    talk(f'{player_name}: Fine! Here take it all.')
                    talk('The thug\'s rough face smoothens as he witnesses the shiny pieces coming out of your pocket.')
                    if calculate_chance(0.15, 'dexterity'):
                        talk('The thug closes his eyes for moment with a smile, as if he was thinking of all he could do with the gold.')
                        choice = player_mc(['Run off', 'Punch his face and run'], 'You recognize this as an opportunity, should you?', leave_option=False)
                        match choice:
                            case '0':
                                talk('You slowly shuffle away with your front towards him, you slowly turn around. Soon enough you\'re sprinting away.')
                            case '1':
                                talk('You take you hand full of gold and punch the thug\'s face. You stumbles back in surprise and agony.')
                                talk('You quickly rush off and take a corner. You hear his curses as you dash off.')
                    player_inventory_change(coins=(-1 * config.coins))
                    talk('You hand him all that you had, he mockingly thanks you and struts into the unknown shadows of the alley.')
                case '1':
                    choice = player_mc(['5 gold', '15 gold', '30 gold', '50 gold'], 'How much should you hand the thug?', leave_option=False)
                    match choice:
                        case '0':
                            gold_handed_over = -5
                        case '1':
                            gold_handed_over = -15
                        case '2':
                            gold_handed_over = -30
                        case '3':
                            gold_handed_over = -50
                    player_inventory_change(coins=gold_handed_over)
                    talk(f'You hand him the amount. Flinching as he inspects you and the gold you offered.')
                    talk(f'{gang_member}: ...', custom_wait=3)
                    if calculate_chance((0.55 + (gold_handed_over / 100)), 'charisma'):
                        talk(f'{gang_member}: ...')