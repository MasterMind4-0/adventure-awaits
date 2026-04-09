import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_gained

def visting_tavern():
    tavern_name = [
        "The Speared Boar", #Reference to "Burn the Witch" music video (Radiohead). In itself is a reference to "Lord of the Flies" :D
        "The Bloody Princess",
        "The Blushing Guitar",
        "The Laughable Hag",
        "The Red Oysters Pub",
        "The Loud Lantern Inn"
    ]
    
    tavern(tavern_name).entering_tavern()

def skeleton_attack():
    talk('You come across a dead body, its skeleton showing through the rotton flesh.')
    choice = input('Should you loot the body, walk away, or bury the body? (1, 2, or 3)\n')
    if choice == '1':
        player_gained(random.randint(6, 14))
        if calculate_chance(.6):
            talk('After you loot the body, it suddenly animates as you come near.')
            talk('It screeches and lunges at you.')
            battle('Skeleton', False).fight()
            talk('You wipe the sweat off your brow.')
            talk('You also loot the body and find a couple coins.')
        else:
            talk('You loot the body of its past life\'s belongings.')
    elif choice == '2':
        talk('You decided to leave, best to leave the dead to the body collectors.')
    elif choice == '3':
        if calculate_chance(.4):
            talk('The body animates as you come near,')
            talk('It screeches and lunges at you.')
            battle('skeleton', False).fight()
            talk('Once you kill the undead. You bury the body.')
            talk('You wipe the sweat off your brow as you leave.')
        else:
            talk('You bury the body, say your prayers, and leave.')
    return
    
eventsls = [
    visting_tavern,
    skeleton_attack
]