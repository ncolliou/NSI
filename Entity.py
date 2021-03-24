import pygame


class Entity:
    def __init__(self, world, name, pos_x, pos_y, image, passive):
        self.world = world
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.image = pygame.transform.scale(image, (90, 90))
        self.passive = passive

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos_x, self.pos_y

    def get_passive(self):
        return self.passive

    def set_pos(self, x, y):
        self.pos_x = x
        self.pos_y = y

    def draw(self, screen):
        screen.blit(self.image, self.get_pos())
