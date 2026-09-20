import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_inventory_change

tags = {
    'is_quest': False,
    'natural': True
}

def visiting_tavern():   
    tavern().entering_tavern()