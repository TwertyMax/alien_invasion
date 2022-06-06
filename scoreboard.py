import pygame

from ship import *

from game_ui import *

class Scoreboard():
    def __init__(self, ai_class):
        self.ai_class = ai_class
        self.screen = ai_class.screen
        self.game_stats = ai_class.game_stats

        self._set_scoreboard()

    def _set_scoreboard(self):
        self.score_text = Text(self.ai_class, str(self.game_stats.score), (255, 255, 255), None, 28, 0, 0)
        self.score_text.text_image_rect.right = self.score_text.screen_rect.right - 200
        self.score_text.text_image_rect.top = 20

        rounded_high_score = round(self.game_stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_text = Text(self.ai_class, f"Record: {high_score_str}", (255, 255, 255), None, 28, 0, 0)
        self.high_score_text.text_image_rect.midtop = self.high_score_text.screen_rect.midtop
        self.high_score_text.text_image_rect.top = 20

        self.level_text = Text(self.ai_class, f"Level: {self.game_stats.level}", (255, 255, 255), None, 28, 0, 0)
        self.level_text.text_image_rect.left = self.level_text.screen_rect.left + 200
        self.level_text.text_image_rect.top = 20

        self.ships = pygame.sprite.Group()
        self.update_ships()

    def update_high_score(self):
        rounded_high_score = round(self.game_stats.high_score, -1)
        high_score_str = "{:,}".format(rounded_high_score)
        self.high_score_text.update_text(f"Record: {high_score_str}")

    def update_score(self):
        if self.game_stats.game_active:
            rounded_score = round(self.game_stats.score, -1)
            score_str = "{:,}".format(rounded_score)
            self.score_text.update_text(f"Score: {score_str}")
            self.score_text.draw_text()
            self.high_score_text.draw_text()
            self.ships.draw(self.screen)

    def update_level(self):
        if self.game_stats.game_active:
            self.level_text.update_text(f"Level: {self.game_stats.level}")
            self.level_text.draw_text()

    def update_ships(self):
        self.ships.empty()
        for ship_number in range(self.game_stats.ships_left):
            ship = PlayerShip(self.ai_class)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 20
            self.ships.add(ship)