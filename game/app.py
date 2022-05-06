import pyxel
import random

from game.world import World


class App:
    """Default pyxel app."""

    def __init__(self, screen_width: int, screen_height: int, block_size: int) -> None:
        # Save initial data
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.block_size = block_size

        self.direction = 0

        # Creates the world
        self.world = World(
            self.screen_width // self.block_size, self.screen_height // self.block_size
        )

        # Launch pyxel
        pyxel.init(self.screen_width, self.screen_height, title="Zero Players Game")
        pyxel.playm(0, loop=True)
        pyxel.run(self.update_world, self.draw_world)

    def _color(self, value: float) -> int:
        """Gets the color for a given value."""
        if value < 0.3:
            return 5
        elif value < 0.5:
            return 11
        elif value < 0.8:
            return 3
        return 7

    def _step(self) -> None:
        """Make the movement."""
        change_direction = random.random()
        
        if change_direction > 0.98:
            self.direction = random.randint(0,3)

        if self.direction == 0:
            self.world.move_up()
        elif self.direction == 1:
            self.world.move_down()
        elif self.direction == 2: 
            self.world.move_left()
        else:
            self.world.move_right()

    def update_world(self):
        """Updates the status of the world."""
        # Handles the quit event.
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Movement
        self._step()

    def draw_world(self):
        """Draws the current view of the world."""
        pyxel.cls(12)
        chunk = self.world.chunk()
        for x in range(chunk.shape[0]):
            for y in range(chunk.shape[1]):
                color = self._color(value=chunk[x, y])
                pyxel.rect(
                    x * self.block_size,
                    y * self.block_size,
                    self.block_size,
                    self.block_size,
                    color,
                )
