class Item:
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image
