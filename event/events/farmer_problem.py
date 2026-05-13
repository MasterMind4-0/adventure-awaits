import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from utils import talk, format_name, wait, calculate_chance, player_var_change

tags = {
    'is_quest': True
}

def farmer_problem():
    Farmer = format_name('Farmer')
    player_name = format_name(config.name)

    talk('A farmer comes, begging for your help,')
    talk(f"{Farmer}: Please! Every night something eats my crops! You look like a charming, capable person; I beg, everyone has rejected, but can you help me?")
    choice = input('Should you help the man? (Y/N)\n')
    if choice == 'y':
        talk(f"{player_name}: Well, I don't see why not.")
        talk('The man graciously thanks you.')
        talk(f"{Farmer}: Every night my berries always seem to be gone! Do you think you can stay overnight and discover what beast eats my berries?")
        talk('You accept and, at night, after waiting for hours, you finally spot the thief.')
        talk('A bear. And a large one at that.')
        if calculate_chance(0.2):
            talk('As you see the bear, you feel a sense of fear.')
            talk('The bear stands on its hind legs, you fall backwards in fear.')
            talk('You dash before the bear does anything else.')
            return
        choice = input('Should you fight the bear, try to tame the bear, or should you leave it be? (1, 2, or 3)\n')
        if choice == '1':
            talk('You charge the bear, frightening it.')
            battle('bear', prevent_coin_drop=True).fight_start()
        elif choice == '2':
            talk(f'{player_name}: Woah! Easy there.')
            talk('The bear seems to stare at you,')
            talk('You reach out your hand.')
            if calculate_chance(0.3, 'intelligence'):
                talk('The bear cautiously walks towards you.')
                talk('It nozzles its nose against your hand.')
                talk('In the morning, you show the farmer how to take care of the bear.')
                talk('You even train it to pick the berries for the farmer.')
                talk('As the farmer gives you your award, you leave to continue your travels.')
            else:
                talk('As you reach out, however, the bear turns aggresive and lashes out at you.')
                battle('bear', prevent_coin_drop=True).fight_start()
                talk("In the morning, the farmer is overjoyed to hear you've gotten rid of the pest problem.")
                talk('He gives you his gold and thanks you for your work.')
        else:
            talk('You look at the large bear, and decide on leaving it be.')
            talk('You slip away under the cover of the night.')
    else:
        talk(f'{player_name}: Sorry, but I have too much to do, deal with it yourself.')

    return