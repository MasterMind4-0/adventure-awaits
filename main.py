import time
import random
import config
import events
from systems.battle import battle
from utils import talk, wait

config.name = input('What is your character\'s name?\n')
talk(f'{config.name} is quite a good one.')
wait()

ba = battle('thug', True).fight_start()

#random.choice(events.eventsls)()
