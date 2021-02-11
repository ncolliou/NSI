import pygame
from const import TILE_SIZE


class Block:
    """
    Class qui initialise un block
    """

    def __init__(self, world, chunk, name, x, y, image, hardness, have_hitbox):
        """
        Constructor d'un block
        :param world: World.World --> monde auquel appartient le block
        :param chunk: liste de block
        :param name: Str --> nom / id du block
        :param x: Int --> position x
        :param y: Int --> position y
        :param image: pygame.Surface --> image
        :param hardness: Int --> resistance du block (temps de minage)
        :param have_hitbox: Bool --> est ce que le block a une hitbox
        """
        self.world = world
        self.chunk = chunk
        self.name = name
        # verification que l'image fait bien TILE_SIZE² (60x60)
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        # variable qui compte le temps ou la souris est appuyer sur le block
        self.timer = 0
        # resistance du block (temps de cassage) -1 -> block incassable
        self.hardness = hardness
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
            # si le bouton gauche de la souris est appuyer et que le temps ou il est appuyer est < self.hardness (temps de cassage)
            if pygame.rect.Rect(self.get_rect().x + self.get_chunk()*10*TILE_SIZE + self.world.decalagex, self.get_rect().y, self.get_rect().w, self.get_rect().h).collidepoint(pos) and self.timer < self.hardness:
                # augmentation du temps ou il est appuyer
                self.timer += 1
            # si le temps ou il est maintenu est egale au temps de cassage (le block se casse)
            if self.timer == self.hardness:
                # pour chaque block dans le monde (optimisation possible [faire ca uniquement pour les blocks dans l'ecran])
                for i in range(len(self.world.tile_list)):
                    # si la position du block est egale a la position de la souris
                    if self.world.tile_list[i].get_rect().x+self.world.tile_list[i].get_chunk()*10*TILE_SIZE + self.world.decalagex == self.get_pos()[0]+self.get_chunk()*10*TILE_SIZE + self.world.decalagex and self.world.tile_list[i].get_rect().y == self.get_pos()[1] and self.world.tile_list[i].get_chunk() == self.get_pos()[2]:
                        # recuperation du block sous le block qui vient d'etre casse et si c'est de la dirt -> transformation en grass
                        self.update_grass(self.get_block_above(self.world.tile_list[i].rect.x+self.get_chunk()*10*TILE_SIZE + self.world.decalagex,
                                                               self.world.tile_list[i].rect.y + TILE_SIZE))
                        # ajout du block dans l'inventaire du joueur
                        self.drop()
                        # suppression du block
                        self.world.tile_list.pop(i)
                        break
        # si le bouton gauche de la souris est relache ou que la souris n'est plus sur le block => reinitialisation du compteur
        if pygame.mouse.get_pressed(3)[0] == 0 or not pygame.rect.Rect(self.get_rect().x + self.get_chunk()*10*TILE_SIZE + self.world.decalagex, self.get_rect().y, self.get_rect().w, self.get_rect().h).collidepoint(pos):
            self.timer = 0

    def place(self):
        """
        A voir
        """
        if self.world.game.right_click:
            if pygame.rect.Rect(self.get_rect().x + self.get_chunk()*10*TILE_SIZE + self.world.decalagex, self.get_rect().y, self.get_rect().w, self.get_rect().h).collidepoint(pygame.mouse.get_pos()):
                print("Not collide")

    def get_block_above(self, x, y):
        """
        Method qui renvoie le block aux coordonnees x, y
        Flemme d'expliquer la methode parce que bon voila...
        """
        for tile in self.world.game.visible_map:
            if tile.rect.x+tile.get_chunk()*10*TILE_SIZE + self.world.decalagex == x and tile.rect.y == y:
                return tile

    def update_grass(self, tile):
        """
        Method qui transforme de la dirt en grass s'il n'y a pas de block au dessus
        """
        # si tile n'est pas un block -> renvoie rien
        if not type(tile) == Block:
            return
        # si c'est de la dirt
        if tile.name == "dirt":
            # transformation de la dirt en grass (nom et image changent)
            tile.set_name("grass")
            tile.set_image(self.world.grass_img)

    def drop(self):
        """
        Ajoute un block a l'inventaire du joueur
        """
        # si le block n'a jamais ete dans l'inventaire
        taille = len(self.world.game.player.inventory)
        if self.name not in self.world.game.player.inventory.keys():
            self.world.game.player.update_inv(self.name, 0, 294 + 14 * taille + 39 * taille, 538)
        # ajout du block dans l'inventaire
        self.world.game.player.inventory[self.name][0] = self.world.game.player.inventory[self.name][0] + 1
