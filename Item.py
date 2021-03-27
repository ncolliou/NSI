class Item:
    """
    Class d'un item
    """
    def __init__(self, world, name, image, have_hitbox):
        """
        Constructor d'un item
        :param world: World.world --> monde dans lequel le jeu se passe
        :param name: Str --> nom de l item
        :param image: pygame.Surface --> image de l item
        :param have_hitbox: Bool --> est ce que l item en tant que block a une hb
        """
        self.world = world
        self.name = name
        self.image = image
        self.have_hitbox = have_hitbox

    def get_name(self):
        """
        Renvoie le nom de l item
        :return: self.name
        """
        return self.name

    def get_image(self):
        """
        Renvoie l'image de l item
        :return: self.image
        """
        return self.image

    def get_have_hitbox(self):
        """
        Renvoie la valeur de have_hitbox (si le block à une hb)
        :return: self.have_hitbox
        """
        return self.have_hitbox
