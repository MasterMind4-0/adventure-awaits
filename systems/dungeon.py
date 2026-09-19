import time
import random
from utils import talk, wait

room_types = config.entities['room_types']

# Generating functions, aka, the functions that make the dungeon.

def generate_dungeon_map(dungeon_map: list):
    full_dungeon = []
    
    for room_data in dungeon_map:
        room_dict = generate_room(room_data[0], room_data[1])
        full_dungeon.append(room_dict)
        
    return full_dungeon

def generate_room(room_type, required_amount_enemies: int):
    new_room = {
        "room_type": None,
        "reward_gold": 0,
        "reward_item": [],
        "enemies": []
    }
    
    # Getting room types
    if room_type in room_types:
        new_room["room_type"] = random.choice(list(room_types[room_type].keys()))
        
    # Getting enemy types
    viable_enemy_types = room_types[room_type][new_room["room_type"]]["enemies_class"]
    
    new_room["enemies"] = random.choices(viable_enemy_types, k=required_amount_enemies)
            
    return new_room

# "Playing" functions, aka, the functions that actually allow playing in the dungeons.

def start_dungeon(map: list):
    talk('You enter the dungeon...')
    wait()
    in_dungeon(map)
    
def end_dungeon(map: list):
    pass

def in_dungeon(map: list):
    for current_room_id in range(len(map)):
        current_room = map[current_room_id]
        talk(f'You enter the room, there are {len(current_room["enemies"])} waiting for you.')