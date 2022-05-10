import random
from typing import Optional

import pyxel

import operator

from game.paths import Path


class Cloud:
    INCREMENT: int = 6
    WIDTH: int = 135
    HEIGHT: int = 63

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        axis: Optional[int] = None,
    ):
        self.x = x
        self.y = y

        if x is None:
            if axis == Path.LEFT:
                self.x = -self.WIDTH + random.randint(-self.WIDTH // 3, 0)
            elif axis == Path.RIGHT:
                self.x = pyxel.width + random.randint(0, self.WIDTH // 3)
            else:
                self.x = random.randint(0, pyxel.width)

        if y is None:
            if axis == Path.UP:
                self.y = -self.HEIGHT + random.randint(-self.HEIGHT // 3, 0)
            elif axis == Path.DOWN:
                self.y = pyxel.height + random.randint(0, self.HEIGHT // 3)
            else:
                self.y = random.randint(0, pyxel.height)

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.WIDTH, self.HEIGHT, 0)

    def move(self, movement):
        operation = {
            Path.UP: (operator.add, "y"),
            Path.RIGHT: (operator.sub, "x"),
            Path.LEFT: (operator.add, "x"),
            Path.DOWN: (operator.sub, "y"),
        }.get(movement)

        setattr(self, operation[1], operation[0](getattr(self, operation[1]), self.INCREMENT))

class Biome:
    CLOUD_PROBABILITY: float = 0.3

    def __init__(self, world, block_size: int):
        self.world = world
        self.block_size = block_size
        self.clouds = self._cloud_generator(random.randint(4, 8))

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
        # Clouds
        [cloud.draw() for cloud in self.clouds]

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

    def _cloud_generator(self, size: int, axis: Optional[int] = None):
        clouds = []
        chunk = self.world.chunk()
        for _ in range(random.randint(size - 2, size + 2)):
            cloud = Cloud(axis=axis)  

            chunk_x = cloud.x // self.block_size
            if chunk_x >= len(chunk):
                chunk_x = len(chunk)-1

            chunk_y = cloud.y // self.block_size
            if (chunk_y >= len(chunk[0])):
                chunk_y = len(chunk[0])-1

            height = chunk[chunk_x, chunk_y ]
            if height > 0.6:
                clouds.append(cloud)      

        return clouds

    def update(self, movement: int):
        for cloud in self.clouds:
            if cloud.x > pyxel.width+Cloud.WIDTH | cloud.x < 0 | cloud.y > pyxel.height+Cloud.HEIGHT | cloud.y < 0:
                self.clouds.remove(cloud)
            elif movement:
                cloud.move(movement=movement)

        if movement:
            generate = random.random()
            if generate > self.CLOUD_PROBABILITY:
                size = random.randint(0, 2)
                self.clouds += self._cloud_generator(size=size, axis=movement)
