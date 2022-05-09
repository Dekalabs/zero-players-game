import pyxel


class Biome:
    def __init__(self, world, block_size: int):
        self.world = world
        self.block_size = block_size

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

    def _color(self, value: float) -> int:
        """Gets the color for a given value."""
        if value < -0.4:
            return 5
        elif value < 0:
            return 11
        elif value < 0.4:
            return 3
        return 7
