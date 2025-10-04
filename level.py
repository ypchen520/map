import pygame
from settings import *
from player import Player

class Level:
    def __init__(self):
        # gets a reference to the main game window, so it knows where to draw things.
        self.display_surface = pygame.display.get_surface()

        # creates a container to hold and manage all the game objects (like the player, enemies, and items).
        self.all_sprites = pygame.sprite.Group()

        self.setup()

    def setup(self):
        self.player = Player(pos=(640, 360), group=self.all_sprites)

    def run(self, dt):
        """
        Updates and draws all sprites for a single game frame.

        Args:
            dt (float): Delta time. The time elapsed since the last frame,
                        used for frame-rate independent updates.
        """
        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface) # draws every game object in the all_sprites group onto the screen.
        
        # Calls the update() method on every sprite in the group, running their individual logic for the frame (e.g., move, animate, check for input).
        self.all_sprites.update(dt)
