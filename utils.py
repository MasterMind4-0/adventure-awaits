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

def player_mc(choices: list, text: str = 'What should you do?', leave_option_text: str = 'Leave', leave_option: bool = True):
    # mc = multiple choice

    print()
    for choice in choices:
        print(f'{choices.index(choice) + 1}. {choice}')
    if leave_option:
        print(f'L. {leave_option_text}')
    print()
    
    player_selected_choice = input(f'{text}\n').strip().lower()

    try:
        return str(int(player_selected_choice) - 1)
    except ValueError:
        return player_selected_choice

def format_name(name: str):
    return f'{colors.NAME}{name}{colors.END}'

def calculate_chance(chance: float, modifier = None, give_exp: bool = True):
    # The chance you give, btw, is the chance of returning True
    dev_output = ""
    random_value = random.random()

    if modifier:
        win_chance = chance - (config.player_stats[modifier] / 10)
        if give_exp:
            config.player_stats[modifier] += random.uniform(0, 0.1)
            if config.dev_mode:
                dev_output = f"New {modifier} value: {config.player_stats[modifier]}"
    else:
        win_chance = chance
    if config.dev_mode:
        dev_output = f"{dev_output}\nModified chance: {win_chance}\nCompared value: {random_value}"
    print(f"{colors.DEV}{dev_output}{colors.END}")
    
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

def player_var_change(coins: int = 0, items = None, print_message: bool = True):
    coins = round(coins)

    if coins:
        if coins < 0:
            config.coin += coins
            if print_message:
                talk(f'You {colors.TITLE}lost{colors.END} {colors.GOLD}{coins}{colors.END} coins!')
        else:
            config.coin += coins
            if print_message:
                talk(f'You {colors.TITLE}gained{colors.END} {colors.GOLD}{coins}{colors.END} coins!')
    if items:
        config.inventory.append(items)
        if print_message:
            talk(f'You {colors.TITLE}gained{colors.END} {colors.VALUE_ITEM}{items}{colors.END}!')

def player_gained_exp(exp_type: str, exp_amount_min: int | float, exp_amount_max: int | float, print_message: bool):
    exp_var = config.player_stats[exp_type] 
    if isinstance(exp_amount_min, float) and isinstance(exp_amount_max, float):
        gained_exp = random.uniform(exp_amount_min, exp_amount_max)
    else:
        gained_exp = random.randint(exp_amount_min, exp_amount_max)
    
    exp_var += gained_exp
    if print_message:
        talk(f'You gained {gained_exp} in {exp_type}!')

def display_inventory(chosen_category: str = ""):
    # Getting amount of items in inventory as int
    item_counts = {}
    for item in config.inventory:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1
    
    result = ""
    for item, count in item_counts.items():
        for category, items in config.entities.items():
            if chosen_category:
                if chosen_category.lower() == category:
                    if item in items:
                        display_name = items[item]['display_name']
                        break
            else:
                if item in items:
                    display_name = items[item]['display_name']
                    break
        if count > 1:
            result += f'{display_name} x{count}\n'
        else:
            result += f'{display_name}\n'
    return result