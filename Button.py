import pygame


class Button:
    """
    Class qui initialise un bouton
    """
    def __init__(self, x, y, image_path, center=False):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        if not center:
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect.center = (x, y)
        self.clicked = False

    def draw(self, screen):
        """
        Method qui affiche le bouton sur screen
        """
        screen.blit(self.image, self.rect)

    def click(self):
        """
        Method qui renvoie True si le bouton est clicke
        """
        action = False
        # recuperation de la position de la souris
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            # si le bouton gauche de la souris est appuye mais qu'il n'est pas enfonce
            if pygame.mouse.get_pressed(3)[0] == 1 and not self.clicked:
                self.clicked = True
                action = True
        # si le bouton gauche de la souris n'est pas appuye
        if pygame.mouse.get_pressed(3)[0] == 0:
            self.clicked = False

        return action
