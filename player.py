import pygame
from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) # Add this sprite to the specified group(s)

        self.image = pygame.Surface((32, 64)) # placeholder
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos) # creates the invisible rectangular box (pygame.Rect) that Pygame uses to handle positioning, movement, and collision detection for your visible image.

    def input(self):
        # when to call the input() method? updating this player via update() called in the Spite group in the Level instance
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            print('up')
        elif keys[pygame.K_DOWN]:
            print('down')
        
        if keys[pygame.K_RIGHT]:
            print('right')
        elif keys[pygame.K_LEFT]:
            print('left')
    
    def update(self, dt):
        # potentially using *args instead of dt
        self.input()