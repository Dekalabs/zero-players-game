import pyxel


class Biome:
    def __init__(self, world, block_size: int):
        self.world = world
        self.block_size = block_size

    def draw(self):
        """Draws the current view of the world."""
        pyxel.cls(12)
        chunk = self.world.chunk()
        for x in range(chunk.shape[0]):
            for y in range(chunk.shape[1]):
                color = self._color(value=chunk[x, y])
                pyxel.rect(
                    y * self.block_size,
                    x * self.block_size,
                    self.block_size,
                    self.block_size,
                    color,
                )

    def _color(self, value: float) -> int:
        """Gets the color for a given value."""
        if value > 0.75:
            return 7
        elif 0.45 < value < 0.75:
            return 4
        elif 0.4 < value < 0.45:
            return 9
        elif 0.35 < value < 0.4:
            return 15
        elif 0.1 < value < 0.35:
            return 3
        return 11
