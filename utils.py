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
        
    time.sleep(wait_time)

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