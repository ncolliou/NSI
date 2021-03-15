import pygame
from const import SCREEN_WIDTH, SCREEN_HEIGHT, player_path_img, inventory_gui_path_img, hotbar_gui_path_img, \
    select_gui_path_img, TILE_SIZE
from Slot import Slot


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
        self.hotbar_img_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 33)
        self.select_hotbar = pygame.image.load(select_gui_path_img)
        self.select_hotbar_rect = self.select_hotbar.get_rect()

        self.move_items = False

        # l = [4, 1, 2, 3]
        for j in [4, 1, 2, 3]:
            for i in range(1, 10):
                self.inventory["Slot"+str(i)+"_"+str(j)] = Slot(None, i, j, 0)
        self.move_items = [False, None, None]

    def update(self, screen):
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
                self.velocity = 6
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
                if pygame.rect.Rect(tile.get_rect().x + tile.get_chunk() * 10 * TILE_SIZE + self.game.world.decalagex,
                                    tile.get_rect().y,
                                    tile.get_rect().w,
                                    tile.get_rect().h) \
                        .colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                    dx = 0
                # y direction
                if pygame.rect.Rect(tile.get_rect().x + tile.get_chunk() * 10 * TILE_SIZE + self.game.world.decalagex,
                                    tile.get_rect().y,
                                    tile.get_rect().w,
                                    tile.get_rect().h) \
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

        if self.game.open_inventory:
            for key, value in self.inventory.items():
                if value.click():
                    if value.item:
                        if not self.move_items[0]:
                            self.move_items = [True, value, key]
                    if value.item is None and self.move_items[0]:
                        value.item = self.move_items[1].item
                        value.count = self.move_items[1].count
                        self.inventory[self.move_items[2]] = Slot(None, int(self.move_items[2][4]), int(self.move_items[2][6]), 0)
                        self.move_items = [False, None, None]
                        self.inventory_update(screen)

    def inventory_update(self, screen):
        """
        Update l'inventaire du joueur et affichage de celui ci
        """

        if self.game.open_inventory:
            for value in self.inventory.values():
                value.draw_item(screen)
                value.draw_count(screen)

    def hotbar_update(self, screen):
        for value in self.inventory.values():
            if value.pos_y == 540:
                value.draw_item(screen, True)
                value.draw_count(screen, True)
