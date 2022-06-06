from email.mime import image
import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, ai_class):
        super().__init__()

        self.screen = ai_class.screen
        self.screen_rect = ai_class.screen.get_rect()
        self.game_settings = ai_class.game_settings
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        if self.rect.right >= self.screen_rect.right or self.rect.left <= self.screen_rect.left:
            return True

    def _move_alien(self):
        self.x += (self.game_settings.alien_speed * self.game_settings.fleet_direction)
        self.rect.x = self.x

    def update(self):
        self._move_alien()