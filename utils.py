import time
import random
import json
import glob
import os
import config

# Loading .json files
def loading_json_entities():
    for file_path in glob.glob('dicts/**/*.json', recursive=True):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                key = os.path.splitext(os.path.basename(file_path))[0]
                config.entities[key] = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f'There was an error loading {file_path}:', e)

def loading_var(clean: bool = False):
    try:
        if not clean:
            with open("var/default_varable.json", 'r', encoding="utf-8") as f:
                var = json.load(f)
        else:
            with open("var/running_varable.json", 'r', encoding="utf-8") as f:
                var = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f'There was an error loading the running varables:', e)


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

def displayinventory():
    item_counts = {}
    for item in config.inventory:
        if item in item_counts:
            item_counts[item] += 1
        else:
            item_counts[item] = 1

    result = ""
    for item, count in item_counts.items():
        dname = item
        for category, items in config.entities.items():
            if item in items:
                entity = config.entities[category].get(item, {})
                dname = entity.get('display_name', item)
                break
        if count > 1:
            result += f"            {dname} x{count}\n"
        else:
            result += f"            {dname}\n"
    return result.strip()