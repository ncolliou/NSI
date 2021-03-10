import pygame
import const


class Text:
    def __init__(self, text, text_color, x, y, size=30, font_path=const.font_path):
        self.text = text
        self.text_color = text_color
        self.x = x
        self.y = y
        self.font_path = font_path
        self.size = size
        self.font = self.init_font()

    def init_font(self):
        return pygame.font.Font(self.font_path, self.size)

    def draw(self, screen):
        # initialisation de la police et de la taille
        # application du texte et de la couleur
        # a noter que la methode render fonction comme pour une image avec le texte
        text = self.font.render(self.text, True, self.text_color)
        # afficher le texte
        screen.blit(text, (self.x, self.y))

    def set_text(self, text):
        self.text = text

    def set_text_color(self, color):
        self.text_color = color
