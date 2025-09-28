import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# 2. Set up the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agentic Life Simulation")

# 3. Define colors
BACKGROUND_COLOR = (20, 20, 40) # A dark blue
ROAD_COLOR = (80, 80, 90)       # Gray for the road

# 4. Main game loop
def main():
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Drawing
        screen.fill(BACKGROUND_COLOR) # Fill the background

        # Draw the road rectangle in the middle of the screen
        road_y_position = SCREEN_HEIGHT // 2 - 25
        road_rect = pygame.Rect(0, road_y_position, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()