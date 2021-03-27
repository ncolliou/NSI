import pygame
import random

from Text import Text
from Player import Player
from Sound import SoundManager
from World import World
from Button import Button
from const import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, background_path_img, button_path_img
from aleatoire import generate_map


class Game:
    """
    Class qui initialise le jeu
    (A faire le joueur devrait apparaitre sur le block le plus haut pas dans les airs)
    """

    def __init__(self):
        # import de l arriere plan
        self.background = pygame.image.load(background_path_img)
        # creation du joueur
        self.seed = 40
        # self.seed = random.randint(1, 100)
        # affichage de la seed pour avoir la meme map par exemple
        print(self.seed)
        # initialisation de la map
        # random.randint(1, nbTotalDeMapsPossibleDansLaGenerationCustom), taille de la map
        # self.map = generate_map(63, 500)
        self.map = generate_map(self.seed, 500)
        # initialisation du monde
        self.world = World(self.map, self)

        # creation du monde
        self.world.create_random()
        # dictionnaire qui contient tous les blocks visible sur l'ecran
        self.visible_map = {}

        self.player = Player(self)
        # creation de boutons pour les menus
        self.play_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, button_path_img, True)
        self.exit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, button_path_img, True)
        self.option_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, button_path_img, True)
        self.back_button = Button(SCREEN_WIDTH // 2, 650, button_path_img, True)
        self.control_opt_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, button_path_img, True)
        self.music_opt_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 4, button_path_img, True)
        self.return_game_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100, button_path_img, True)
        self.option_button2 = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, button_path_img, True)
        self.menu_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, button_path_img, True)
        self.return_options_music_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 200, button_path_img, True)

        # position
        self.x = 0
        self.y = 0

        # meilleur nom de variable a trouver
        self.actual = "menu"

        # affichages
        # position du joueur
        self.show_position = False
        # inventaire
        self.open_inventory = False

        # inventaire
        self.inventory = []

        # emplacement du slot selectionne dans la hotbar
        self.hotbar_num = 1

        # sounds
        self.soundManager = SoundManager()
        # self.soundManager.play('music', -1)

        self.user_text = ''

        self.running = True

        self.key_pressed = pygame.key.get_pressed()

        self.volume_back_music = str(self.soundManager.sounds['music'].get_volume())
        self.input_rect = pygame.Rect(100, 100, 50, 30)
        self.color_active = pygame.Color('lightskyblue3')
        self.color_passive = pygame.Color('gray15')
        self.color = self.color_passive
        self.active = False

    def update(self, screen):
        """
        Method qui update l'ecran
        """
        # affichage du background
        self.key_pressed = pygame.key.get_pressed()
        self.draw_background(screen)
        self.world.draw(screen)
        self.player.update(screen)
        self.player.inventory_update(screen)
        screen.blit(self.player.hotbar_img, self.player.hotbar_img_rect)
        self.player.hotbar_update(screen)
        # afficher le joueur
        screen.blit(self.player.image, self.player.rect)
        self.set_visible_map()
        # affichage de l emplacement du slot selectionne
        self.player.select_hotbar_rect.x = 302 + 53 * (self.hotbar_num - 1)
        self.player.select_hotbar_rect.y = 661
        screen.blit(self.player.select_hotbar, self.player.select_hotbar_rect)
        Text(self.user_text, (0, 0, 0), 100, 100).draw(screen)

    def update_menu(self, screen):
        """
        Method qui update le menu
        """
        self.play_button.draw(screen)
        self.exit_button.draw(screen)
        self.option_button.draw(screen)
        Text("Play", (255, 255, 255), self.play_button.rect.centerx - 20,
             self.play_button.rect.centery - 15).draw(screen)
        Text("Exit", (255, 255, 255), self.exit_button.rect.centerx - 20,
             self.exit_button.rect.centery - 15).draw(screen)
        Text("Options", (255, 255, 255), self.option_button.rect.centerx - 40,
             self.option_button.rect.centery - 15).draw(screen)
        # si le bouton play est clicker
        if self.play_button.click():
            self.actual = "playing"
        # si le bouton exit est clicker
        if self.exit_button.click():
            self.running = False
        # si le bouton options est clicker
        if self.option_button.click():
            self.actual = "options"

    def update_options(self, screen):
        """
        Method qui update les options
        """
        self.back_button.draw(screen)
        self.control_opt_button.draw(screen)
        self.music_opt_button.draw(screen)
        Text("Controls", (255, 255, 255), self.control_opt_button.rect.centerx - 20,
             self.control_opt_button.rect.centery - 15).draw(screen)
        Text("Musique", (255, 255, 255), self.music_opt_button.rect.centerx - 20,
             self.music_opt_button.rect.centery - 15).draw(screen)
        Text("Back", (255, 255, 255), self.back_button.rect.centerx - 20,
             self.back_button.rect.centery - 15).draw(screen)

        # si le bouton back est appuyer
        if self.back_button.click():
            self.actual = "menu"
        if self.music_opt_button.click():
            self.actual = "options_musique"

    def update_options_music(self, screen):
        self.return_options_music_button.draw(screen)
        if self.return_options_music_button.click():
            self.actual = "options"
        Text("Back", (255, 255, 255), self.return_options_music_button.rect.centerx - 20,
             self.return_options_music_button.rect.centery - 15).draw(screen)
        pygame.draw.rect(screen, self.color, self.input_rect, 2)
        Text(self.volume_back_music, (255, 255, 255), 100, 100).draw(screen)

    def update_pause(self, screen):
        self.return_game_button.draw(screen)
        self.option_button2.draw(screen)
        self.menu_button.draw(screen)
        Text("Return Game", (255, 255, 255), self.return_game_button.rect.centerx - 60,
             self.return_game_button.rect.centery - 15).draw(screen)
        Text("Options", (255, 255, 255), self.option_button2.rect.centerx - 40,
             self.option_button2.rect.centery - 15).draw(screen)
        Text("Return Menu", (255, 255, 255), self.menu_button.rect.centerx - 60,
             self.menu_button.rect.centery - 15).draw(screen)
        if self.return_game_button.click():
            self.actual = "playing"
        if self.option_button2.click():
            self.actual = "options"
        if self.menu_button.click():
            self.actual = "menu"

    def set_visible_map(self):
        """
        Liste des blocks visible sur l'ecran
        """
        self.visible_map.clear()
        for key, value in self.world.tile_list.items():
            if not (
                    value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.world.decalagex > 1080
                    or
                    value.get_rect().x * TILE_SIZE + TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.world.decalagex < 0
                    or
                    value.get_rect().y * (-TILE_SIZE) + self.world.decalagey > 720
                    or
                    value.get_rect().y * (-TILE_SIZE) + TILE_SIZE + self.world.decalagey < 0):
                self.visible_map[str(key)] = value

    def draw_background(self, screen):
        """
        Affiche le background
        """
        screen.blit(self.background, (0, 0))

    def show_hitboxes(self, screen):
        """
        Affiche les hitboxs
        """
        for value in self.visible_map.values():
            if value.have_hitbox:
                pygame.draw.rect(screen, (255, 255, 255),
                                 (value.get_rect().x * TILE_SIZE + value.get_chunk() * 10 * TILE_SIZE + self.world.decalagex,
                                  value.get_rect().y * (-TILE_SIZE) + self.world.decalagey,
                                  value.get_rect().w,
                                  value.get_rect().h), 2)
        pygame.draw.rect(screen, (255, 255, 255), self.player.rect, 2)

    def key_write(self, event):
        """
        Fonction qui permet d ecrire certaines choses
        """
        if self.active:
            if event.key == pygame.K_BACKSPACE:
                self.volume_back_music = self.volume_back_music[:-1]
            elif event.key == pygame.K_RETURN:
                self.soundManager.set_vol(float(self.volume_back_music), 'music')
            else:
                self.volume_back_music += event.unicode
