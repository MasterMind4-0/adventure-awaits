import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_var_change

tags = {
    'is_quest': False
}

def visiting_tavern():
    tavern_name = [
        "The Speared Boar", #Reference to "Burn the Witch" music video (Radiohead). In itself is a reference to "Lord of the Flies" :D
        "The Bloody Princess",
        "The Blushing Guitar",
        "The Laughable Hag",
        "The Red Oysters Pub",
        "The Loud Lantern Inn"
    ]
    
    tavern(tavern_name).entering_tavern()