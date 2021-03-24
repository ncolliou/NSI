class Item:
    def __init__(self, world, name, image, have_hitbox):
        self.world = world
        self.name = name
        self.image = image
        self.have_hitbox = have_hitbox

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def get_have_hitbox(self):
        return self.have_hitbox
