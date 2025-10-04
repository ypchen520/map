import pygame
import sys
from map.map_utils import generate_random_map, draw_map, TILE_SIZE

class Task:
    def __init__(self, progress_pos, task_type='small'):
        self.progress_pos = progress_pos # Position on the 0-100 timeline
        self.type = task_type
        self.completed = False

class Character:
    # Add a new 'display_size' parameter
    def __init__(self, start_grid_pos, spritesheet_path, frame_size, layout, display_size, speed=0.2):
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
        # self.rect = self.image.get_rect(center=start_pos)
        self.animation_speed_ms = 180
        self.last_update_time = pygame.time.get_ticks()
        self.progress = 0
        self.target_task = None
        self.speed = speed # How fast the character moves
        self.energy = 100  # Start with full energy
        self.max_energy = 100

        # -- FIX 1: Store the initial vertical position --
        # self.y_pos = start_pos[1]

        # -- NEW: Store position in grid coordinates --
        self.grid_x, self.grid_y = start_grid_pos
        
        # We can now calculate the pixel position from the grid position
        start_pixel_pos = (start_grid_pos[0] * TILE_SIZE, start_grid_pos[1] * TILE_SIZE)
        self.rect = self.image.get_rect(center=start_pixel_pos)



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
# -- NEW: Define map dimensions --
MAP_WIDTH = 30 # In tiles
MAP_HEIGHT = 22 # In tiles

SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE
# SCREEN_WIDTH = 1200
# SCREEN_HEIGHT = 900
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Agentic Life Simulation")

# 3. Define colors
BACKGROUND_COLOR = (20, 20, 40) # A dark blue
ROAD_COLOR = (80, 80, 90)       # Gray for the road

# 4. Main game loop
def main():
    # -- NEW: Generate a new map every time the game starts --
    map_data = generate_random_map(MAP_WIDTH, MAP_HEIGHT)
                                   
    # --- Setup ---
    road_center_y = SCREEN_HEIGHT // 2
    road_rect = pygame.Rect(0, road_center_y - 25, SCREEN_WIDTH, 50)

    # --- Energy Bar Colors ---
    ENERGY_BAR_BG = (50, 50, 50)
    ENERGY_BAR_FILL = (60, 200, 60)

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
    CHARACTER_DISPLAY_SIZE = (80, 80)
    # player = Character(
    #     spritesheet_path='sprites/lucky-idle.png',
    #     start_pos=(50, road_center_y),
    #     frame_size=CHARACTER_FRAME_SIZE,
    #     layout=CHARACTER_LAYOUT,
    #     display_size=CHARACTER_DISPLAY_SIZE
    # )

    # characters = []
    # # Create the first character, positioned slightly above the center
    # char1 = Character('sprites/lucky-idle.png', (50, road_center_y - 75), CHARACTER_FRAME_SIZE, CHARACTER_LAYOUT, CHARACTER_DISPLAY_SIZE)
    # # Create the second character, positioned slightly below the center
    # char2 = Character('sprites/lucky-idle.png', (50, road_center_y + 75), CHARACTER_FRAME_SIZE, CHARACTER_LAYOUT, CHARACTER_DISPLAY_SIZE)
    # characters.append(char1)
    # characters.append(char2)

    player = Character(start_grid_pos=(0, 0), spritesheet_path='sprites/lucky-idle.png',
                       frame_size=CHARACTER_FRAME_SIZE, layout=CHARACTER_LAYOUT, 
                       display_size=CHARACTER_DISPLAY_SIZE)

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
                # if event.key == pygame.K_s:
                #     placement_mode = 'small'
                #     print("Placement Mode: SMALL TASK (click to place)")
                # elif event.key == pygame.K_m:
                #     placement_mode = 'milestone'
                #     print("Placement Mode: MILESTONE (click to place)")
                new_x, new_y = player.grid_x, player.grid_y
                if event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1
                elif event.key == pygame.K_LEFT:
                    new_x -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                
                # Collision Check: Before moving, check if the new tile is valid
                if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT and map_data[new_y][new_x] == 0:
                    player.grid_x, player.grid_y = new_x, new_y
        
        player.update_animation()

        # --- Drawing ---
        screen.fill(BACKGROUND_COLOR)
        
        # Draw the randomly generated map
        draw_map(screen, map_data)

        # Update the character's pixel position from its grid position for drawing
        player.rect.centerx = player.grid_x * TILE_SIZE + TILE_SIZE // 2
        player.rect.centery = player.grid_y * TILE_SIZE + TILE_SIZE // 2
        screen.blit(player.image, player.rect)

        pygame.display.flip()

            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     if placement_mode is not None and road_rect.collidepoint(event.pos):
            #         start_margin, road_width = 50, SCREEN_WIDTH - 100
            #         click_x = event.pos[0] - start_margin
            #         progress_pos = max(0, min(100, (click_x / road_width) * 100))
            #         new_task = Task(progress_pos=progress_pos, task_type=placement_mode)
            #         tasks.append(new_task)
            #         print(f"Placed {placement_mode.upper()} at {progress_pos:.1f}%")
            #         placement_mode = None

            # # Check if any key is pressed
            # if event.type == pygame.KEYDOWN:
            #     # Check if the pressed key is the spacebar
            #     if event.key == pygame.K_SPACE:
            #         player.progress += 5  # Increase progress by 5
            #         # Cap the progress at 100 to prevent going off-screen
            #         player.progress = min(player.progress, 100)
            #         print(f"Progress: {player.progress}%")

        # -- Loop through each character for updates --
        # for character in characters:
        #     # --- Agent "Brain" Logic with Energy ---
        #     # 1. If idle, decide whether to work or rest.
        #     if character.target_task is None:
        #         # If energy is low, rest.
        #         if character.energy < character.max_energy:
        #             character.energy += 0.001 # Recovery rate
        #             character.energy = min(character.energy, character.max_energy)
        #         # If energy is high enough, find a task.
        #         if character.energy > 20: # Must have at least 20 energy to start a task
        #             uncompleted_tasks = [t for t in tasks if not t.completed and t.progress_pos > character.progress]
        #             if uncompleted_tasks:
        #                 uncompleted_tasks.sort(key=lambda t: t.progress_pos)
        #                 character.target_task = uncompleted_tasks[0]
            
        #     # 2. If working on a task, move and use energy.
        #     elif character.energy > 0:
        #         character.progress += character.speed
        #         character.energy -= 0.15 # Energy drain rate

        #         # 3. Check for task completion.
        #         if character.progress >= character.target_task.progress_pos:
        #             character.progress = character.target_task.progress_pos
        #             if not character.target_task.completed:
        #                 character.target_task.completed = True
        #                 print("Task Completed!")
        #             character.target_task = None
            
        #     # 4. If out of energy while working, stop.
        #     elif character.energy <= 0:
        #         character.target_task = None # Give up on the task
        #         print("Character is exhausted and stopped working!")

        #     # Update the character's animation each loop
        #     character.update_animation()

        # Drawing
        # screen.fill(BACKGROUND_COLOR)
        # pygame.draw.rect(screen, ROAD_COLOR, road_rect)

        # # -- DRAW TASKS AND MILESTONES DIFFERENTLY --
        # start_margin, road_width = 50, SCREEN_WIDTH - 100
        # for task in tasks:
        #     task_x = start_margin + (road_width * (task.progress_pos / 100))
            
        #     # Use different colors and sizes based on completion and type
        #     if task.completed:
        #         color = COMPLETED_COLOR
        #         radius = MILESTONE_RADIUS if task.type == 'milestone' else TASK_RADIUS
        #     elif task.type == 'milestone':
        #         color = MILESTONE_COLOR
        #         radius = MILESTONE_RADIUS
        #     else:
        #         color = TASK_COLOR
        #         radius = TASK_RADIUS
            
        #     pygame.draw.circle(screen, color, (task_x, road_center_y), radius)

        # # Draw characters and their energy bars
        # for character in characters:
        #     char_x_pos = start_margin + (road_width * (character.progress / 100))
            
        #     # Set the character's rect position
        #     character.rect.centerx = char_x_pos
        #     character.rect.centery = character.y_pos
            
        #     # Draw the character
        #     screen.blit(character.image, character.rect)

        #     # --- DRAW ENERGY BAR (CORRECTED) ---
        #     bar_width, bar_height = 50, 8
            
        #     # -- FIX: Calculate the bar's y-position manually --
        #     # Get the character's known height from our constant
        #     # character_height = CHARACTER_DISPLAY_SIZE[1] 
        #     # character_height = CHARACTER_FRAME_SIZE[1]
        #     # # Calculate the bottom edge: center y + half the height
        #     # character_bottom_edge = character.y_pos + (character_height / 2)
        #     # # Position the bar 5 pixels below that edge
        #     # bar_y = character_bottom_edge + 5
        #     bar_y = character.y_pos + CHARACTER_FRAME_SIZE[1] / 3

        #     # bar_x = char_x_pos - bar_width / 2
        #     bar_x = char_x_pos - bar_width / 8

        #     energy_percentage = character.energy / character.max_energy
        #     fill_width = bar_width * energy_percentage
            
        #     pygame.draw.rect(screen, ENERGY_BAR_BG, (bar_x, bar_y, bar_width, bar_height))
        #     pygame.draw.rect(screen, ENERGY_BAR_FILL, (bar_x, bar_y, fill_width, bar_height))

        # # --- RENDER AND DRAW THE UI TEXT ---
        # if placement_mode:
        #     mode_text = f"Mode: Place {placement_mode.title()}"
        #     text_surface = UI_FONT.render(mode_text, True, TEXT_COLOR)
        #     screen.blit(text_surface, (10, 10))

        # # Update the display
        # pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()