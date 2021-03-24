import pygame
from Text import Text
from const import dirt_block_path_img


class Slot:
    def __init__(self, item, pos_x, pos_y, count, where="inv"):
        self.item = item
        self.where = where
        if self.where == "inv":
            self.pos_x = 241 + 53 * pos_x
            if pos_y == 4:
                self.pos_y = 328 + pos_y*53
            else:
                self.pos_y = 315 + pos_y*53
        elif self.where == "craft_small":
            self.pos_x = 506 + 53 * pos_x
            self.pos_y = 128 + 53 * pos_y
        elif self.where == "result_craft_small":
            self.pos_x = 702
            self.pos_y = 210
        self.count = count
        self.rect = pygame.rect.Rect(self.pos_x, self.pos_y, 47, 47)
        self.clicked = False

    def get_pos(self):
        return self.pos_x, self.pos_y

    def get_item(self):
        return self.item

    def get_count(self):
        return self.count

    def draw_item(self, screen, hotbar=False):
        if self.item is None:
            return
        else:
            if not hotbar and self.where == "inv":
                screen.blit(self.item.image, self.get_pos())
            if hotbar and self.where == "inv":
                screen.blit(self.item.image, (self.pos_x+14, self.pos_y+127))
            if self.where == "craft_small":
                screen.blit(self.item.image, self.get_pos())
            if self.where == "result_craft_small":
                screen.blit(self.item.image, self.get_pos())

    def draw_count(self, screen, hotbar=False):
        if self.item is not None:
            if self.count >= 10:
                if not hotbar:
                    Text(str(self.count), (255, 255, 255), self.pos_x + 20, self.pos_y + 27, 20).draw(screen)
                else:
                    Text(str(self.count), (255, 255, 255), self.pos_x + 42, self.pos_y + 155, 20).draw(screen)
            else:
                if not hotbar:
                    Text(str(self.count), (255, 255, 255), self.pos_x + 26, self.pos_y + 27, 20).draw(screen)
                else:
                    Text(str(self.count), (255, 255, 255), self.pos_x + 48, self.pos_y + 155, 20).draw(screen)

    def click(self):
        action = False
        # recuperation de la position de la souris
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            # si le bouton gauche de la souris est appuye mais qu'il n'est pas enfonce
            if pygame.mouse.get_pressed(3)[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        # si le bouton gauche de la souris n'est pas appuye
        if pygame.mouse.get_pressed(3)[0] == 0:
            self.clicked = False

        return action
