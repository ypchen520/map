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
    # --- Setup ---
    road_center_y = SCREEN_HEIGHT // 2
    road_rect = pygame.Rect(0, road_center_y - 25, SCREEN_WIDTH, 50)

    # --- FONT AND TEXT SETUP ---
    UI_FONT = pygame.font.Font(None, 32) # Use Pygame's default font, size 32
    TEXT_COLOR = (220, 220, 220)         # A light gray for the text

    # --- Define colors and sizes for different task types ---
    TASK_COLOR = (255, 255, 255)         # White
    MILESTONE_COLOR = (255, 215, 0)      # Gold
    COMPLETED_COLOR = (120, 120, 120)    # Gray
    TASK_RADIUS = 8
    MILESTONE_RADIUS = 12

    # --- Character Setup ---
    CHARACTER_FRAME_SIZE = (96, 96) # The size of ONE frame
    CHARACTER_LAYOUT = (4, 1)       # 4 columns, 1 row
    CHARACTER_DISPLAY_SIZE = (192, 192)
    # player = Character(
    #     spritesheet_path='sprites/lucky-idle.png',
    #     start_pos=(50, road_center_y),
    #     frame_size=CHARACTER_FRAME_SIZE,
    #     layout=CHARACTER_LAYOUT,
    #     display_size=CHARACTER_DISPLAY_SIZE
    # )

    characters = []
    # Create the first character, positioned slightly above the center
    char1 = Character('sprites/lucky-idle.png', (50, road_center_y - 15), CHARACTER_FRAME_SIZE, CHARACTER_LAYOUT, CHARACTER_DISPLAY_SIZE)
    # Create the second character, positioned slightly below the center
    char2 = Character('sprites/lucky-idle.png', (50, road_center_y + 15), CHARACTER_FRAME_SIZE, CHARACTER_LAYOUT, CHARACTER_DISPLAY_SIZE)
    characters.append(char1)
    characters.append(char2)

    # A list to store all created tasks
    tasks = []

    placement_mode = None

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    placement_mode = 'small'
                    print("Placement Mode: SMALL TASK (click to place)")
                elif event.key == pygame.K_m:
                    placement_mode = 'milestone'
                    print("Placement Mode: MILESTONE (click to place)")

            if event.type == pygame.MOUSEBUTTONDOWN:
                if placement_mode is not None and road_rect.collidepoint(event.pos):
                    start_margin, road_width = 50, SCREEN_WIDTH - 100
                    click_x = event.pos[0] - start_margin
                    progress_pos = max(0, min(100, (click_x / road_width) * 100))
                    new_task = Task(progress_pos=progress_pos, task_type=placement_mode)
                    tasks.append(new_task)
                    print(f"Placed {placement_mode.upper()} at {progress_pos:.1f}%")
                    placement_mode = None

            # # Check if any key is pressed
            # if event.type == pygame.KEYDOWN:
            #     # Check if the pressed key is the spacebar
            #     if event.key == pygame.K_SPACE:
            #         player.progress += 5  # Increase progress by 5
            #         # Cap the progress at 100 to prevent going off-screen
            #         player.progress = min(player.progress, 100)
            #         print(f"Progress: {player.progress}%")

        # -- Loop through each character for updates --
        for character in characters:
            # -- AGENT "BRAIN" LOGIC STARTS HERE --
        
            # 1. If the character has no target, find one.
            if character.target_task is None:
                uncompleted_tasks = [t for t in tasks if not t.completed and t.progress_pos > character.progress]
                if uncompleted_tasks:
                    uncompleted_tasks.sort(key=lambda t: t.progress_pos)
                    character.target_task = uncompleted_tasks[0]
            
            if character.target_task is not None:
                character.progress += 0.2
                if character.progress >= character.target_task.progress_pos:
                    character.progress = character.target_task.progress_pos
                    # Only the first character to arrive completes the task
                    if not character.target_task.completed:
                        character.target_task.completed = True
                        print("Task Completed!")
                    character.target_task = None

            # -- AGENT "BRAIN" LOGIC ENDS HERE --

            # Update the character's animation each loop
            character.update_animation()

        # Drawing
        screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # -- DRAW TASKS AND MILESTONES DIFFERENTLY --
        start_margin, road_width = 50, SCREEN_WIDTH - 100
        for task in tasks:
            task_x = start_margin + (road_width * (task.progress_pos / 100))
            
            # Use different colors and sizes based on completion and type
            if task.completed:
                color = COMPLETED_COLOR
                radius = MILESTONE_RADIUS if task.type == 'milestone' else TASK_RADIUS
            elif task.type == 'milestone':
                color = MILESTONE_COLOR
                radius = MILESTONE_RADIUS
            else:
                color = TASK_COLOR
                radius = TASK_RADIUS
            
            pygame.draw.circle(screen, color, (task_x, road_center_y), radius)

        # -- UPDATED: Loop through each character to draw it --
        for character in characters:
            character.rect.centerx = start_margin + (road_width * (character.progress / 100))
            screen.blit(character.image, character.rect)

        # --- RENDER AND DRAW THE UI TEXT ---
        if placement_mode:
            mode_text = f"Mode: Place {placement_mode.title()}"
            text_surface = UI_FONT.render(mode_text, True, TEXT_COLOR)
            screen.blit(text_surface, (10, 10))

        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()