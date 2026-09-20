import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_inventory_change, player_mc

tags = {
    'is_quest': True
}

places = [
    "market",
    "tavern",
    "town_square",
    "well",
    "shrine"
]
descriptors = {
    "hair": ['black', 'brown', 'blonde'],
    "eyes": ['brown', 'blue', 'green', 'hazel'],
    "shirt_color": ['brown', 'blue', 'green', 'black'],
    "age": ['child', 'adolescent', 'adult', 'elder']
}

def make_person():
    person = {
        "hair": random.choice(descriptors['hair']),
        "eyes": random.choice(descriptors['eyes']),
        "shirt_color": random.choice(descriptors['shirt_color']),
        "age": random.choice(descriptors['age'])
    }
    while person == lost_girl:
        person = {
            "hair": random.choice(descriptors['hair']),
            "eyes": random.choice(descriptors['eyes']),
            "shirt_color": random.choice(descriptors['shirt_color']),
            "age": random.choice(descriptors['age'])
        }
    return person

def child_game_prep():
    global lost_girl, game_map, beginning_details, last_location
    game_length = random.randint(2, 5)

    # Correct lost girl
    age = random.choice(descriptors['age'])
    while age == 'elder':
        age = random.choice(descriptors['age'])
    
    lost_girl = {
        "hair": random.choice(descriptors['hair']),
        "eyes": random.choice(descriptors['eyes']),
        "shirt_color": random.choice(descriptors['shirt_color']),
        "age": age
    }

    # Map
    game_map = {}
    possible_places = random.sample(places, game_length)
    for place in possible_places:
        game_map[place] = []
        for i in range(random.randint(1, 4)):
            game_map[place].append(make_person())
    # One place gets correct lost girl
    game_map[random.choice(possible_places)].append(lost_girl)

    # Defines beginning details of lost girl
    beginning_details = {}
    for detail in lost_girl.keys():
        if calculate_chance(.50):
            beginning_details[detail] = lost_girl[detail]

    # Start location
    last_location = next(iter(game_map))

    if config.dev_mode:
        print(f'lost girl description:\n{colors.DEV}{lost_girl}{colors.END}')
        print(f'Game map:\n{colors.DEV}{game_map}{colors.END}')
        print(f'Beginning details:\n{colors.DEV}{beginning_details}{colors.END}')
        print(f'starting location:\n{colors.DEV}{last_location}{colors.END}')

def child_game():
    global win
    player = format_name(config.name)
    person_name = format_name('Person')

    win = False

    wait()
    for place in game_map.keys():
        talk(f'You walk towards the {place.replace('_', ' ').capitalize()}.')
        wait()
        for num_id, person in enumerate(game_map[place]):
            talk(f"You see a person (person number {num_id + 1}) with {colors.VALUE_ITEM}{person['hair']} hair{colors.END} and {colors.VALUE_ITEM}{person['eyes']} colored eyes{colors.END}.")
            if person['age'] == 'child':
                talk(f"They look to be a {colors.VALUE_ITEM}{person['age']}{colors.END} with a {colors.VALUE_ITEM}{person['shirt_color']} colored shirt{colors.END}.")
            else:
                talk(f"They look to be an {colors.VALUE_ITEM}{person['age']}{colors.END} with a {colors.VALUE_ITEM}{person['shirt_color']} colored shirt{colors.END}.")
            print()

        choice = input('Is it anyone? (Y/N)\n')
        if choice.lower() == 'y':
            choice = int(input("Who could it be?\n")) - 1

            talk(f'{player}: Are you lost?')
            if game_map[place][choice] == lost_girl:
                win = True
                talk(f'{person_name}: Yes!')
                break
            else:
                talk(f'{person_name}: Sorry?')
                talk(f'{player}: My apologies...')
                talk('You walk off embarrassed.')

def kidnap():
    player = format_name(config.name)
    girl = format_name('Lost Girl')
    kidnapper = format_name('Stranger')
    reward_gold = random.randint(5, 30)

    talk(f'{kidnapper}: No, she\'s not, sorry. She\'s a little weird.')
    match player_mc(['No, she is!', 'And who are you?', 'Oh, I\'m sorry'], leave_option=False):
        case '0':
            talk(f'{kidnapper}: You couldn\'t just walk away.')
            battle('thug').fight_start("The kidnapper takes out their weapon, the people in the area scatter.")
        case '1':
            talk(f'{kidnapper}: Why, her parent, of course!')
            match player_mc(['I don\'t think so...', 'My apologises.'], leave_option=False):
                case '0':
                    talk(f'{kidnapper}: You couldn\'t just walk away.')
                    battle('thug').fight_start("The kidnapper takes out their weapon, the people in the area scatter.")
                case '1':
                    talk('They chuckle,')
                    talk(f'{kidnapper}: No problem, really. Have a good day.')
                    talk('You walk off, confident you were correct in your judgement.')
                    wait()
                    talk(f'You return and tell the woman you couldn\'t find her daughter.')
                    talk(f'She wells up with tears. You walk away in shame, trying to forget the mess.')
                    return
        case '2':
            talk('They chuckle,')
            talk(f'{kidnapper}: No problem, really. Have a good day.')
            talk('You walk off, confident you were correct in your judgement.')
            wait()
            talk(f'You return and tell the woman you couldn\'t find her daughter.')
            talk(f'She wells up with tears. You walk away in shame, trying to forget the mess.')
            return


    talk(f'{girl}: Oh thank you, thank you!')
    talk(f'{player}: Let\'s get you to your mom.')
    wait()
    talk('The woman nearly jumps with excitement as you walk her daughter back.')
    talk(f'She gives you a peck on the cheek and sends you off with {reward_gold} gold.')
    player_inventory_change(reward_gold)

def ran_away():
    woman = format_name('Woman')
    player = format_name(config.name)
    girl = format_name('Lost Girl')
    reward_gold = random.randint(5, 30)

    talk(f'{girl}: But, please, listen to me! I can\'t go back home.')
    talk(f'{girl}: I don\'t want to live under my mother\'s rules anymore. I want to run away.')
    talk(f'{player}: Why would you do that?')
    talk(f'{girl}: She never lets me choose anything. I just want a life of my own.')

    match player_mc(['Force her back', 'Let her run away'], 'What do you do?', leave_option=False):
        case '0':
            talk(f'{player}: Sorry, but I came to get you to your mother. Not to let you run away.')
            if calculate_chance(0.35, 'charisma', False):
                talk(f'{girl}: ...Fine. I\'ll go back.')
                talk('The girl keeps her head down the entire walk back, but she does return with you.')
                wait()
                talk(f'{woman}: Thank you for bringing her home! Here, I hope this token of grattitude carries you far.')
                player_inventory_change(reward_gold)
            else:
                talk(f'{girl}: No! I won\'t go back!')
                talk('She runs off. You chase her through a crowd, but the people sufficate you and you lose sight of the girl.')
                talk('You return empty-handed. You can\'t even muster the courage to go back to her mother and so you leave without another word.')
        case '1':
            talk(f'{player}: You aren\'t lying, are you?')
            talk(f'{girl}: No! I swear!')
            talk(f'You breathe a heavy sigh.')
            talk(f'{player}: Fine.')
            talk('The girl smiles up at you,')
            talk(f'{girl}: Thank you! Thanks a million!')
            talk(f'{woman}: My daughter... no!')
            talk('The woman cries into her hands, and you can do nothing but watch the girl leave.')
        case _:
            talk('You hesitate for a moment, and the girl slips away before you can decide.')
            talk(f'{girl}: I am leaving. I won\'t go back.')
            wait()
            talk('You tell the woman what happened.')
            talk('You leave heavy heartedly as she sobbs.')

def scam():
    player = format_name(config.name)
    girl = format_name('Lost Girl')

    talk('The girl suddenly darts away from you and disappears down a narrow alley between the buildings.')
    talk(f'{player}: Hey! Wait!')
    talk('You follow after her, but as soon as you turn the corner, a rough-looking man steps from the shadows.')
    talk(f'{girl}: Oh! You found me!')
    battle('thug').fight_start('The man gives a deep, cruel laugh and draws a blade.')

    talk('You beat the man back into the alley wall and he collapses, gasping for air.')
    talk('However, the girl has disappeared. The alley is left empty except for a few broken lanterns and a trail of muddy footprints.')
    talk('The girl is gone, and when you hurry back to the woman you find her, too, gone.')

def lost_child(from_quest = False):
    woman = format_name('Woman')
    player = format_name(config.name)

    if from_quest:
        talk('You step onto a nice house\'s porch, before raising the metal knocker.')
        talk('A woman walks answers the door, her limbs kept close to her body and tear-stained cloth in her hands.')
        talk(f'{woman}: Are y-you here in r-regard to my daughter?')
        talk(f'{player}: Yes, I saw a poster at the tavern.')
        talk(f'{woman}: Yes. She has been gone for two days now.')
        talk('She sniffles.')
    else:
        talk('You are passing through a town for a quick rest before venturing once again.')
        talk('As you exit the joyful tavern with the crowd laughing to your last drunk joke, a woman besides the tavern door grabs you\'re arm.')
        talk(f'{woman}: Please! I don\'t know where my daughter wandered off to! S-she must of... I don\'t know...')
        match player_mc(['Calm the woman down', 'Wait for her to continue', 'Push the woman away', ], leave_option=False):
            case '0':
                talk('You place your arm on the woman\'s back.')
                talk('She sniffles in your shoulder as you embrace her.')
                talk('She calms down enough to continue.')
            case '1':
                talk('You let her cry in your arm as you wait for her to calm down.')
                talk('She calms down.')
                talk(f'{woman}: Sorry if I brought shame to you.')
                match player_mc(['"You did no such thing."', '"It\'s fine."', '"I hope you are."'], leave_option=False):
                    case '0':
                        talk('She gives a brief subtle smile, she then continues.')
                    case '1':
                        talk("She continues.")
                    case '2':
                        talk('She looks down to your feet.')
                        talk(f'{player}: Well, out with it.')
                        talk('She reluctantly continues.')
            case '2':
                talk('You shove the woman off you.')
                if calculate_chance(0.05, 'strength', False):
                    pass # Chance of her pulling you down with her.
                else:
                    talk(f'You stared at her disheveled self before walking away with your chin up high.')
                    return

    child_game_prep()
    talk(f'{woman}: Can you find her? She was last at the {last_location.replace('_', ' ').capitalize()}.')
    for category, detail in beginning_details.items():
        if category == 'hair':
            talk(f'{woman}: She has {colors.VALUE_ITEM}{detail}{colors.END} hair.')
        elif category == 'eyes':
            talk(f'{woman}: She has bright {colors.VALUE_ITEM}{detail}{colors.END} eyes.')
        elif category == 'shirt_color':
            talk(f'{woman}: Her shirt was {colors.VALUE_ITEM}{detail}{colors.END}.')
        elif category == 'age':
            if detail == 'child':
                talk(f'Most importantly, she\'s a {colors.VALUE_ITEM}{detail}{colors.END}.')
            else:
                talk(f'Most importantly, she\'s an {colors.VALUE_ITEM}{detail}{colors.END}.')
    talk('She gives the last of the details, her voice breaking near the end. She breaks down into tears and closes the door.')
    talk(f'{woman}: Please find her.')
    talk('She says in a muffled voice through the door.')

    child_game()

    if win:
        match random.randint(1, 3):
                case 1:
                    kidnap()
                case 2:
                    ran_away()
                case 3:
                    scam()
    else:
        talk('You go to the last place she could have been and don\'t find her.')
        if from_quest:
            talk(f'You walk towards the house of the lady.')
        else:
            talk(f'You walk towards the tavern where you saw the woman.')
        talk(f'{player}: I\'m sorry, but I couldn\'t find her.')
        talk(f'The woman wells up with tears.')
        talk(f'You walk away in shame, trying to forget the mess.')