import pygame
import random

# --- Tile Properties ---
TILE_SIZE = 40
GRASS_COLOR = (50, 150, 50)
ROCK_COLOR = (130, 130, 130)

# -- NEW: Random Map Generation Function --
def generate_random_map(width, height, obstacle_chance=0.25):
    """
    Generates a 2D list representing a map with random obstacles.
    'obstacle_chance' is the probability (0.0 to 1.0) of a tile being a rock.
    """
    grid = []
    for row in range(height):
        grid.append([])
        for col in range(width):
            if random.random() < obstacle_chance:
                grid[row].append(1) # 1 = Rock
            else:
                grid[row].append(0) # 0 = Grass
    
    # Ensure the top-left corner is always clear for the player to start
    grid[0][0] = 0
    return grid

def draw_map(screen, map_data):
    """
    Draws the map grid onto the screen.
    """
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
            
            color = GRASS_COLOR if tile == 0 else ROCK_COLOR
            pygame.draw.rect(screen, color, rect)