import colors
import time
import config
import random
from utils import talk, format_damage, death

class battle:
    def __init__(self, preset: str, player_initiative: bool, prevent_item_drops: bool = False, prevent_coin_drop: bool = False):
        preset = preset.lower()
        enemy_weapon = config.entities['enemies'][preset]['weapon']
        enemy_armor = config.entities['enemies'][preset]['armor']

        self.player_initiative = player_initiative
        self.player_victory = False

        self.enemy_display_name = config.entities['enemies'][preset]['display_name']
        self.enemy_health = config.entities['enemies'][preset]['health']
        self.enemy_weapon = config.entities['weapons'][enemy_weapon]
        self.enemy_armor = config.entities['armors'][enemy_armor]
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

            armor_name = f'{colors.EQUITABLE}{config.player_armor['display_name']}{colors.END}'

            print(f'''
                {colors.TITLE}Fighting {self.enemy_display_name}!{colors.END}

            Health: {colors.HEALTH}{config.player_health}{colors.END}

            Equiped Weapon: {weapon_name} [{format_damage(config.player_weapon)}]
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

    def healing_menu(self):
        pass

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

    def fight_end(self, player_victor: bool, rewards_dropped: bool = True):
        if player_victor:
            dropped_items = self.calculate_dropped_items()
            print(f'---~~~### {colors.TITLE}YOU WON!{colors.END} ###~~~---')
            if self.gold_drop and rewards_dropped:
                talk(f'You gained {self.gold_drop} coins')
            if dropped_items and rewards_dropped:
                talk(f'You looted the body and found {dropped_items}')
        else:
            if self.lethal_fight:
                death(self.enemy_display_name)
            else:
                talk(f'{self.enemy_display_name}: Pff. Not worth my time.')
                talk(f'You lived.')
        return

    def fight(self):
        if self.player_initiative:
            self.player_initiative = False
            self.player_turn()
        while self.enemy_health >= 0 and config.player_health >= 0:
            self.enemy_turn()
            if config.player_health <= 0:
                self.fight_end(False)
                break
            self.player_turn()
            if self.enemy_health <= 0:
                self.fight_end(True)
                break

    def player_turn(self):
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
        if compared_value < self.enemy_base_flee_chance and self.enemy_health <= 5:
            self.flee(False)
        self.perform_attack(False)
        return

    def flee(self, player_fleeing: bool):
        if player_fleeing:
            subject_fleeing = config.name
        else:
            subject_fleeing = self.enemy_display_name
        
        talk(f'{subject_fleeing} suddenly cowers, and backs away slowly...')
        talk(f'{subject_fleeing}: H-hey now, how about I just---')
        talk(f"Before {subject_fleeing} can even finish their sentence,")

        if self.calculate_flee(player_fleeing):
            if player_fleeing:
                config.player_stats['dexterity'] += random.uniform(0.01, 0.05)

            talk(f'{subject_fleeing} runs off, leaving nothing, but dust in the air.\n')
            self.fight_end(True, False)
        else:
            if player_fleeing:
                talk(f'{self.enemy_display_name} grabs you instantly and throws you to the ground.\n')
                return
            else:
                talk(f'You grab {subject_fleeing} by the throat and throw them to the ground.\n')
                self.player_turn()
                return

    def perform_attack(self, player_attacking: bool):
        if player_attacking:
            talk(f'You attack with your {colors.EQUITABLE}{config.player_weapon['display_name']}{colors.END}')
        else:
            talk(f'{self.enemy_display_name} swings their weapon at you.', True, 1)
        if self.calculate_hit(player_attacking):
            if player_attacking:
                config.player_stats['strength'] += random.uniform(0.0001, 0.001)
                self.enemy_health -= self.calculate_damage(True)

                talk(f'You clobber {self.enemy_display_name}.', True, 1)
                if config.dev_mode:
                    print(f'{colors.DEV}Enemy health: {self.enemy_health}{colors.END}')
            else:
                config.player_health -= self.calculate_damage(False)
                talk(f'{self.enemy_display_name}\'s weapon thuds into you.', True, 1)
        else:
            if player_attacking:
                talk(f'...But you miss!', True, 1)
            else:
                talk(f'...But {self.enemy_display_name} missed!', True, 1)
        return

    def calculate_damage(self, player_attacking: bool):
        damage = 0
        if player_attacking:
            rootdict = config.player_weapon['damage']
        else:
            rootdict = self.enemy_weapon['damage']

        for key, amount in rootdict.items():
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
        if player_attacking:
            armor = self.enemy_armor['armor']
            piercing = config.player_weapon['damage']['piercing']
        else:
            armor = config.player_armor['armor'] + config.player_stats['dexterity']
            piercing = self.enemy_weapon['damage']['piercing']
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
            flee_chance = (self.enemy_health / 40) - config.player_stats['dexterity']
        if config.dev_mode:
            print(f'{colors.DEV}Flee chance: {flee_chance}\nCompared value: {compared_value}{colors.END}')
        return compared_value < flee_chance