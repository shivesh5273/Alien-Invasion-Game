# Chapter 1 : A ship that firers bullets
"""In Alien Invasion, the player controls a rocket ship that appears
at the bottom center of the screen. The player can move the ship
right and left using the arrow keys and shoots bullets using the
spacebar. When the game begins, a fleet of aliens fills the sky
and moves across and down the screen. The player shoots and
destroys the aliens. If the player destroys the aliens, a new fleet
appears and that fleet moves faster than the previous fleet. If any alien hits
the player's ship or reaches the bottom of the screen, the player
loses a ship. If the player loses 3 ships, the game ends."""

import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Full Screen
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        # Load and scale the background image
        self.bg_image = pygame.transform.scale(
            pygame.image.load("IMG_5110.JPG"),
            (self.settings.screen_width, self.settings.screen_height)
        )

        # Game stats and sprites
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = True

    def run_game(self):
        """Main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    self._fire_bullet()

    def _check_keydown_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = True
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = True
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.ship.moving_up = True
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        elif event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False
        elif event.key in (pygame.K_UP, pygame.K_w):
            self.ship.moving_up = False
        elif event.key in (pygame.K_DOWN, pygame.K_s):
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Create and fire a new bullet."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update bullet positions and remove off-screen bullets."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        """Check if the fleet is at an edge, update aliens, and check for collisions."""
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _update_screen(self):
        """Draw everything on the screen."""
        self.screen.blit(self.bg_image, (0, 0))
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    # ---- FLEET CREATION LOGIC ----
    def _create_fleet(self):
        """Create a full fleet/grid of aliens (classic style)."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # How many aliens fit horizontally
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # How many rows fit
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                x = alien_width + 2 * alien_width * alien_number
                y = alien_height + 2 * alien_height * row_number
                self._create_alien(x, y)

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ship_left > 0:
            self.stats.ship_left -= 1
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            # ----- FIX: Reset all movement flags -----
            self.ship.moving_left = False
            self.ship.moving_right = False
            self.ship.moving_up = False
            self.ship.moving_down = False
            sleep(0.5)
        else:
            self.game_active = False

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()