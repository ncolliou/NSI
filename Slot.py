import pygame


class Slot:
    def __init__(self, pos):
        self.pos = pos
        self.contenu = [None]*2

    def get_contenu(self):
        return self.contenu

    def get_pos(self):
        return self.pos

    def draw(self):
        pass
