import pyxel

from game.biome import Biome
from game.paths import Path
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
            rows=self.screen_height // self.block_size,
            columns=self.screen_width // self.block_size,
        )
        # Creates the Biome
        self.biome = Biome(self.world, self.block_size)
        self.path = Path()
        # Launch pyxel
        pyxel.init(self.screen_width, self.screen_height, title="Zero Players Game")
        pyxel.playm(0, loop=True)
        pyxel.load("../assets/resources.pyxres")
        pyxel.run(self.update_world, self.biome.draw_world)

    def _step(self) -> None:
        """Make the movement."""
        movement = self.path.direction()
        movements = {
            Path.UP: self.world.move_up,
            Path.RIGHT: self.world.move_right,
            Path.LEFT: self.world.move_left,
            Path.DOWN: self.world.move_down,
        }
        movements.get(movement, lambda: ...)()

    def update_world(self):
        """Updates the status of the world."""
        # Handles the quit event
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        # Movement
        self._step()
        # Music
        self.music_controls()

    def music_controls(self):
        if pyxel.btnp(pyxel.KEY_M):
            pyxel.playm(0, loop=True)
        if pyxel.btnp(pyxel.KEY_Z):
            pyxel.stop()
