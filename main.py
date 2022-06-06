import sys
import time

import pygame

from settings import *
from ship import *
from bullet import *
from alien import *
from game_stats import *
from game_ui import *
from scoreboard import *
from audio import *

class AlienInvasion():
    def __init__(self):
        self.game_settings = GameSettings(self)
        pygame.init()
        pygame.display.set_caption(self.game_settings.caption)
        pygame.display.set_icon(self.game_settings.icon)
        self.screen = pygame.display.set_mode((\
            self.game_settings.window_width, \
                self.game_settings.window_height), \
                    self.game_settings.fullscreen, self.game_settings.vsync)
        self.screen_rect = self.screen.get_rect()
        self.game_stats = GameStats(self)
        self.player_ship = PlayerShip(self)
        self.scoreboard = Scoreboard(self)
        self.audio = Audio(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._set_start_menu()

    def _set_start_menu(self):
        self.play_button = Button(self, "Play", y=400)
        self.quit_button = Button(self, "Quit", y=512)
        self.menu_text = Text(self, "Menu", color=(255, 0, 0), y=200)
        self.audio.play_background_sounds()

    def _key_down_events(self, event):
        match event.key:
            case pygame.K_q:
                sys.exit()
            case pygame.K_p:
                self._new_game()
            case pygame.K_LEFT:
                self.player_ship.is_moving_left = True
            case pygame.K_RIGHT:
                self.player_ship.is_moving_right = True

    def _key_up_events(self, event):
        match event.key:
            case pygame.K_LEFT:
                self.player_ship.is_moving_left = False
            case pygame.K_RIGHT:
                self.player_ship.is_moving_right = False
            case pygame.K_SPACE:
                if len(self.bullets) < self.game_settings.bullets_allowed:
                    self._fire_bullet()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                self._key_down_events(event)
            if event.type == pygame.KEYUP:
                self._key_up_events(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_buttons(mouse_pos)
    
    def _check_buttons(self, mouse_pos):
        play_button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        quit_button_clicked = self.quit_button.rect.collidepoint(mouse_pos)
        if play_button_clicked and not self.game_stats.game_active:
            self._new_game()
        if quit_button_clicked and not self.game_stats.game_active:
            sys.exit()

    def _check_collisions(self):
        bullet_alien_collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True if not self.game_settings.super_bullets else False, True)
        if bullet_alien_collisions:
            for alien in bullet_alien_collisions.values():
                self.game_stats.score += self.game_settings.aliens_points * len(alien)
        if pygame.sprite.spritecollideany(self.player_ship, self.aliens):
            self._ship_lose()

    def _check_fleet(self):
        if not self.aliens:
            self.bullets.empty()
            self.game_settings.increase_level()
            self._create_fleet()

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen_rect.bottom:
                self._ship_lose()
                break

    def _ship_lose(self):
        if self.game_stats.ships_left > 0:
            if not self.game_settings.invicible:
                self.game_stats.ships_left -= 1
                self.scoreboard.update_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.player_ship.center_ship()
            time.sleep(0.5)
        else:
            self.game_stats.game_active = False
            self.audio.play_background_music()
            self.audio.play_background_sounds()
            self.game_stats.check_high_score()

    def _set_cursor(self):
        pygame.mouse.set_visible(not self.game_stats.game_active)

    def _new_game(self):
        self.game_stats.reset_stats()
        self.game_stats.game_active = True
        self.aliens.empty()
        self.bullets.empty()
        self.game_settings.initialize_dynamic_settings()
        self._create_fleet()
        self.player_ship.center_ship()
        self.scoreboard.update_ships()
        self.audio.play_background_sounds()
        self.audio.play_background_music()

    def _display_frame(self):
        pygame.display.flip()

    def _fill_screen(self):
        self.screen.fill(self.game_settings.bg_color)

    def _draw_fleet(self):
        self.aliens.draw(self.screen)

    def _draw_buttons(self):
        if not self.game_stats.game_active:
            self.play_button.draw_button()
            self.quit_button.draw_button()

    def _draw_text(self):
        if not self.game_stats.game_active:
            self.menu_text.draw_text()

    def _update_objects(self):
        self.player_ship.update_ship()
        self._update_fleet()
        self._update_bullets()

    def _update_fleet(self):
        self._draw_fleet()
        self._check_fleet_edges()
        self._check_aliens_bottom()
        self.aliens.update()

    def _update_game(self):
        self._check_events()
        self._fill_screen()
        if self.game_stats.game_active:
            self._update_objects()
            self._check_collisions()
            self._check_fleet()
        self._draw_buttons()
        self._draw_text()
        self.scoreboard.update_score()
        self._set_cursor()

    def _update_bullets(self):
        self.bullets.update()
        self._draw_all_bullets()
        self._clear_bullet()

    def _draw_all_bullets(self):
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

    def _clear_bullet(self):
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < self.screen.get_rect().top:
                self.bullets.remove(bullet)

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)
        self.audio.laser_effect.play()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break;

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.game_settings.fleet_drop_speed
        self.game_settings.fleet_direction *= -1

    def _create_fleet(self):
        number_aliens_x, rows_count = self._get_avaliable_space()
        for row_number in range(rows_count):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.y = alien_height + 2 * alien_height * row_number
        alien.rect.x = alien.x
        self.aliens.add(alien)

    def _get_avaliable_space(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        ship_height = self.player_ship.rect.height
        avaliable_space_x = self.game_settings.window_width - \
            (2 * alien_width)
        avaliable_space_y = self.game_settings.window_height - \
            (3 * alien_height) - ship_height
        number_aliens_x = int(avaliable_space_x // (2 * alien_width))
        rows_count = int(avaliable_space_y // (2 * alien_height))
        return (number_aliens_x, rows_count)

    def update(self):
        while True:
            self._update_game()
            self._display_frame()

def main():
    alien_invasion = AlienInvasion()
    alien_invasion.update()

if __name__ == "__main__":
    main()