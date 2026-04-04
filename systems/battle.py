import colors
import time
import config
import random
from utils import talk

class battle:
    def __init__(self, preset: str, player_initiative: bool, prevent_item_drops: bool = False, prevent_coin_drop: bool = False):
        preset = preset.lower()

        self.player_initiative = player_initiative
        self.player_victory = False

        self.enemy_display_name = config.entities['enemies'][preset]['display_name']
        self.enemy_health = config.entities['enemies'][preset]['health']
        self.enemy_weapon = config.entities['enemies'][preset]['weapon']
        self.enemy_armor = config.entities['enemies'][preset]['armor']
        self.enemy_base_flee_chance = config.entities['enemies'][preset]['base_flee_chance']
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
            weapon_name = f'{colors.EQUITABLE}{config.player_weapon['display_name']}{colors.END}'
            weapon_damage = config.player_weapon['damage']

            armor_name = f'{colors.EQUITABLE}{config.player_armor['display_name']}{colors.END}'

            print(f'''
                {colors.TITLE}Fighting {self.enemy_display_name}!{colors.END}

            Health: {colors.HEALTH}{config.player_health}{colors.END}

            Equiped Weapon: {weapon_name} [{weapon_damage}]
            Armor: {armor_name}

            1. Attack (1 turn)
            2. Using healing (1 turn)
            3. Skip (1 turn)
            4. Flee
            ''')
            action = input()
            if action in ['1', '2', '3', '4']:
                return action
            talk('Invalid answer. Try again.', True)

    def fight_start(self, custom_entry_phrase: str = "", lethal_fight: bool = True):
        self.lethal_fight = lethal_fight

        entry_phrasels = [
            f"{self.enemy_display_name} looks in your eyes with pure rage.",
            f"{self.enemy_display_name} walks towards you, weapon in hand."
        ]

        if custom_entry_phrase:
            entry_phrase = custom_entry_phrase
        else:
            entry_phrase = random.choice(entry_phrasels)

        talk(entry_phrase)
        self.fight()

    def fight_end(self, player_victor: bool):
        if player_victor:
            print(f'---~~~### {colors.TITLE}YOU WON!{colors.END} ###~~~---')
            if self.gold_drop:
                talk(f'You gained {self.gold_drop} coins')
            talk(f'You looted the body and found {self.calculate_dropped_items()}')

    def flee(self, player_fleeing: bool):
        if player_fleeing:
            subject_fleeing = config.name
        else:
            subject_fleeing = self.enemy_display_name
        
        talk(f'{subject_fleeing} suddenly cowers, and backs away slowly...')
        talk(f'{subject_fleeing}: H-hey now, how about I just---')
        talk(f"Before {subject_fleeing} can even finish their sentence,")

        if self.calculate_flee(player_fleeing):
            talk(f'{subject_fleeing} runs off, leaving nothing, but dust in the air.')
            self.fight_end(True)
        else:
            if player_fleeing:
                talk(f'{self.enemy_display_name} grabs you instantly and throws you to the ground.')
                self.player_initiative = False
                return
            else:
                talk(f'You grab {subject_fleeing} by the throat and throw them to the ground.')
                self.player_initiative = True
                return

    def fight(self):
        if self.player_initiative:
            self.player_initiative = False
            self.player_turn()
        while self.enemy_health > 0 or not self.player_victory:
            if self.player_initiative:
                self.player_initiative = False
                self.player_turn()
                time.sleep(2)
            self.enemy_turn()
            time.sleep(2)
            self.player_turn()
        self.fight_end(True)

    def player_turn(self):
        print('Your turn!')
        action = self.player_menu()
        
        match action:
            case '1':
                self.calculate_hit(True)
            case '2':
                self.healing_menu()
            case '4':
                self.flee(True)

    def enemy_turn(self):
        print('ENEMY TURN')

    def perform_attack(self, player_attacking: bool):
        if self.calculate_hit(player_attacking):
            talk(f'You attack with your {colors.EQUITABLE}{config.player_weapon['display_name']}{colors.END}')

    def calculate_hit(self, player_attacking: bool):
        compared_value = random.random()
        base_hit_chance = .75
        if player_attacking:
            armor = self.enemy_armor
        else:
            armor = config.player_armor['armor']

        hit_chance = base_hit_chance - armor
        if config.dev_mode:
            print(f"{colors.DEV}Hit chance: {hit_chance}\nArmor: {armor}\nBase hit chance: {base_hit_chance}\nCompared value {compared_value}\nHit chance {hit_chance}\nWould hit? {compared_value < hit_chance} < {colors.END}")
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

    def healing_menu(self):
        pass

    def calculate_flee(self, player_fleeing: bool):
        if player_fleeing:
            flee_chance = (config.player_health / 40) + config.player_stats['dexterity']
            compared_value = random.random()
            return compared_value < flee_chance
        else:
            compared_value = random.uniform(0, 1)
            return compared_value < self.enemy_base_flee_chance