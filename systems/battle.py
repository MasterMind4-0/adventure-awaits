import colors
import config
from utils import loading_json_entities

loading_json_entities()

class battle:
    def __init__(self, preset: str):
        preset = preset.lower()

        self.enemy_health = entities['enemies'][preset]['health']
        self.enemy_weapon = entities['enemies'][preset]['weapon']
        self.enemy_armor = entities['enemies'][preset]['armor']
        self.drop = {}
        for element in list(entities['enemies'][preset]['drops'].key()):
            self.drop = entities['enemies'][element].key()
            self.drop_chances = entities['enemies'][element].value()
        self.gold_drop = entities['enemies'][preset]['health'] * .4