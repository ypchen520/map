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
