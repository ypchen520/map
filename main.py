import pygame
import sys

class Character:
    # Add a new 'display_size' parameter
    def __init__(self, spritesheet_path, start_pos, frame_size, layout, display_size):
        try:
            self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet: {spritesheet_path}")
            raise SystemExit(e)

        print(f"Successfully loaded '{spritesheet_path}' with dimensions: {self.spritesheet.get_size()}")
        self.spritesheet.set_colorkey((0, 0, 0))
        
        # Pass the new parameter to the load_frames method
        self.frames = self.load_frames(frame_size, layout, display_size)
        
        if not self.frames:
            print("Error: No frames were loaded. Check frame_size and layout.")
            self.frames.append(pygame.Surface(display_size)) 
            self.frames[0].fill((255, 0, 255))

        self.current_frame_index = 0
        self.image = self.frames[self.current_frame_index]
        self.rect = self.image.get_rect(center=start_pos)
        self.animation_speed_ms = 180
        self.last_update_time = pygame.time.get_ticks()
        self.progress = 0

    # The load_frames method also needs to accept 'display_size'
    def load_frames(self, frame_size, layout, display_size):
        frames = []
        frame_width, frame_height = frame_size
        cols, rows = layout
        if frame_width > 0 and frame_height > 0:
            for row in range(rows):
                for col in range(cols):
                    x = col * frame_width
                    y = row * frame_height
                    frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                    frame_surface.blit(self.spritesheet, (0, 0), (x, y, frame_width, frame_height))
                    # --!! THIS IS THE KEY CHANGE !! --
                    # We now scale to the new 'display_size' variable
                    scaled_frame = pygame.transform.scale(frame_surface, display_size)
                    frames.append(scaled_frame)
        return frames

    def update_animation(self):
        # (This method remains unchanged)
        if len(self.frames) > 1:
            now = pygame.time.get_ticks()
            if now - self.last_update_time > self.animation_speed_ms:
                self.last_update_time = now
                self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
                self.image = self.frames[self.current_frame_index]

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
    # Calculate the vertical center of the road
    road_center_y = SCREEN_HEIGHT // 2

    # Example 1: A horizontal strip of 4 frames (128x32 total size)
    CHARACTER_FRAME_SIZE = (96, 96) # The size of ONE frame
    CHARACTER_LAYOUT = (4, 1)       # 4 columns, 1 row

    CHARACTER_DISPLAY_SIZE = (192, 192)

    # Create an instance of our character
    # We place it at x=50 to start, and vertically centered on the road
    player = Character(
        spritesheet_path='sprites/lucky-idle.png',
        start_pos=(50, road_center_y),
        frame_size=CHARACTER_FRAME_SIZE,
        layout=CHARACTER_LAYOUT,
        display_size=CHARACTER_DISPLAY_SIZE
    )

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check if any key is pressed
            if event.type == pygame.KEYDOWN:
                # Check if the pressed key is the spacebar
                if event.key == pygame.K_SPACE:
                    player.progress += 5  # Increase progress by 5
                    # Cap the progress at 100 to prevent going off-screen
                    player.progress = min(player.progress, 100)
                    print(f"Progress: {player.progress}%")

        # Update the character's animation each loop
        player.update_animation()

        # Drawing
        screen.fill(BACKGROUND_COLOR) # Fill the background
        road_rect = pygame.Rect(0, road_center_y - 25, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # -- NEW CODE: DYNAMICALLY SET POSITION BASED ON PROGRESS --
        # Define the margins for the road
        start_margin = 50
        road_width = SCREEN_WIDTH - (2 * start_margin)
        # Calculate the x position
        player.rect.centerx = start_margin + (road_width * (player.progress / 100))
        
        # Keep the y position centered on the road
        player.rect.centery = road_center_y

        # Draw the character at its new position
        screen.blit(player.image, player.rect)

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()