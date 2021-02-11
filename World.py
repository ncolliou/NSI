import pygame
from aleatoire import random_number_int
from Block import Block
from const import TILE_SIZE, \
    grass_block_path_img, dirt_block_path_img, stone_block_path_img, log_block_path_img, leaves_block_path_img, \
    bedrock_block_path_img, tallgrass_block_path_img, coal_block_path_img


class World:
    """
    Class qui initialise le monde
    """

    def __init__(self, data, game):
        # liste qui sauvegarde les blocks avec leurs positions
        self.tile_list = []
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

    def create_random(self):
        """
        Method qui cree la map avec la liste de nb genere aleatoirement
        """
        t = 0
        # pour chaque item de self.data
        for col_count in range(len(self.data)):
            if random_number_int(5) and t > 7:
                t = 0
                # initialisation d'un arbre
                self.init_tree(col_count)
            # le block du dessus est de la grass
            else:
                t += 1
                tile = Block(self, col_count // 10, "grass", col_count % 10 * TILE_SIZE,
                             self.data[col_count] * (-TILE_SIZE) + 1000, self.grass_img, 50, True)
                self.tile_list.append(tile)
                if random_number_int(40):
                    tile = Block(self, col_count // 10, "tallgrass", col_count % 10 * TILE_SIZE,
                                 self.data[col_count] * (-TILE_SIZE) - TILE_SIZE + 1000, self.tallgrass_img, 20, False)
                    self.tile_list.append(tile)
            # on ajoute 3 blocks de dirt en dessous de la grass
            for i in range(1, 4):
                tile = Block(self, col_count // 10, "dirt", col_count % 10 * TILE_SIZE,
                             self.data[col_count] * (-TILE_SIZE) + 1000 + TILE_SIZE * i, self.dirt_img, 50, True)
                self.tile_list.append(tile)

            tile = Block(self, col_count // 10, "bedrock", col_count % 10 * TILE_SIZE, TILE_SIZE * 20 + 1000,
                         self.bedrock_img, -1, True)
            self.tile_list.append(tile)

            # on ajouter 10 blocks de stone en dessous de la dirt
            for i in range(4, 20 + self.data[col_count]):
                if random_number_int(10):
                    tile = Block(self, col_count // 10, "coal", col_count % 10 * TILE_SIZE,
                                 self.data[col_count] * (-TILE_SIZE) + 1000 + TILE_SIZE * i, self.coal_img, 150, True)
                    self.tile_list.append(tile)
                else:
                    tile = Block(self, col_count // 10, "stone", col_count % 10 * TILE_SIZE,
                                 self.data[col_count] * (-TILE_SIZE) + 1000 + TILE_SIZE * i, self.stone_img, 150, True)
                    self.tile_list.append(tile)

    def draw(self, screen):
        """
        Method qui applique chaque block sur screen avec sa position sauf s'il est en dehors de l'ecran
        """
        for tile in self.game.visible_map:
            screen.blit(tile.image, (
                tile.get_rect().x + tile.get_chunk() * 10 * TILE_SIZE + self.decalagex,
                tile.get_rect().y))
            if not self.game.player.dont_play:
                tile.destroy()
                tile.place()

    def update_position(self, x):
        """
        Method qui change la position des blocks en x et y par rapport à sa position precedente
        """
        self.decalagex += x
        # for tile in self.tile_list:
        #     tile.get_rect().x += x
        #     tile.get_rect().y += y

    def init_tree(self, col_count):
        # tronc d'arbre
        for i in range(3):
            tile = Block(self, col_count // 10, "log", col_count % 10 * TILE_SIZE,
                         self.data[col_count] * (-TILE_SIZE) + 1000 - TILE_SIZE * (i + 1),
                         self.log_img, 75, True)
            self.tile_list.append(tile)
        # leaves
        for j in range(-2, 3):
            # if not j == 0:
            tile = Block(self, col_count // 10, "leaves", col_count % 10 * TILE_SIZE - TILE_SIZE * j,
                         (self.data[col_count] + 4) * (-TILE_SIZE) + 1000, self.leaves_img, 25, True)
            self.tile_list.append(tile)
            tile = Block(self, col_count // 10, "leaves", col_count % 10 * TILE_SIZE - TILE_SIZE * j,
                         (self.data[col_count] + 5) * (-TILE_SIZE) + 1000, self.leaves_img, 25, True)
            self.tile_list.append(tile)
        for i in range(-1, 2):
            tile = Block(self, col_count // 10, "leaves", col_count % 10 * TILE_SIZE - TILE_SIZE * i,
                         (self.data[col_count] + 6) * (-TILE_SIZE) + 1000, self.leaves_img, 25, True)
            self.tile_list.append(tile)
        tile = Block(self, col_count // 10, "leaves", col_count % 10 * TILE_SIZE,
                     (self.data[col_count] + 7) * (-TILE_SIZE) + 1000, self.leaves_img, 25, True)
        self.tile_list.append(tile)
        # dirt sous l'arbre
        tile = Block(self, col_count // 10, "dirt", col_count % 10 * TILE_SIZE,
                     self.data[col_count] * (-TILE_SIZE) + 1000, self.dirt_img, 50, True)
        self.tile_list.append(tile)
