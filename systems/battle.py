import colors
import config
import random
from utils import loading_json_entities, talk

loading_json_entities()

class battle:
    def __init__(self, preset: str):
        preset = preset.lower()

        self.enemy_display_name = entities['enemies'][preset]['display_name']
        self.enemy_health = entities['enemies'][preset]['health']
        self.enemy_weapon = entities['enemies'][preset]['weapon']
        self.enemy_armor = entities['enemies'][preset]['armor']
        self.drop = {}
        for element in list(entities['enemies'][preset]['drops'].key()):
            self.drop = entities['enemies'][element].key()
            self.drop_chances = entities['enemies'][element].value()
        self.gold_drop = entities['enemies'][preset]['health'] * .4

    def fight_start(self, custom_entry_phrase: str = ""):
        entry_phrasels = [
            f"{self.enemy_display_name} looks in your eyes with pure rage.",
            f"{self.enemy_display_name} walks towards you, weapon in hand."
        ]

        if custom_entry_phrase:
            entry_phrase = custom_entry_phrase
        else:
            entry_phrase = random.choice(entry_phrasels)

        talk(entry_phrase)
    
    def 

    def player_turn(self):