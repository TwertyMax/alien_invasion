import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, ai_class):
        super().__init__()

        self.screen = ai_class.screen
        self.game_settings = ai_class.game_settings

        self.bullet_width = 3 if not self.game_settings.super_bullets else self.game_settings.window_width
        self.bullet_height = 15
        self.bullet_color = (255, 230, 0)

        self.rect = pygame.Rect(0, 0, self.bullet_width, self.bullet_height)
        self.rect.midtop = ai_class.player_ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        self._move_bullet()

    def _move_bullet(self):
        self.y -= self.game_settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.bullet_color, self.rect)