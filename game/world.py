from typing import Optional, Tuple

import numpy as np
import opensimplex

opensimplex.seed(42)


class World:
    """Class that represents the generation of the world."""

    SPEED: int = 3
    SCALE: int = 10

    def __init__(self, width: int, height: int, speed: Optional[int] = None):
        """Initializes the tile with the width and height given for the chunk."""
        self.width: int = width
        self.height: int = height
        self.speed: int = speed if speed is not None else self.SPEED
        self.position: Tuple[int, int] = (0, 0)  # Initial global position
        self.tile: "np.ndarray" = self._generate_tile(
            width * 3, height * 3
        )  # Generates a tile with the current chunk and the nearest chunks

    def _generate_tile(self, width: int, height: int) -> "np.ndarray":
        """Generates a complete tile."""
        tile = np.empty((width, height))
        for x in range(width):
            for y in range(height):
                tile[x, y] = opensimplex.noise2(x / self.SCALE, y / self.SCALE)
        return tile

    def chunk(self) -> "np.ndarray":
        """Gets the central chunk."""
        return self.tile[self.width : -self.width, self.height : -self.height]

    def move_left(self) -> None:
        """Moves the tiles to the left."""
        chunk = np.empty((self.SPEED, self.tile.shape[1]))
        for i in range(chunk.shape[0]):
            for j in range(chunk.shape[1]):
                chunk[i, j] = opensimplex.noise2(
                    (self.position[0] - self.SPEED + i) / self.SCALE, j / self.SCALE
                )
        self.position = (self.position[0] - self.SPEED, self.position[1])
        self.tile = np.concatenate((chunk, self.tile))[: -self.SPEED]

    def move_right(self) -> None:
        """Moves the tiles to the right."""
        chunk = np.empty((self.SPEED, self.tile.shape[1]))
        for i in range(chunk.shape[0]):
            for j in range(chunk.shape[1]):
                chunk[i, j] = opensimplex.noise2(
                    (self.position[0] + self.SPEED + i) / self.SCALE, j / self.SCALE
                )
        self.position = (self.position[0] + self.SPEED, self.position[1])
        self.tile = np.concatenate((self.tile, chunk))[self.SPEED :]

    def move_up(self) -> None:
        """Moves the tiles to the up."""
        chunk = np.empty((self.tile.shape[0], self.SPEED))
        for i in range(chunk.shape[0]):
            for j in range(chunk.shape[1]):
                chunk[i, j] = opensimplex.noise2(
                    i / self.SCALE, (self.position[1] - self.SPEED + j) / self.SCALE
                )

        self.position = (self.position[0], self.position[1] - self.SPEED)
        self.tile = np.concatenate((chunk, self.tile), axis=1)[:, : -self.SPEED]

    def move_down(self) -> None:
        """Moves the tiles to the down."""
        chunk = np.empty((self.tile.shape[0], self.SPEED))
        for i in range(chunk.shape[0]):
            for j in range(chunk.shape[1]):
                chunk[i, j] = opensimplex.noise2(
                    i / self.SCALE, (self.position[1] + self.SPEED + j) / self.SCALE
                )
        self.position = (self.position[0], self.position[1] + self.SPEED)
        self.tile = np.concatenate((self.tile, chunk), axis=1)[:, self.SPEED :]
