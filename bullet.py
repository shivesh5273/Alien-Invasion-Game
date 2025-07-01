# Chapter 1 : A ship that firers bullets
# Creating the Bullet Class

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = ai_game.settings.bullet_color

        # Create a bullet rect at (0, 0) and set correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw a glowing plasma bullet on the screen."""
        # Draw the core (white, bright)
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)

        # Draw a semi-transparent glow (blueish plasma)
        glow_rect = self.rect.inflate(6, 10)  # Makes the glow a bit bigger than the core
        glow_surf = pygame.Surface(glow_rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(glow_surf, (50, 150, 255, 80), glow_surf.get_rect())  # RGBA for see-through blue
        self.screen.blit(glow_surf, glow_rect)
