import glob
import os
import json

# Dictionary for all items
entities = {}
for file_path in glob.glob('dicts/**/*.json', recursive=True):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            key = os.path.splitext(os.path.basename(file_path))[0]
            entities[key] = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'There was an error loading {file_path}:', e)

# Player
player_stats = {
    "strength": 0.0,
    "constitution": 0.0,
    "dexterity": 0.0,
    "charisma": 0.0,
    "intelligence": 0.0,
}
name = 'dev'
dev_mode = True
coin = 100
player_health = 20
inventory = [
    "greatest_health_potion",
    "greatest_health_potion"
]
player_weapon = entities['weapons']['longsword']
player_armor = entities['armors']['plate_armor']