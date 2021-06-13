import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.game_active = False
        self.settings = Settings()
        self.stats = GameStats(self)

        self.screen = pygame.display.set_mode(
            (0, 0), pygame.FULLSCREEN)

        self.sb = Scoreboard(self)

        self.play_button = Button(self, "play")

        self.settings.screen_height = self.screen.get_rect().height
        self.settings.screen_width = self.screen.get_rect().width
        pygame.display.set_caption('Alien Invasion')

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # make ship
        self.ship = Ship(self)

        self._create_fleet()

    def _create_fleet(self):
        alien = Alien(self)
        scree_width = self.settings.screen_width
        screen_hight = self.settings.screen_height

        alien_width, alien_hight = alien.rect.size

        ship_height = self.ship.rect.height

        available_space_x = scree_width - (alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        available_space_y = screen_hight - (3*alien_hight) - ship_height

        number_rows = available_space_y // (2 * alien_hight)

        for row_number in range(number_rows):
            for aline_number in range(number_aliens_x):
                self._create_alien(aline_number, row_number)

    def _create_alien(self, aline_number, row_number):
        alien = Alien(self)
        alien_width, alien_hight = alien.rect.size
        alien.x = alien_width + 2 * alien_width * aline_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _update_aliens(self):
        self.aliens.update()
        self._check_fleet_edges()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()
    
    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    
    def _check_aliens_bottom(self):
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullets_alien_collisions()

    def _check_bullets_alien_collisions(self):
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collision:
            # self.stats.score += self.settings.alien_point
            for alins in collision.values():
                self.stats.score += self.settings.alien_point * len(alins)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increae_speed()

            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            
    def _check_play_button(self,mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            if self.play_button.rect.collidepoint(mouse_pos):
                self.stats._reset_stats()
                self.sb.prep_score()

                self.game_active = True

                self.aliens.empty()
                self.bullets.empty()

                self._create_fleet()
                self.ship.center_ship()

                pygame.mouse.set_visible(False)


    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
