import pygame
from settings import * 
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group) # Add this sprite to the specified group(s)

        self.import_assets() # Needs to be at the top
        
        # For creating images using the imported assets (as Surfaces)
        self.status = 'down_idle'
        self.frame_index = 0 # for animation

        # general setup
        # self.image = pygame.Surface((32, 64)) # placeholder
        self.image = self.animations[self.status][self.frame_index]
        self.image.fill('green')
        self.rect = self.image.get_rect(center=pos) # creates the invisible rectangular box (pygame.Rect) that Pygame uses to handle positioning, movement, and collision detection for your visible image.

        # movement attributes
        self.direction = pygame.math.Vector2() # default: (0,0)
        self.pos = pygame.math.Vector2(self.rect.center) # we'll need to update the self.rect in the end
        self.speed = 200
    
    def import_assets(self):
        # Character animations: a dict with keys mapping to a list of Surfaces
        # TODO: Use a diffusion model to generate variant characters with matching animations
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
            'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
            'right_water': [], 'left_water': [], 'up_water': [], 'down_water': [],
        }

        for animation in self.animations.keys():
            full_path = './graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self, dt):
        self.frame_index += 4 * dt # 4 decides the speed of the animation
        # if self.frame_index >= len(self.animations[self.status]):
        #     self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index % len(self.animations[self.status]))]

    def input(self):
        # when to call the input() method? updating this player via update() called in the Spite group in the Level instance
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = 'up'
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = 'down'
        else:
            self.direction.y = 0
        
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = 'left'
        else:
            self.direction.x = 0

    def get_status(self):
        # idle: if the player is not moving, add _idle to the status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        
        # tool use

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
        self.get_status()
        self.move(dt)