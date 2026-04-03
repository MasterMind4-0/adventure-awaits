import time
import random
import config
from utils import talk, wait, loading_json_entities

loading_json_entities()

config.name = input('What is your character\'s name?\n')
talk(f'{config.name} is quite a good one.')
wait()

random.choice(events.eventls)()
