import pygame

class PlayerShip(pygame.sprite.Sprite):
    def __init__(self, ai_class):
        super().__init__()

        self.screen = ai_class.screen
        self.screen_rect = ai_class.screen.get_rect()
        self.game_settings = ai_class.game_settings
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        self.x = float(self.rect.x)
        self.is_moving_right = False
        self.is_moving_left = False
        self.can_move_right = True
        self.can_move_left = True

    def _display_ship(self):
        self.screen.blit(self.image, self.rect)

    def update_ship(self):
        self._display_ship()
        self._check_edges()
        self._move_ship()

    def _check_edges(self):
        self.can_move_right = self.rect.right < self.screen_rect.right
        self.can_move_left = self.rect.left > self.screen_rect.left

    def _move_ship(self):
        if self.is_moving_left and self.can_move_left:
            self.x -= self.game_settings.ship_speed
        if self.is_moving_right and self.can_move_right:
            self.x += self.game_settings.ship_speed

        self.rect.x = self.x

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)