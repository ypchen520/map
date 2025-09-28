import pygame
import sys

class Task:
    def __init__(self, progress_pos, task_type='small'):
        self.progress_pos = progress_pos # Position on the 0-100 timeline
        self.type = task_type
        self.completed = False

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
        self.target_task = None

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

    # --- Colors for Tasks ---
    TASK_COLOR = (255, 255, 255) # White
    COMPLETED_COLOR = (120, 120, 120) # Gray

    # --- Character Setup ---
    CHARACTER_FRAME_SIZE = (96, 96) # The size of ONE frame
    CHARACTER_LAYOUT = (4, 1)       # 4 columns, 1 row
    CHARACTER_DISPLAY_SIZE = (192, 192)
    player = Character(
        spritesheet_path='sprites/lucky-idle.png',
        start_pos=(50, road_center_y),
        frame_size=CHARACTER_FRAME_SIZE,
        layout=CHARACTER_LAYOUT,
        display_size=CHARACTER_DISPLAY_SIZE
    )

    # A list to store all created tasks
    tasks = []

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # -- NEW: HANDLE MOUSE CLICKS TO CREATE TASKS --
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the click was a left-click and was on the road
                if event.button == 1 and road_rect.collidepoint(event.pos):
                    # Calculate the progress percentage of the click
                    start_margin = 50
                    road_width = SCREEN_WIDTH - (2 * start_margin)
                    click_x = event.pos[0] - start_margin
                    progress_pos = (click_x / road_width) * 100
                    
                    # Ensure progress is within bounds (0-100)
                    progress_pos = max(0, min(100, progress_pos))

                    # Create a new task and add it to our list
                    new_task = Task(progress_pos=progress_pos)
                    tasks.append(new_task)
                    print(f"Created task at {progress_pos:.1f}%")

            # # Check if any key is pressed
            # if event.type == pygame.KEYDOWN:
            #     # Check if the pressed key is the spacebar
            #     if event.key == pygame.K_SPACE:
            #         player.progress += 5  # Increase progress by 5
            #         # Cap the progress at 100 to prevent going off-screen
            #         player.progress = min(player.progress, 100)
            #         print(f"Progress: {player.progress}%")

        # -- NEW: AGENT "BRAIN" LOGIC STARTS HERE --
        
        # 1. If the character has no target, find one.
        if player.target_task is None:
            # Find the first uncompleted task that is ahead of the player
            uncompleted_tasks = [t for t in tasks if not t.completed and t.progress_pos > player.progress]
            if uncompleted_tasks:
                # Sort them by position to find the closest one
                uncompleted_tasks.sort(key=lambda t: t.progress_pos)
                player.target_task = uncompleted_tasks[0]

        # 2. If the character has a target, move towards it.
        if player.target_task is not None:
            # Move forward by a small amount each frame
            player.progress += 0.2 # This is the character's "speed"

            # 3. Check for task completion.
            if player.progress >= player.target_task.progress_pos:
                player.progress = player.target_task.progress_pos # Snap to the task position
                player.target_task.completed = True
                player.target_task = None # Reset target so it can find a new one
                print("Task Completed!")

        # -- AGENT "BRAIN" LOGIC ENDS HERE --

        # Update the character's animation each loop
        player.update_animation()

        # Drawing
        screen.fill(BACKGROUND_COLOR) # Fill the background
        road_rect = pygame.Rect(0, road_center_y - 25, SCREEN_WIDTH, 50)
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # -- NEW: DRAW ALL THE TASKS IN THE LIST --
        # Draw tasks with different colors for completed ones
        start_margin, road_width = 50, SCREEN_WIDTH - 100
        for task in tasks:
            task_x = start_margin + (road_width * (task.progress_pos / 100))
            color = COMPLETED_COLOR if task.completed else TASK_COLOR
            pygame.draw.circle(screen, color, (task_x, road_center_y), 8)
        # start_margin = 50
        # road_width = SCREEN_WIDTH - (2 * start_margin)
        # for task in tasks:
        #     task_x = start_margin + (road_width * (task.progress_pos / 100))
        #     # Draw a white circle for the task
        #     pygame.draw.circle(screen, (255, 255, 255), (task_x, road_center_y), 8)

        # Set character position based on progress
        player.rect.centerx = start_margin + (road_width * (player.progress / 100))
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