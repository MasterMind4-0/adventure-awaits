import colors
import time
import config
import random
from utils import talk, format_damage, death, player_gained_exp, display_inventory, player_inventory_change

class battle:
    def __init__(self, preset: str, player_initiative: bool = False, prevent_item_drops: bool = False, prevent_coin_drop: bool = False):
        preset = preset.lower()
        enemy_weapon = config.entities['enemies'][preset]['weapon']
        enemy_armor = config.entities['enemies'][preset]['armor']

        self.player_initiative = player_initiative
        self.player_victory = False
        self.exit_loop = False

        self.enemy = config.entities['enemies'][preset]

        if not prevent_item_drops:
            self.possible_drops = config.entities['enemies'][preset]['drops']     
        else:
            self.possible_drops = {}
        
        if not prevent_coin_drop:
            self.gold_drop = config.entities['enemies'][preset]['health'] * .4
        else:
            self.gold_drop = 0

    def player_menu(self):
        while True:
            weapon_name = f'{colors.EQUITABLE}{config.player_weapon["display_name"]}{colors.END}'

            armor_name = f'{colors.EQUITABLE}{config.player_armor["display_name"]}{colors.END}'

            print(f'''
                {colors.TITLE}Fighting {self.enemy["display_name"]}!{colors.END}

            Health: {colors.HEALTH}{config.player_health}{colors.END}

            Equiped Weapon: {weapon_name} [{format_damage(config.player_weapon)}]
            Armor: {armor_name}

            1. Attack (1 turn)
            2. Using potion (1 turn)
            3. Skip (1 turn)
            4. Flee
            ''')
            action = input()
            if action in ['1', '2', '3', '4']:
                return action
            talk('Invalid answer. Try again.', True)
    
    def healing_menu(self):
        health_potions = [item for item in config.inventory if 'health_potion' in item]
        
        if not health_potions:
            talk('You have no health potions!', True)
            return
        
        print(f'\n{colors.TITLE}Your Health Potions:{colors.END}')
        for i, potion in enumerate(health_potions, 1):
            display_name = config.entities["potions"][potion]["display_name"]
            min_heal = config.entities["potions"][potion]["min"]
            max_heal = config.entities["potions"][potion]["max"]

            print(f'{i}. {display_name}')
        
        print(f'{len(health_potions) + 1}. Cancel\n')
        choice = input('Which health potion: ').strip()

        if not choice.isdigit():
            talk('Invalid choice.', True)
            return
        choice_idx = int(choice)

        if choice_idx == len(health_potions) + 1:
            talk('You decided not to use a potion.', True)
            return
        if choice_idx < 1 or choice_idx > len(health_potions):
            talk('Invalid choice.', True)
            return
        
        selected_potion = health_potions[choice_idx - 1]
        potion_data = config.entities['potions'][selected_potion]
        heal_amount = random.randint(potion_data['min'], potion_data['max'])
        old_health = config.player_health
        config.player_health += heal_amount

        talk(f'You used {potion_data["display_name"]} and recovered {heal_amount} health! ({old_health} → {config.player_health})', True)

        config.inventory.remove(selected_potion)
        return

    def fight_start(self, custom_entry_phrase: str = "", lethal_fight: bool = True):
        self.lethal_fight = lethal_fight

        entry_phrasels = [
            f'{self.enemy["display_name"]} looks in your eyes with pure rage.',
            f'{self.enemy["display_name"]} walks towards you, ready for battle.'
        ]

        if custom_entry_phrase:
            entry_phrase = custom_entry_phrase
        else:
            entry_phrase = random.choice(entry_phrasels)

        talk(entry_phrase)
        self.fight()

    def fight_end(self, player_victor: bool, rewards_dropped: bool = True):
        title_text = "YOU WON!"

        if player_victor:
            dropped_items = self.calculate_dropped_items()
            if self.exit_loop:
                title_text = "ESCAPED!"
            print(f'---~~~### {colors.TITLE}{title_text}{colors.END} ###~~~---')
            if self.gold_drop and rewards_dropped:
                player_inventory_change(self.gold_drop)
            if dropped_items and rewards_dropped:
                player_inventory_change(items=rewards_dropped, print_message=False)
                talk(f'You looted the body and found {colors.VALUE_ITEM}{dropped_items}{colors.END}')
        else:
            if self.lethal_fight:
                death(self.enemy['display_name'])
            else:
                talk(f'{self.enemy["display_name"]} then stops, dusting their shoulders.')
        print('---~~~################~~~---\n\n')
        return

    def fight(self):
        if self.player_initiative:
            self.player_initiative = False
            self.player_turn()
        while self.enemy['health'] > 0 and config.player_health > 0:
            self.enemy_turn()

            if config.player_health <= 0:
                self.fight_end(False)
                break
            elif self.enemy['health'] <= 0:
                self.fight_end(True)
                break
            elif self.exit_loop:
                self.fight_end(True, False)
                break

            self.player_turn()

            if config.player_health <= 0:
                self.fight_end(False)
                break
            elif self.enemy['health'] <= 0:
                self.fight_end(True)
                break
            elif self.exit_loop:
                self.fight_end(True, False)
                break

    def player_turn(self):
        if config.player_health > config.player_max_health:
            config.player_health = config.player_max_health
        talk('\nYour turn!\n', True, 1)
        action = self.player_menu()
        
        match action:
            case '1':
                self.perform_attack(True)
            case '2':
                self.healing_menu()
            case '4':
                self.flee(True)
        return

    def enemy_turn(self):
        talk('\nEnemy\'s turn!\n', True, 1)
        compared_value = random.random()
        if self.enemy['health'] > 0:
            self.perform_attack(False)
        if compared_value < self.enemy['base_flee_chance'] and self.enemy['health'] <= 5:
            self.flee(False)
        return

    def flee(self, player_fleeing: bool):
        if player_fleeing:
            subject_fleeing = config.name
        else:
            subject_fleeing = self.enemy['display_name']
        
        talk(f'{subject_fleeing} suddenly cowers, and backs away slowly...')
        if "NoLanguage" in self.enemy["tags"]:
            talk(f'{subject_fleeing} backs away, frightened.')
            talk(f"Before {subject_fleeing} can even get a foot further,")
        else:
            talk(f'{subject_fleeing}: H-hey now, how about I just---')
            talk(f"Before {subject_fleeing} can even finish their sentence,")

        if self.calculate_flee(player_fleeing):
            self.exit_loop = True
            if player_fleeing:
                player_gained_exp('dexterity', 0.01, 0.05, False)

            talk(f'{subject_fleeing} runs off, leaving nothing, but dust in the air.\n')
        else:
            if player_fleeing:
                talk(f'{self.enemy["display_name"]} grabs you instantly and throws you to the ground.\n')
            else:
                talk(f'You grab {subject_fleeing} by the throat and throw them to the ground.\n')
        return

    def perform_attack(self, player_attacking: bool):
        if player_attacking:
            talk(f'You attack with your {colors.EQUITABLE}{config.player_weapon["display_name"]}{colors.END}')
        else:
            if "Handless" in self.enemy["tags"]:
                talk(f'{self.enemy["display_name"]} attacks you.')
            else:
                talk(f'{self.enemy["display_name"]} swings their weapon at you.', True, 1)
        if self.calculate_hit(player_attacking):
            if player_attacking:
                player_gained_exp('strength', 0.0001, 0.001, False)
                self.enemy['health'] -= self.calculate_damage(player_attacking)
                talk(f'You clobber {self.enemy["display_name"]}.', True, 1)
                
                if config.dev_mode:
                    print(f'{colors.DEV}Enemy health: {self.enemy["health"]}{colors.END}')
            else:
                config.player_health -= self.calculate_damage(player_attacking)
                if "Handless" in self.enemy["tags"]:
                    talk(f'{self.enemy["display_name"]} hits you.')
                else:
                    talk(f'{self.enemy["display_name"]}\'s weapon thuds into you.', True, 1)
        else:
            if player_attacking:
                talk(f'...But you miss!', True, 1)
            else:
                talk(f'...But {self.enemy["display_name"]} missed!', True, 1)
        return

    def calculate_damage(self, player_attacking: bool):
        damage = 0
        if player_attacking:
            weaponrootdict = config.player_weapon['damage']
        else:
            weaponrootdict = config.entities['weapons'][self.enemy['weapon']]['damage']

        for key, amount in weaponrootdict.items():
            if not amount:
                continue
            if key == "add":
                damage += amount

            elif key.startswith("d"):
                sides = int(key[1:])
                for _ in range(amount):
                    roll_result = random.randint(1, sides)
                    if config.dev_mode:
                        print(f'{colors.DEV}Roll result: {roll_result}{colors.END}')
                    damage += roll_result
        return damage

    def calculate_hit(self, player_attacking: bool):
        compared_value = random.random()
        base_hit_chance = 0.65
        weaponrootdict = config.entities['weapons'][self.enemy['weapon']]

        if player_attacking:
            armor = config.entities['armors'][self.enemy['armor']]['armor']
            piercing = config.player_weapon['damage']['piercing']
        else:
            armor = config.player_armor['armor'] + config.player_stats['dexterity']
            piercing = weaponrootdict['damage']['piercing']
        effective_armor = armor * (1 - piercing)

        hit_chance = base_hit_chance * (1 - effective_armor)
        hit_chance = max(0.05, min(0.95, hit_chance))
        if config.dev_mode:
            print(f"{colors.DEV}Hit chance: {hit_chance}\nArmor: {armor}\nBase hit chance: {base_hit_chance}\nCompared value {compared_value}\nHit chance {hit_chance}\nWould hit? {compared_value < hit_chance}{colors.END}")
        return compared_value < hit_chance

    def calculate_dropped_items(self):
        drops = []
        for drop in self.possible_drops.keys():
            compared_value = random.random()
            item_chance_dropping = self.possible_drops[drop]

            if compared_value < item_chance_dropping:
                drops.append(drop)

        # Cleaning list to human format (e.i, `[ "dagger", "leather_armor" ]` -> `dagger, leather armor`)
        if drops:
            formatted_drops = [drop.replace('_', ' ') for drop in drops]
            return ', '.join(formatted_drops)
        else:
            return ''                

    def calculate_flee(self, player_fleeing: bool):
        compared_value = random.random()  
        if player_fleeing:
            flee_chance = (config.player_health / 40) + config.player_stats['dexterity']
        else:
            flee_chance = (self.enemy['health'] / 40) - config.player_stats['dexterity']
        if config.dev_mode:
            print(f'{colors.DEV}Flee chance: {flee_chance}\nCompared value: {compared_value}{colors.END}')
        return compared_value < flee_chance