import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_inventory_change, player_mc

tags = {
    'is_quest': True
}

possible_creature = [
    "bear",
    "fox"
]

def farmer_problem():
    creature = random.choice(possible_creature)
    Farmer = format_name('Farmer')
    player_name = format_name(config.name)

    talk('A farmer comes, begging for your help,')
    talk(f"{Farmer}: Please! Every night something eats my crops! You look like a charming, capable person; I beg, everyone has rejected, but can you help me?")
    choice = player_mc(['Yes', "No"], 'Should you help the man?', leave_option=False)
    if choice == '0':
        talk(f"{player_name}: Well, I don't see why not.")
        talk('The man graciously thanks you.')
        talk(f"{Farmer}: Every night my berries always seem to be gone! Do you think you can stay overnight and discover what beast eats my berries?")
        talk('You accept and, at night, after waiting for hours, you finally spot the thief.')
        talk(f'A {creature.capitalize()}.')
        if calculate_chance(0.2) and creature == 'bear':
            talk(f'As you see the {creature.capitalize()}, you feel a sense of fear.')
            talk(f'The {creature.capitalize()} stands on its hind legs, you fall backwards in fear.')
            talk(f'You dash before the {creature.capitalize()} does anything else.')
            return
        choice = player_mc([f'Fight the {creature.capitalize()}', f'Tame the {creature.capitalize()}'], leave_option_text='Leave it alone', leave_option=True)
        if choice == '0':
            talk(f'You charge the {creature.capitalize()}, frightening it.')
            battle(creature, True, prevent_coin_drop=True).fight_start()
            talk('You finish the job and head to the local inn.')
            talk('In the morn\', you visit the farmer to tell him the news.')
            talk('He\'s overjoyed and hands you a pouch of gold.')
            player_inventory_change(coins=random.randint(5, 12))
        elif choice == '1':
            talk(f'{player_name}: Woah! Easy there.')
            talk(f'The {creature.capitalize()} seems to stare at you,')
            talk('You reach out your hand.')
            if calculate_chance(0.3, 'intelligence'):
                talk(f'The {creature.capitalize()} cautiously walks towards you.')
                talk('It nozzles its nose against your hand.')
                talk(f'In the morning, you show the farmer how to take care of the {creature.capitalize()}.')
                talk('You even train it to pick the berries for the farmer.')
                talk('As the farmer gives you your award, you leave to continue your travels.')
                player_inventory_change(coins=random.randint(5, 12))
            else:
                talk(f'As you reach out, however, the {creature.capitalize()} turns aggresive and lashes out at you.')
                battle(creature, prevent_coin_drop=True).fight_start()
                talk("In the morning, the farmer is overjoyed to hear you've gotten rid of the pest problem.")
                talk('He gives you his gold and thanks you for your work.')
                player_inventory_change(coins=random.randint(5, 12))
        else:
            talk(f'You look at the {creature.capitalize()}, and decide on leaving it be.')
            talk('You slip away under the cover of the night.')
    else:
        talk(f'{player_name}: Sorry, but I have too much to do, deal with it yourself.')

    return