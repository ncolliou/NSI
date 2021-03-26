import json


class Craft:
    def __init__(self, player, path):
        self.player = player
        self.data = json.load(open(path))
        self.size = [len(self.data['pattern'][0]), len(self.data['pattern'])]
        self.result = {"item": self.data["result"]["item"], "count": self.data["result"]["count"]}
        self.pattern = self.data["pattern"]
        self.ingredients = [value["item"] for value in self.data["key"].values()]
        self.ingredients2 = {}
        for key, value in self.data["key"].items():
            self.ingredients2[key] = value["item"]
        self.ingredients_pos = {}
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                if self.data["pattern"][x][y] == " ":
                    print("Nothing here")
                else:
                    self.ingredients_pos[str(x) + "_" + str(y)] = self.data["pattern"][x][y]

    def get_result(self):
        return self.result

    def get_ingredients(self):
        return self.ingredients

    def get_pos_ingredients(self):
        return self.ingredients_pos

    def get_size(self):
        return self.size

    def show_result(self):
        if self.player.inventory["Slot1_1_Craft"].item is not None:
            if self.player.inventory["Slot1_1_Craft"].item.name == "log":
                print("Hellllllo")
