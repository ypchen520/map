import pygame
from settings import * 

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) # Add this sprite to the specified group(s)

        # general setup
        self.image = pygame.Surface((32, 64)) # placeholder
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos) # creates the invisible rectangular box (pygame.Rect) that Pygame uses to handle positioning, movement, and collision detection for your visible image.

        # movement attributes
        self.direction = pygame.math.Vector2() # default: (0,0)
        self.pos = pygame.math.Vector2(self.rect.center) # we'll need to update the self.rect in the end
        self.speed = 200

    def input(self):
        # when to call the input() method? updating this player via update() called in the Spite group in the Level instance
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, dt):
        # fix: moving diagonally is faster
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # to implement collision mechanics, we need to separate horizontal and vertical movements

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y   
    
    def update(self, dt):
        # potentially using *args instead of dt
        self.input()
        self.move(dt)