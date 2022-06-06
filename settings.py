import screeninfo
import pygame

class GameSettings():
    def __init__(self, ai_class):
        self.ai_class = ai_class

        self.fullscreen = True
        self.vsync = True
        self.screen_width, self.screen_height = self._get_screen_resolution()
        self.window_width, self.window_height = (self.screen_width / 1.25, \
            self.screen_height / 1.25) if not self.fullscreen \
                else (self.screen_width, self.screen_height)
        self.bg_color = (45, 45, 45)

        self.caption = "Alien Invasion!"
        self.icon = pygame.image.load("images/ufo.png")

        self.effects_volume = 0.5
        self.music_volume = 1

        self.bullets_allowed = 3
        self.ship_limit = 3

        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.super_bullets = False
        self.invicible = False

        self.speedup_scale = 1.1
        self.alien_points_scale = 2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.alien_speed = 1
        self.bullet_speed = 3

        self.aliens_points = 50

        self.fleet_direction = 1

    def increase_level(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale

        self.aliens_points *= self.alien_points_scale

        self.ai_class.game_stats.level += 1

    def _get_screen_resolution(self):
        for monitor in screeninfo.get_monitors():
            return (monitor.width, monitor.height)