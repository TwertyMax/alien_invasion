import os

class GameStats():
    def __init__(self, ai_class):
        self.ai_class = ai_class
        self.game_settings = ai_class.game_settings

        self.game_active = False

        self.high_score = 0

        self.reset_stats()

        self._check_high_score_save()

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self._save_high_score()
            self.ai_class.scoreboard.update_high_score()

    def _check_high_score_save(self):
        if os.path.exists("record.txt"):
            self._get_high_score()
        else:
            self._save_high_score()

    def _save_high_score(self):
        with open("record.txt", "w") as f:
            f.write(str(self.high_score))

    def _get_high_score(self):
        with open("record.txt", "r") as f:
            self.high_score = int(f.readline())

    def reset_stats(self):
        self.ships_left = self.game_settings.ship_limit
        self.score = 0
        self.level = 1