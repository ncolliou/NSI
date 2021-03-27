import json
from Item import Item


class Craft:
    """
    Class qui initialise un craft
    """
    def __init__(self, player, path):
        """
        Constructor d'un craft
        :param player: Player.player --> joueur qui utilise les crafts
        :param path: chemin du fichier pour lire le craft (.json)
        """
        self.player = player
        # ouvrir le fichier et le charger en tant que json
        self.data = json.load(open(path))
        # recuperation de la taille du craft
        self.size = (len(self.data['pattern'][0]), len(self.data['pattern']))
        # tuple avec le resultat en item et le nombre en 2eme
        self.result = {"item": self.data["result"]["item"], "count": self.data["result"]["count"]}
        # pattern du craft
        self.pattern = self.data["pattern"]
        # ingredients neccesaire pour le craft
        self.ingredients = [value["item"] for value in self.data["key"].values()]
        # ingredients lies avec un cle
        self.ingredients2 = {}
        for key, value in self.data["key"].items():
            self.ingredients2[key] = value["item"]
        # position des ingredients
        self.ingredients_pos = {}
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.data["pattern"][x][y] == " ":
                    print("Nothing here")
                else:
                    self.ingredients_pos[str(x) + "_" + str(y)] = self.data["pattern"][x][y]
        # les 4 slots pour les crafts dans l'inventaire
        self.slot_craft_small = [self.player.inventory["Slot1_1_Craft"], self.player.inventory["Slot1_2_Craft"],
                                 self.player.inventory["Slot2_1_Craft"], self.player.inventory["Slot2_2_Craft"]]
        # slot du resultat
        self.slot_result = self.player.inventory["Slot0_0_Craft"]
        # le ou les slots utiliser pour le crafts
        self.use_slot = None

    def get_result(self):
        """
        Renvoie le resultat
        :return: self.result
        """
        return self.result

    def get_ingredients(self):
        """
        Renvoie le / les ingredients
        :return: self.ingredients
        """
        return self.ingredients

    def get_pos_ingredients(self):
        """
        Renvoie un dictionnaire avec coordonnees et les ingredients associes
        :return: self.ingredients_pos
        """
        return self.ingredients_pos

    def get_size(self):
        """
        Renvoie la taille du craft
        :return: self.size
        """
        return self.size

    def show_result(self):
        if self.size == (1, 1):
            for slot in self.slot_craft_small:
                if slot.item is not None and slot.item.name == "log":
                    self.use_slot = slot
                    self.slot_result.item = Item(self.player.game.world, self.get_result()["item"], self.player.game.world.blocks_img[self.get_result()["item"]], True)
                    self.slot_result.count = self.get_result()["count"]
                    print(self.slot_result.item)
                    print(self.slot_result.count)
                    break
                else:
                    self.slot_result.item = None
                    self.slot_result.count = 0
