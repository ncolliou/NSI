import pygame
from const import SCREEN_WIDTH, SCREEN_HEIGHT, player_path_img, inventory_gui_path_img, hotbar_gui_path_img, \
    select_gui_path_img, font_path, TILE_SIZE


class Player:
    """
    Class qui initialise le joueur
    """
    def __init__(self, game):
        self.game = game
        # chargement de l'image
        self.image = pygame.image.load(player_path_img)
        self.rect = self.image.get_rect()
        # position du joueur au debut
        self.rect.x = SCREEN_WIDTH // 2
        self.rect.y = 360
        # taille du joueur
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # vitesse du joueur
        self.velocity = 5
        # gestion de la gravite ne pas changer !
        self.vel_y = 0
        # le joueur ne saute pas au debut
        self.jumped = False
        # est ce que le joueur est dans les airs
        self.in_air = True
        # inventaire du joueur
        self.inventory = {}
        self.dont_play = False
        # chargement des images
        self.inventory_img = pygame.image.load(inventory_gui_path_img)
        self.hotbar_img = pygame.image.load(hotbar_gui_path_img)
        self.hotbar_img_rect = self.hotbar_img.get_rect()
        self.hotbar_img_rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-33)
        self.select_hotbar = pygame.image.load(select_gui_path_img)
        self.select_hotbar_rect = self.select_hotbar.get_rect()

        self.move_items = False

    def update(self):
        """
        Method qui update la position du joueur (le monde bouge pour que le joueur soit toujours au centre de l'ecran)
        """
        # futur position du joueur
        dx = 0
        dy = 0

        # recuperation des touches presser
        self.velocity = 5
        key = pygame.key.get_pressed()
        # si on appuye sur la touche espace et qu'on est sur le sol
        if not self.dont_play:
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -13
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LCTRL]:
                self.velocity = 10
            # deplacement sur la gauche
            if key[pygame.K_q]:
                dx += self.velocity
            # deplacement sur la droite
            if key[pygame.K_d]:
                dx -= self.velocity

        # gravite (ne pas chercher a comprendre sauf si vous voulez reflechir ;p), en vrai c'est simple
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy -= self.vel_y

        # collision
        # self.in_air = True
        for tile in self.game.visible_map:
            if tile.have_hitbox:
                # x direction
                if pygame.rect.Rect(tile.get_rect().x + tile.get_chunk()*10*TILE_SIZE + self.game.world.decalagex,
                                    tile.get_rect().y,
                                    tile.get_rect().w,
                                    tile.get_rect().h)\
                        .colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y direction
                if pygame.rect.Rect(tile.get_rect().x + tile.get_chunk()*10*TILE_SIZE + self.game.world.decalagex,
                                    tile.get_rect().y,
                                    tile.get_rect().w,
                                    tile.get_rect().h)\
                        .colliderect(self.rect.x, self.rect.y - dy, self.width, self.height):
                    # en dessous du sol
                    if self.vel_y < 0:
                        dy = self.rect.top - tile.get_rect().bottom
                        self.vel_y = 0
                    # au dessus du sol
                    elif self.vel_y >= 0:
                        dy = self.rect.bottom - tile.get_rect().top
                        self.vel_y = 0
                        self.in_air = False

        # update de la position
        self.game.x += dx
        self.game.y += dy
        self.game.world.update_position(dx)
        for tile in self.game.world.tile_list:
            tile.get_rect().y += dy

    def inventory_update(self, screen):
        """
        Update l'inventaire du joueur et affichage de celui ci avec uniquement s'il y a des blocks
        """
        # reset i et j
        i = 0
        j = 0
        if self.game.open_inventory:
            if i == 9:
                i = 0
                j += 1
            if j == 3:
                j = 0
            for key, value in self.inventory.items():
                # s'il y a au moins un block dans le dictionnaire
                if not value == 0:
                    # afficher le block
                    if j >= 1:
                        screen.blit(self.game.world.blocks_img[key], self.inventory[key][1:])
                    else:
                        screen.blit(self.game.world.blocks_img[key], self.inventory[key][1:])
                    # afficher le nombre de blocks
                    self.draw_text(screen, str(self.inventory[key][0]), (255, 255, 255), self.inventory[key][1]+26,
                                   self.inventory[key][2]+27, 20)
                    # augmenter le compteur pour que chaque image ne soit pas sur la precedente 294-320 541-568
                    i += 1

            # if self.move_items:
            #     screen.blit(self.game.world.blocks_img[self.k], (pygame.mouse.get_pos()))

    def hotbar_update(self, screen):
        i = 0
        if i == 9:
            i = 0
        for key, value in self.inventory.items():
            if not value == 0:
                screen.blit(self.game.world.blocks_img[key], (309 + 14 * i + 39*i, 668))
                self.draw_text(screen, str(self.inventory[key][0]), (255, 255, 255), 335 + 14*i+39*i, 695, 20)
                i += 1

    def update_inv(self, name, count, x, y):
        self.inventory[name] = [count, x, y]

    # noinspection PyMethodMayBeStatic
    # ne pas chercher a comprendre c'est juste sur PyCharm
    def draw_text(self, screen, text, text_color, x, y, size=30):
        """
        Dessine du texte
        """
        # initialisation de la police et de la taille
        font = pygame.font.Font(font_path, size)
        # application du texte et de la couleur
        # a noter que la methode render fonction comme pour une image avec le texte
        text = font.render(text, True, text_color)
        # afficher le texte
        screen.blit(text, (x, y))
