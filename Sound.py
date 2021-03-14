import pygame


class SoundManager:
    def __init__(self):
        self.sounds = {
            'music': pygame.mixer.Sound('assets/music/c418-sweden.mp3')
        }

    def play(self, name, loop=1):
        self.sounds[name].play(loop)

    def set_vol(self, vol, key):
        self.sounds[key].set_volume(vol)
