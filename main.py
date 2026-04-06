import time
import random
import config
import events
from systems.battle import battle
from systems.tavern import tavern
from utils import talk, wait

config.name = input('What is your character\'s name?\n')
if config.name.lower() != 'dev':
    config.coin = 12
    config.inventory = []
    config.player_armor = config.entities['armors']['no_armor']
    config.player_weapon = config.entities['weapons']['shortsword']
    config.dev_mode = False
talk(f'{config.name} is quite a good one.')
wait()

while True:
    random.choice(events.eventsls)()
