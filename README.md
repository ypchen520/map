# Life Simulation Map

## 🙏 Acknowledgements

The foundation for this game comes from Clear Code's fantastic tutorial: [Creating a Stardew Valley inspired game in Python](https://www.youtube.com/watch?v=T4IX36sP_0c&t=0s).

I'm building on it to create a mini life-sim that turns your TODO list into a game!

## Basics

### Setup

#### `main.py`

- A `Game` class

#### `settings.py`

- Constants

#### `level.py`

Acts as the central controller for a single game level or scene. It's responsible for:
- Managing the main game loop and all updates.
- Loading the map, sprites, and collision objects.
- Controlling the camera and drawing all elements.
- Connecting all game systems (player, soil, weather, etc.).

This self-contained structure makes it easy to add and switch between multiple levels in the future.

### Basic Player

#### `player.py`



## `pygame`

A `Surface` only handles **visuals** (the pixels of an image), while a `Rect` handles **position and collision** (the coordinates and dimensions). They are separate objects for separate jobs.

---
### An Analogy: The Painting and the Frame 🖼️

Think of it this way:

* A **`pygame.Surface`** is the **painting itself**. It's the canvas with all the colors and pixels that make up the image you see. 
* A **`pygame.Rect`** is the **picture frame**. It doesn't contain any art; it just defines the painting's position on the wall, its dimensions, and its boundaries.

You need both. You move the frame to reposition the painting, and you check if two frames are overlapping to see if they're touching.

---
### What a `Surface` Can and Can't Do

A `Surface` is fundamentally a grid of pixels.

#### What it's for:
* **Holding image data**: It stores the actual look of your player, an enemy, or a wall.
* **Drawing**: It's the object you `blit` (draw) onto the screen.

#### What it's missing:
* **Position**: A `Surface` has no built-in concept of its location on the game screen. It doesn't have an `.x` or `.y` coordinate. It's just a free-floating collection of pixels until you tell Pygame where to put it.

---
### Why the `Rect` is Essential

A `Rect` (rectangle) is a simple object that stores numerical data.

#### What it's for:
* **Storing Coordinates**: It holds attributes like `.x`, `.y`, `.topleft`, `.center`, etc., which define its position.
* **Easy Movement**: To move a sprite, you simply change the coordinates of its `Rect` (e.g., `player.rect.x += 5`).
* **Collision Detection**: It has highly optimized methods like `.colliderect()` to instantly check if two objects are overlapping. This is crucial for gameplay and is the primary reason you can't just use a `Surface`.

---
### How They Work Together

The standard Pygame workflow combines their strengths:

1.  **Load Image**: You load your image into a `Surface` (`self.image`).
2.  **Create Frame**: You create a `Rect` from that `Surface` to get its dimensions and give it a starting position (`self.rect = self.image.get_rect()`).
3.  **Update Logic**: In your game loop, you update the position of the `Rect` (`self.rect.y += 1`).
4.  **Draw Visuals**: You tell Pygame to draw the `Surface` at the `Rect`'s current position (`screen.blit(self.image, self.rect)`).