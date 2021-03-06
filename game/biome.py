import operator
import random
from typing import Optional

import pyxel

from game.paths import Path

class Drone:
    def __init__(self):
        self.width = 64
        self.height = 64
        
        self.x = pyxel.screen.width // 2 - self.height // 2
        self.y = pyxel.screen.height // 2 - self.width // 2


    def draw(self):
        """Draws the cloud in the screen."""
        pyxel.blt(self.x, self.y, 1, 0, 0, self.width-1, self.height-1, 7)

class Cloud:
    INCREMENT: int = 6
    WIDTH: int = 135
    HEIGHT: int = 63
    SMALL_CLOUD_POSITION: int = 64

    def __init__(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        axis: Optional[int] = None,
        image_tile: Optional[int]= 0
    ):
        """Initializes the cloud. If there isn't any coordinate provided, the cloud
        is located in a random position.
        """
        self.x = x
        self.y = y
        self.image_tile = image_tile

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
        """Draws the cloud in the screen."""
        pyxel.blt(self.x, self.y, 0, 0, self.image_tile, self.WIDTH, self.HEIGHT, 0)

    def move(self, movement):
        """Move the cloud in the screen."""
        operation = {
            Path.UP: (operator.add, "y"),
            Path.RIGHT: (operator.sub, "x"),
            Path.LEFT: (operator.add, "x"),
            Path.DOWN: (operator.sub, "y"),
        }.get(movement)
        setattr(
            self,
            operation[1],
            operation[0](getattr(self, operation[1]), self.INCREMENT),
        )


class Biome:
    CLOUD_PROBABILITY: float = 0.3

    def __init__(self, world, block_size: int):
        self.world = world
        self.block_size = block_size
        # Generates the cloud in the biome
        self.clouds = self._cloud_generator(random.randint(4, 8))

        self.drone = Drone()

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
            cloud_choice = random.choice([0, Cloud.SMALL_CLOUD_POSITION])
            cloud = Cloud(axis=axis, image_tile=cloud_choice)
            chunk_x = (cloud.x // self.block_size) % chunk.shape[0]
            chunk_y = (cloud.y // self.block_size) % chunk.shape[1]
            height = chunk[chunk_x, chunk_y]
            if random.random() < height:
                clouds.append(cloud)
        return clouds

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

        #Drone
        self.drone.draw()

        # Clouds
        [cloud.draw() for cloud in self.clouds]


    def update(self, movement: int):
        """Updates the biome using the provided movement."""
        for cloud in self.clouds:
            if (
                cloud.x
                > pyxel.width + Cloud.WIDTH | cloud.x
                < 0 | cloud.y
                > pyxel.height + Cloud.HEIGHT | cloud.y
                < 0
            ):
                self.clouds.remove(cloud)
            elif movement:
                cloud.move(movement=movement)
        if movement:
            generate = random.random()
            if generate > self.CLOUD_PROBABILITY:
                size = random.randint(0, 2)
                self.clouds += self._cloud_generator(size=size, axis=movement)
