import time
import random
import config
import colors

def wait():
    if config.dev_mode:
        pass
    else:
        print('.\n')
        time.sleep(.5)
        print('..\n')
        time.sleep(.5)
        print('...\n')
        time.sleep(.5)

def talk(text: str, custom_wait: bool = False, wait_time: int = 2):
    print(text)
    if not custom_wait:
        num_characters = len(text)
        wait_time = num_characters // 28

    if config.dev_mode:
        time.sleep(0.5)
    else:
        time.sleep(wait_time)

def format_name(name: str):
    return f'{colors.NAME}{name}{colors.END}'

def calculate_chance(chance: float, modifier = None):
    # The chance you give, btw, is the chance of winning
    random_value = random.random()
    if modifier:
        win_chance = chance - (config.player_stats[modifier] / 10)
        config.player_stats[modifier] += random.uniform(0, 0.1)
        if config.dev_mode:
            print(f"{colors.DEV}Modified chance: {win_chance}\nCompared value: {random_value}\nNew {modifier} value: {config.player_stats[modifier]}{colors.END}")
    else:
        win_chance = chance
    if random_value < win_chance:
        return True
    else:
        return False

def format_damage(weapon: dict):
    parts = []

    for die, amount in weapon['damage'].items():
        if not amount:
            continue

        if die.startswith("d"):
            if amount == 1:
                parts.append(die)
            else:
                parts.append(f"{amount}{die}")
        elif die == "add":
            parts.append(str(amount))
    if not parts:
        return "0"
    return " + ".join(parts)

def death(death_by: str = ""):
    if death_by:
        by = f" BY {death_by.upper()}"
    else:
        by = ""
    print(f"---~~~### {colors.HEALTH}{colors.TITLE}YOU DIED{by}{colors.END} ###~~~---")
    exit()

def player_gained(gain_coins: int = 0, gain_items: list = [], print_message: bool = True):
    if gain_coins:
        config.coin += gain_coins
        if print_message:
            talk(f'You gained {colors.GOLD}{gain_coins}{colors.END}!')
    if gain_items:
        config.inventory.append(gain_items)
        if print_message:
            talk(f'You gained {colors.VALUE_ITEM}{gain_items}{colors.END}!')