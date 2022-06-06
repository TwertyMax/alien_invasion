import pygame

class Audio():
    def __init__(self, ai_class):
        self.game_settings = ai_class.game_settings
        self.game_stats = ai_class.game_stats

        self.space_effect = pygame.mixer.Sound("sounds/space.wav")
        self.laser_effect = pygame.mixer.Sound("sounds/laser.wav")

        self.bg_music = "music/bg_music.ogg"

        self._set_start_values()

    def _set_start_values(self):
        self.space_effect.set_volume(self.game_settings.effects_volume)
        self.laser_effect.set_volume(self.game_settings.effects_volume)

    def update_audio(self):
        self._play_regular_sounds()

    def play_background_music(self):
        pygame.mixer.music.load(self.bg_music)
        pygame.mixer.music.set_volume(self.game_settings.music_volume)
        if self.game_stats.game_active:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def play_background_sounds(self):
        if not self.game_stats.game_active:
            self.space_effect.play(-1)
        else:
            self.space_effect.stop()