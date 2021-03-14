import pygame
from Game import Game
from const import PROJECT_NAME, SCREEN_HEIGHT, SCREEN_WIDTH, FPS, TILE_SIZE

pygame.init()
# creation du clock pour fixer les fps
clock = pygame.time.Clock()

# Création de la fenetre
pygame.display.set_caption(PROJECT_NAME)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# initialisation du jeu
game = Game()

while game.running:
    # si l utilisateur joue
    if game.actual == "playing":
        # update tout
        game.update(screen)
        # si on appuie sur h (hitboxes)
        if game.key_pressed[pygame.K_h]:
            # affichage des hitboxes
            game.show_hitboxes(screen)

        # si on montre la position (F3)
        if game.show_position:
            game.player.draw_text(screen, "X: " + str(int(game.x / TILE_SIZE)), (255, 255, 255), 900, 10)
            game.player.draw_text(screen, "Y: " + str(int(game.y / TILE_SIZE)), (255, 255, 255), 900, 30)

        # si on montre l'inventaire (e)
        if game.open_inventory:
            # le joueur ne peux pas bouger ni casser de blocks
            game.player.dont_play = True
            mouse_pos = pygame.mouse.get_pos()
            # affichage de l'inventaire
            screen.blit(game.player.inventory_img,
                        (SCREEN_WIDTH // 2 - SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 - SCREEN_HEIGHT // 3))
            # update de l'inventaire
            game.player.inventory_update(screen)
        else:
            game.player.dont_play = False

    elif game.actual == "pause":
        game.draw_background(screen)
        game.update_pause(screen)

    elif game.actual == "menu":
        # background du menu
        game.draw_background(screen)
        # affichage des boutons
        game.update_menu(screen)

    elif game.actual == "options":
        # affichage du background
        game.draw_background(screen)
        # affichage des elements dans le menu options
        game.update_options(screen)
    elif game.actual == "options_musique":
        game.draw_background(screen)
        game.update_options_music(screen)

    # mise à jour de l'ecran
    pygame.display.flip()

    # fix des fps
    clock.tick(FPS)

    game.right_click = False

    # events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.input_rect.collidepoint(event.pos):
                if game.active:
                    game.active = False
                    game.color = game.color_passive
                else:
                    game.active = True
                    game.color = game.color_active
        # si une touche est appuyer
        if event.type == pygame.KEYDOWN:
            game.key_write(event)
            # si F3 est appuyer -> on montre la position si elle n'est pas deja afficher
            if event.key == pygame.K_F3 and game.actual == 'playing':
                if game.show_position:
                    game.show_position = False
                else:
                    game.show_position = True
            if event.key == pygame.K_ESCAPE:
                if game.actual == "playing":
                    game.actual = "pause"
                elif game.actual == "pause":
                    game.actual = "playing"
            # si on est entrain de jouer et qu'on ouvre l'inventaire (e)
            if game.actual == "playing":
                if event.key == pygame.K_e:
                    if not game.open_inventory:
                        game.open_inventory = True
                    else:
                        game.open_inventory = False

                if event.key == pygame.K_1 and game.hotbar_num != 1:
                    game.hotbar_num = 1
                elif event.key == pygame.K_2 and game.hotbar_num != 2:
                    game.hotbar_num = 2
                elif event.key == pygame.K_3 and game.hotbar_num != 3:
                    game.hotbar_num = 3
                elif event.key == pygame.K_4 and game.hotbar_num != 4:
                    game.hotbar_num = 4
                elif event.key == pygame.K_5 and game.hotbar_num != 5:
                    game.hotbar_num = 5
                elif event.key == pygame.K_6 and game.hotbar_num != 6:
                    game.hotbar_num = 6
                elif event.key == pygame.K_7 and game.hotbar_num != 7:
                    game.hotbar_num = 7
                elif event.key == pygame.K_8 and game.hotbar_num != 8:
                    game.hotbar_num = 8
                elif event.key == pygame.K_9 and game.hotbar_num != 9:
                    game.hotbar_num = 9

        if game.actual == "playing" and game.open_inventory:
            if event.type == pygame.MOUSEBUTTONUP:
                game.position = pygame.mouse.get_pos()
                if game.player.move_items:
                    game.player.move_items = False
                    # game.player.update_inv(game.player.k, game.player.inventory[game.player.k][0], game.position[0],
                    # game.position[1])
                elif not game.player.move_items:
                    game.player.move_items = True
                    for i in range(0, 9):
                        for j in range(0, 4):
                            if j == 3:
                                if 291 + 14 * i + 39 * i < game.position[0] < 336 + 14 * i + 39 * i and 538 < \
                                        game.position[1] < 583:
                                    print(i, j)
                                    for key, value in game.player.inventory.items():
                                        if value[1] == 294 + 14 * i + 39 * i and value[2] == 538:
                                            while game.player.move_items:
                                                print("test")
                                                game.player.inventory[key][1:] = pygame.mouse.get_pos()
                                                if event.type == pygame.MOUSEBUTTONUP:
                                                    game.player.move_items = False
                            else:
                                if 291 + 14 * i + 39 * i < game.position[0] < 336 + 14 * i + 39 * i and \
                                        363 + 14 * j + 39 * j < game.position[1] < 410 + 14 * j + 39 * j:
                                    print(i, j)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_RIGHT:
                game.right_click = True

        # fermeture de la fenetre
        if event.type == pygame.QUIT:
            game.running = False
            pygame.quit()
