import pygame
from const import TILE_SIZE
from Item import Item


class Block:
    """
    Class qui initialise un block
    """

    def __init__(self, world, chunk, name, x, y, image, hardness, have_hitbox):
        """
        Constructor d'un block
        :param world: World.World --> monde auquel appartient le block
        :param chunk: Int --> position du block dans le monde dans un chunk (10xhauteur du monde)
        :param name: Str --> nom / id du block
        :param x: Int --> position x
        :param y: Int --> position y
        :param image: pygame.Surface --> image
        :param hardness: Int --> resistance du block (temps de minage)
        :param have_hitbox: Bool --> est ce que le block a une hitbox
        """
        self.world = world
        self.chunk = chunk
        # print(chunk)
        self.name = name
        # change la taille de l'image => TILE_SIZE² (60x60)
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # variable qui compte le temps ou la souris est appuyer sur le block
        self.timer = 0
        # resistance du block (temps de cassage) -1 -> block incassable
        self.hardness = hardness
        # collision avec ce block ?
        self.have_hitbox = have_hitbox

    def set_image(self, image):
        """
        Change la variable image
        """
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def set_name(self, name):
        """
        Change la variable name
        """
        self.name = name

    def get_rect(self):
        """
        Renvoie self.rect
        """
        return self.rect

    def get_pos(self):
        """
        Renvoie la position du block
        """
        return self.rect.x, self.rect.y, self.get_chunk()

    def get_chunk(self):
        """
        Renvoie le chunk dans leqeul le block est
        """
        return self.chunk

    def destroy(self):
        """
        Method qui permet de detruire les blocks (meilleur nom a trouve)
        """
        # recuperation de la position de la souris
        pos = pygame.mouse.get_pos()
        # si la souris est sur le block
        if pygame.mouse.get_pressed(3)[0] == 1:
            # si le bouton gauche de la souris est appuyer et que le temps ou il est appuyer est < self.hardness
            # (temps de cassage)
            if pygame.rect.Rect(self.get_rect().x * TILE_SIZE + self.get_chunk() * 10 * TILE_SIZE + self.world.decalagex,
                                self.get_rect().y * (-TILE_SIZE) + self.world.decalagey,
                                self.get_rect().w, self.get_rect().h).collidepoint(pos) and \
                    self.timer < self.hardness:
                # le block est en train d'etre casse
                self.timer += 1
            # si le temps ou il est maintenu est egal au temps de cassage (le block se casse)
            if self.timer == self.hardness:
                # recuperation de la cle du block
                key = str(self.get_pos()[0]) + "_" + str(self.get_pos()[1] - self.world.game.y + self.world.decalagey) + "_" + str(self.get_pos()[2])
                # ajout dans l'inventaire
                self.drop()
                # recuperation de la cle du block en dessous
                block_below = str(self.get_pos()[0]) + "_" + str(self.get_pos()[1] - self.world.game.y + self.world.decalagey - 1) + "_" + str(self.get_pos()[2])
                # s il existe un block en dessous de celui qui vient d etre casse
                if block_below in self.world.tile_list:
                    # update du block si c'est de la terre
                    self.update_grass(self.world.tile_list[block_below])
                # suppression du block dans le monde
                del (self.world.tile_list[key])
        # si le bouton gauche de la souris est relache ou
        # que la souris n'est plus sur le block => reinitialisation du compteur
        if pygame.mouse.get_pressed(3)[0] == 0 or not pygame.rect.Rect(
                self.get_rect().x * TILE_SIZE + self.get_chunk() * 10 * TILE_SIZE + self.world.decalagex,
                self.get_rect().y * (-TILE_SIZE) + self.world.decalagey,
                self.get_rect().w,
                self.get_rect().h).collidepoint(pos):
            self.timer = 0

    def update_grass(self, tile):
        """
        Method qui transforme de la dirt en grass s il n'y a pas de block au dessus
        """
        # si c'est de la dirt
        if tile.name == "dirt":
            # transformation de la dirt en grass (nom et image changent)
            tile.set_name("grass")
            tile.set_image(self.world.grass_img)
        # sinon on ne fait rien
        else:
            return

    def drop(self):
        """
        Ajoute un block a l'inventaire du joueur
        """
        # recuperation du 1er slot vide dans l inventaire ou s il y a deja le meme block dans l inventaire
        for key, value in self.world.game.player.inventory.items():
            if value.item is not None and value.item.name == self.name:
                self.world.game.player.inventory[key].count += 1
                return
        for key, value in self.world.game.player.inventory.items():
            if value.item is None:
                self.world.game.player.inventory[key].item = Item(self.world, self.name, self.world.blocks_img[self.name], self.have_hitbox)
                self.world.game.player.inventory[key].count = 1
                return
