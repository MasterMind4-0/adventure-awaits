import colors
import config
from systems.tavern import tavern
from utils import talk, format_name, wait

def alley_way(from_tavern: bool = False):
    wait()

def tavern():
    tavern_name = [
        "The Speared Boar", #Reference to "Burn the Witch" music video (Radiohead). In itself is a reference to "Lord of the Flies" :D
        "The Bloody Princess",
        "The Blushing Guitar",
        "The Laughable Hag",
        "The Red Oysters Pub",
        "The Loud Lantern Inn"
    ]
    
    tavern(tavern_name).entering_tavern()
    
eventsls = [
    alley_way,
    tavern
]