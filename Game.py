import pygame
import random
from Player import Player
from Sound import SoundManager
from World import World
from Button import Button
from const import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, background_path_img, \
    button_path_img
from aleatoire import generate_map


class Game:
    """
    Class qui initialise le jeu
    (A faire le joueur devrai apparaitre sur le block le plus haut pas dans les airs)
    """

    def __init__(self):
        # import de l'arriere plan
        self.background = pygame.image.load(background_path_img)
        # creation du joueur
        self.seed = random.randint(1, 100)
        # affichage de la seed pour avoir la meme map par exemple
        print(self.seed)
        self.player = Player(self)
        # initialisation de la map
        # random.randint(1, nbTotalDeMapsPossibleDansLaGenerationCustom), taille de la map
        # seed precise : 19 ou 93 sont speciales (19 sans better et 45 aussi est cool)
        # A voir absolument 31 et 77
        # self.map = generate_map(63, 500)
        self.map = generate_map(self.seed, 500)
        # initialisation du monde
        self.world = World(self.map, self)

        # creation du monde
        self.world.create_random()
        # liste qui contient tous les blocks visible sur l'ecran
        self.visible_map = []

        # creation de bouton pour les menus
        self.play_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, button_path_img, True)
        self.exit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, button_path_img, True)
        self.option_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, button_path_img, True)
        self.back_button = Button(100, 100, button_path_img, True)

        # position
        self.x = 0
        self.y = 0

        # meilleur nom de variable a trouver XD
        self.actual = "menu"

        # affichages
        # hitboxes
        self.show_hitboxes = False
        # position du joueur
        self.show_position = False
        # inventaire
        self.open_inventory = False

        self.right_click = False

        # inventaire
        self.inventory = []

        self.hotbar_num = 1
        self.move = False
        self.position = None

        # sounds
        self.soundManager = SoundManager()
        self.soundManager.play('music', -1)

    def update(self, screen):
        """
        Method qui update l'ecran
        """
        # affichage du background
        self.draw_background(screen)
        self.world.draw(screen)
        self.player.update()
        self.player.inventory_update(screen)
        screen.blit(self.player.hotbar_img, self.player.hotbar_img_rect)
        self.player.hotbar_update(screen)
        # afficher le joueur
        screen.blit(self.player.image, self.player.rect)
        self.set_visible_map()
        self.player.select_hotbar_rect.x = 302 + 53 * (self.hotbar_num - 1)
        self.player.select_hotbar_rect.y = 661
        screen.blit(self.player.select_hotbar, self.player.select_hotbar_rect)

    def update_menu(self, screen):
        """
        Method qui update le menu
        """
        self.play_button.draw(screen)
        self.exit_button.draw(screen)
        self.option_button.draw(screen)
        self.player.draw_text(screen, "Play", (255, 255, 255), self.play_button.rect.centerx - 20,
                              self.play_button.rect.centery - 15)
        self.player.draw_text(screen, "Exit", (255, 255, 255), self.exit_button.rect.centerx - 20,
                              self.exit_button.rect.centery - 15)
        self.player.draw_text(screen, "Options", (255, 255, 255), self.option_button.rect.centerx - 40,
                              self.option_button.rect.centery - 15)

    def update_options(self, screen):
        """
        Method qui update les options
        """
        self.back_button.draw(screen)

    def set_visible_map(self):
        """
        Liste des blocks visible sur l'ecran
        """
        self.visible_map.clear()
        for tile in self.world.tile_list:
            if not (
                    tile.get_rect().x + tile.get_chunk() * 10 * TILE_SIZE + self.world.decalagex > 1080 or tile.get_rect().x + TILE_SIZE + tile.get_chunk() * 10 * TILE_SIZE + self.world.decalagex < 0 or tile.get_rect().y > 720 or tile.get_rect().y + TILE_SIZE < 0):
                self.visible_map.append(tile)

    def draw_background(self, screen):
        """
        Affiche le background
        """
        screen.blit(self.background, (0, 0))
