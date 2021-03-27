import pygame
from const import SCREEN_WIDTH, SCREEN_HEIGHT, player_path_img, inventory_gui_path_img, hotbar_gui_path_img, \
    select_gui_path_img, TILE_SIZE
from Slot import Slot
from Block import Block
from Craft import Craft


class Player:
    """
    Class qui initialise le joueur
    """

    def __init__(self, game):
        self.game = game
        self.image = pygame.transform.scale(pygame.image.load(player_path_img), (30, 120))
        # chargement de l'image
        self.imageL = pygame.transform.flip(self.image, False, False)
        self.imageR = pygame.transform.flip(self.image, True, False)
        self.image = self.imageL
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
                self.inventory["Slot" + str(i) + "_" + str(j)] = Slot(None, i, j, 0)

        for j in range(1, 3):
            for i in range(1, 3):
                self.inventory["Slot" + str(i) + "_" + str(j) + "_Craft"] = Slot(None, i, j, 0, "craft_small")

        self.inventory["Slot0_0_Craft"] = Slot(None, 0, 0, 0, "result_craft_small")

        self.move_items = [False, None, None]
        self.decy = 0

        self.crafts = {}
        self.init_crafts()

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
                self.velocity = 7
            # deplacement sur la gauche
            if key[pygame.K_q]:
                dx += self.velocity
                self.image = self.imageR
            # deplacement sur la droite
            if key[pygame.K_d]:
                dx -= self.velocity
                self.image = self.imageL

        # gravite (ne pas chercher a comprendre sauf si vous voulez reflechir ;p), en vrai c'est simple
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy -= self.vel_y

        # collision
        # self.in_air = True
        for value in self.game.visible_map.values():
            if value.have_hitbox:
                # x direction
                while pygame.rect.Rect(
                        value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.game.world.decalagex,
                        value.get_rect().y * (-TILE_SIZE) + self.game.world.decalagey,
                        value.get_rect().w,
                        value.get_rect().h) \
                        .colliderect(self.rect.x - dx, self.rect.y, self.width, self.height):
                    if dx > 0:
                        dx -= 1
                    elif dx < 0:
                        dx += 1
                # y direction
                if pygame.rect.Rect(
                        value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.game.world.decalagex,
                        value.get_rect().y * (-TILE_SIZE) + self.game.world.decalagey,
                        value.get_rect().w,
                        value.get_rect().h) \
                        .colliderect(self.rect.x, self.rect.y - dy, self.width, self.height):
                    # en dessous du sol
                    if self.vel_y < 0:
                        # print("Hello there")
                        # dy = self.rect.top + value.get_rect().bottom - self.game.world.decalagey * TILE_SIZE
                        # print(self.rect.top)
                        # print(value.get_rect().bottom)
                        dy = 0
                        self.vel_y = 0
                    # au dessus du sol
                    elif self.vel_y >= 0:
                        dy = self.rect.bottom - value.get_rect().top * (-TILE_SIZE) - self.game.world.decalagey
                        # print(self.rect.bottom, value.get_rect().top, self.game.world.decalagey)
                        self.vel_y = 0
                        self.in_air = False

        # update de la position
        self.game.x += dx
        self.game.y += dy
        self.decy += dy
        self.game.world.cow.set_pos(self.game.world.cow.pos_x, self.game.world.cow.pos_y + dy)
        self.game.world.update_position(dx, dy)

        if self.game.open_inventory:
            for key, value in self.inventory.items():
                if value.click():
                    if value.item:
                        if not self.move_items[0]:
                            self.move_items = [True, value, key]
                    if value.item is None and self.move_items[0] and self.move_items[2] == "Slot0_0_Craft":
                        value.item = self.move_items[1].item
                        value.count = self.move_items[1].count
                        self.inventory[self.move_items[2]] = Slot(None, int(self.move_items[2][4]),
                                                                  int(self.move_items[2][6]),
                                                                  0, self.move_items[1].where)
                        self.move_items = [False, None, None]
                        self.inventory_update(screen)
                        self.crafts["planks"].use_slot.count -= 1
                        if self.crafts["planks"].use_slot.count <= 0:
                            self.crafts["planks"].use_slot.item = None
                            self.crafts["planks"].use_slot.count = 0

                    if value.item is None and self.move_items[0] and key != "Slot0_0_Craft":
                        value.item = self.move_items[1].item
                        value.count = self.move_items[1].count
                        self.inventory[self.move_items[2]] = \
                            Slot(None,
                                 int(self.move_items[2][4]), int(self.move_items[2][6]),
                                 0, self.move_items[1].where)
                        self.move_items = [False, None, None]
                        self.inventory_update(screen)
        if self.game.open_inventory:
            self.crafts["planks"].show_result()

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

    def get_item_hand(self):
        if self.inventory["Slot" + str(self.game.hotbar_num) + "_4"].item is not None:
            return self.inventory["Slot" + str(self.game.hotbar_num) + "_4"].item

    def place_block(self, pos):
        item = self.get_item_hand()
        if item is not None:
            chunk = (pos[0] // TILE_SIZE // 10) - (self.game.x // TILE_SIZE // 10)
            x = (pos[0] // TILE_SIZE % 10) - (self.game.x // TILE_SIZE % 10)
            y = (pos[1] // (-TILE_SIZE) + (self.game.world.decalagey // TILE_SIZE)) + 1
            b = Block(self.game.world, chunk, item.name, x, y, item.image, 50, item.have_hitbox)
            self.game.world.tile_list[str(x) + "_" + str(y) + "_" + str(chunk)] = b

    def init_crafts(self):
        self.crafts["planks"] = Craft(self, "assets/data/recipes/planks.json")
