import pygame
from aleatoire import random_number_int
from Block import Block
from const import TILE_SIZE, \
    grass_block_path_img, dirt_block_path_img, stone_block_path_img, log_block_path_img, leaves_block_path_img, \
    bedrock_block_path_img, tallgrass_block_path_img, coal_block_path_img, cow_path_img
from Entity import Entity
from Text import Text


class World:
    """
    Class qui initialise le monde
    """

    def __init__(self, data, game):
        # liste qui sauvegarde les blocks avec leurs positions
        self.tile_list = {}
        self.data = data
        self.game = game
        # chargements images
        self.dirt_img = pygame.image.load(dirt_block_path_img)
        self.grass_img = pygame.image.load(grass_block_path_img)
        self.stone_img = pygame.image.load(stone_block_path_img)
        self.log_img = pygame.image.load(log_block_path_img)
        self.leaves_img = pygame.image.load(leaves_block_path_img)
        self.bedrock_img = pygame.image.load(bedrock_block_path_img)
        self.tallgrass_img = pygame.image.load(tallgrass_block_path_img)
        self.coal_img = pygame.image.load(coal_block_path_img)
        # utiliser dans l'inventaire et la hotbar
        self.blocks_img = {
            "dirt": pygame.transform.scale(self.dirt_img, (39, 39)),
            "grass": pygame.transform.scale(self.grass_img, (39, 39)),
            "stone": pygame.transform.scale(self.stone_img, (39, 39)),
            "log": pygame.transform.scale(self.log_img, (39, 39)),
            "leaves": pygame.transform.scale(self.leaves_img, (39, 39)),
            "tallgrass": pygame.transform.scale(self.tallgrass_img, (39, 39)),
            "coal": pygame.transform.scale(self.coal_img, (39, 39))
        }
        self.decalagex = 0
        self.decalagey = 0
        self.cow = Entity(self, "cow", 120, 480 + self.data[2] - 89, pygame.image.load(cow_path_img), True)
        self.dec = -250

    def create_random(self):
        """
        Method qui cree la map avec la liste de nb genere aleatoirement
        """
        t = 0
        # + 1 sinon le jeu plante ;)
        # if self.data[8] > 0:
        #     up = (self.data[8]*60 + 60)
        # elif self.data[8] < 0:
        #     up = + 1 # self.data[8] - 1
        # else:
        #     up = 0
        up = 0
        # up = abs(self.data[8]*(60)) + 2
        # print(abs(self.data[8]*(60)) + 2)
        # print(up)
        # pour chaque item de self.data
        for col_count in range(len(self.data)):
            if random_number_int(5) and t > 6:
                t = 0
                pass
                # initialisation d'un arbre
                self.tree(col_count, up)
            # le block du dessus est de la grass
            else:
                t += 1
                # print(self.data[col_count] * (-TILE_SIZE))
                tile = Block(self, (self.dec + col_count) // 10, "grass", col_count % 10,
                             self.data[col_count] + up, self.grass_img, 50, True)
                self.tile_list[str(col_count % 10) + "_" + str(
                    self.data[col_count]) + "_" + str((self.dec + col_count) // 10)] = tile
                if random_number_int(40):
                    tile = Block(self, (self.dec + col_count) // 10, "tallgrass", col_count % 10,
                                 self.data[col_count] + 1 + up, self.tallgrass_img, 20,
                                 False)
                    self.tile_list[str(col_count % 10) + "_" +
                                   str(self.data[col_count] + 1) + "_" + str((self.dec + col_count) // 10)] = tile
            # on ajoute 3 blocks de dirt en dessous de la grass
            for i in range(0, 3):
                tile = Block(self, (self.dec + col_count) // 10, "dirt", col_count % 10,
                             self.data[col_count] + up + (-1) - 1 * i, self.dirt_img, 50, True)
                self.tile_list[str(col_count % 10) + "_" +
                               str(self.data[col_count] + (-1) - 1 * i) + "_" + str(
                    (self.dec + col_count) // 10)] = tile

            tile = Block(self, (self.dec + col_count) // 10, "bedrock", col_count % 10,
                         - 20 + up,
                         self.bedrock_img, -1, True)
            self.tile_list[
                str(col_count % 10) + "_" + str(20) + "_" + str(
                    (self.dec + col_count) // 10)] = tile

            # on ajouter 10 blocks de stone en dessous de la dirt
            for i in range(3, 19 + self.data[col_count]):
                if random_number_int(10):
                    tile = Block(self, (self.dec + col_count) // 10, "coal", col_count % 10,
                                 self.data[col_count] + (-1) - 1 * i + up, self.coal_img, 150,
                                 True)
                    self.tile_list[str(col_count % 10) + "_" +
                                   str(self.data[col_count] + (-1) - 1 * i) + "_" + str(
                        (self.dec + col_count) // 10)] = tile
                else:
                    tile = Block(self, (self.dec + col_count) // 10, "stone", col_count % 10,
                                 self.data[col_count] + up + (-1) - 1 * i, self.stone_img, 150,
                                 True)
                    self.tile_list[str(col_count % 10) + "_" +
                                   str(self.data[col_count] + (-1) - 1 * i) + "_" + str(
                        (self.dec + col_count) // 10)] = tile

    def draw(self, screen):
        """
        Method qui applique chaque block sur screen avec sa position sauf s'il est en dehors de l'ecran
        """
        for key, value in self.game.visible_map.items():
            screen.blit(value.image, (
                value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.decalagex,
                value.get_rect().y * (-TILE_SIZE) + self.decalagey))
            # Text(key, (255, 255, 255), value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.decalagex,
            #      value.get_rect().y * (-TILE_SIZE) + self.decalagey, size=13).draw(screen)
            # Text(str(value.get_rect().x + value.get_chunk() * 10 * TILE_SIZE + self.decalagex) + " " +
            #      str(value.get_rect().y + self.decalagey) + " " + str(value.get_chunk()), (255, 255, 255), value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.decalagex,
            #      value.get_rect().y * (-TILE_SIZE) + self.decalagey + 20, size=13).draw(screen)
            if not self.game.player.dont_play:
                value.destroy()
        self.cow.set_pos(self.decalagex, self.cow.pos_y)
        self.cow.draw(screen)

    def update_position(self, x, y):
        """
        Method qui change la position des blocks en x et y par rapport à sa position precedente
        """
        self.decalagex += x
        self.decalagey += y

    def tree(self, col_count, up):
        tile = Block(self, (self.dec + col_count) // 10, "dirt", col_count % 10,
                     self.data[col_count] + up, self.dirt_img, 50, True)
        self.tile_list[str(col_count % 10) + "_" + str(self.data[col_count]) + "_" + str((self.dec + col_count) // 10)] = tile
        for i in range(2, 5):
            tile = Block(self, (self.dec + col_count) // 10, "log", col_count % 10,
                         self.data[col_count] + up - 1 + 1 * i, self.log_img, 75, True)
            self.tile_list[str(col_count % 10) + "_" + str(self.data[col_count] - 1 + 1 * i) + "_" + str((self.dec + col_count) // 10)] = tile
        for i in range(-2, 3):
            for j in range(0, 2):
                tile = Block(self, (self.dec + col_count + i) // 10, "leaves", (col_count + i) % 10,
                             self.data[col_count] + up + 4 + 1 * j, self.leaves_img, 25, True)
                self.tile_list[str((col_count + i) % 10) + "_" + str(self.data[col_count] + 4 + 1 * j) + "_" + str((self.dec + col_count + i) // 10)] = tile

        for i in range(-1, 2):
            tile = Block(self, (self.dec + col_count + i) // 10, "leaves", (col_count + i) % 10,
                         self.data[col_count] + up + 6, self.leaves_img, 25, True)
            self.tile_list[str((col_count + i) % 10) + "_" + str(self.data[col_count] + 6) + "_" + str(
                (self.dec + col_count + i) // 10)] = tile

        tile = Block(self, (self.dec + col_count) // 10, "leaves", col_count % 10,
                     self.data[col_count] + up + 7, self.leaves_img, 25, True)
        self.tile_list[str(col_count % 10) + "_" + str(self.data[col_count] + 7) + "_" + str(
            (self.dec + col_count) // 10)] = tile
