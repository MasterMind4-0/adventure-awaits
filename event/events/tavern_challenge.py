import colors
import config
import random
from systems.tavern import tavern
from systems.battle import battle
from systems.shop import shop
from utils import talk, format_name, wait, calculate_chance, player_inventory_change, player_mc

tags = {
    'is_quest': False
}

def tavern_challenge():
    bartender = format_name("Bartender")
    player = format_name(config.name)

    talk('Completely beat, you walk into a tavern, sitting down by the bartender.')
    talk('You notice a crowd around a table across the tavern; getting drunk as if their was no tommorrow.')
    talk(f"{bartender}: I see you're interested.")
    match player_mc(['Nah, just let me see what you sell.', 'What\'s going on?'], leave_option=False):
        case '0':
            tavern().bartender_menu()
        case '1':
            talk(f"{bartender}: Well, those fools are drinking their heart out to win in a competition.")
            choice = input(f"{bartender}: Ya interested? (Y/N)\n")
            if choice.lower() == 'y':
                talk(f"{player}: Why not? What's to lose?")
                talk(f'{bartender}: Actually, you do lose something; admission is 5 coins.')
                talk(f'{bartender}: But hey, you could win the pot.')
                choice = input(f'{colors.THOUGHTS}Should I..? (Y/N)\n{colors.END}')
                if choice.lower() == 'y':
                    if config.coin < 5:
                        talk(f'{bartender}: Sorry, you do not have enough coins.')
                        talk(f'{bartender}: You might have enough for a drink if you want though.')
                        tavern().bartender_menu()
                    else:
                        amount_people = random.randint(3, 15)
                        random_value = random.random()
                        win_chance = .45 - (config.player_stats['constitution'] / 10)
                        config.coin -= 5

                        talk('You give the bartender the 5 coins.')
                        talk('You make you way down to the table.')
                        talk(f'There seems to be {amount_people} people at the table.')
                        talk('You sit and prepare yourself as the large beer is placed in front of you.')
                        talk(f'{bartender}: Alright, the rules are simple, drink the beer as fast as you can.')
                        talk(f'{bartender}: The first to finish, wins.')
                        talk(f"{bartender}: Now, let's begin!")
                        if random_value < win_chance:
                            talk('As you drink your large mug of ale,')
                            talk("You don't even pay attention to the others, you're set on your goal of winning.")
                            talk('And just before you black out, you take the last swig and slam the mug on the table.')
                            talk('You barely manage to hear the bartender saying you won.')
                            talk('You completely pass out, everything far beyond a haze.')
                            talk('You wake up on the streets in front of the tavern with a nasty headache. You shrug it off and get up to continue your journey.')
                            player_inventory_change(5 * amount_people)
                            config.player_health -= 1
                        else:
                            talk('As you down the mug, it sloshes down your chin.')
                            talk('And right there your fall, completely knocked out.')
                            talk(f'{player}: Ugh...')
                            tavern().alley_way()
                else:
                    print(f'{player}: Nah, just let me see what you sell.')
                    tavern().bartender_menu()
            else:
                print(f'{player}: Nah, just let me see what you sell.')
                tavern().bartender_menu()