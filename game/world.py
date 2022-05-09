from typing import Optional, Tuple

import numpy as np
import opensimplex

opensimplex.seed(42)


class World:
    """Class that represents the generation of the world."""

    INCREMENT: int = 1
    SCALE: int = 30
    BUFFER: int = 1

    def __init__(self, columns: int, rows: int, increment: Optional[int] = None):
        """Initializes the tile with the width and height given for the chunk.

        :columns: number of columns in the world, the width of the screen.
        :rows: number of rows in the world, the width of the screen.
        """
        self.position: Tuple[int, int] = (0, 0)  # Initial global position
        self.increment: int = increment if increment is not None else self.INCREMENT
        self.tile: "np.ndarray" = self._generate_tile(
            shape=(columns * self.BUFFER, rows * self.BUFFER)
        )  # Generates a tile with the current chunk and the nearest chunks

    def _generate_tile(self, shape: Tuple[int, int]) -> "np.ndarray":
        """Generates a complete tile."""
        tile = opensimplex.noise2array(
            np.arange(shape[0]) / self.SCALE, np.arange(shape[1]) / self.SCALE
        )
        self.position = (shape[0] - 1, shape[1] - 1)
        print(tile.shape)
        return tile

    def chunk(self) -> "np.ndarray":
        """Gets the central chunk."""

        if self.BUFFER == 1:
            return self.tile
        chunk_size = (
            self.tile.shape[0] // self.BUFFER,
            self.tile.shape[1] // self.BUFFER,
        )
        return self.tile[chunk_size[0] : -chunk_size[0], chunk_size[1] : -chunk_size[1]]

    def move_left(self) -> None:
        """Moves the tiles to the left."""
        # X range
        x_0 = self.position[0] - self.tile.shape[1] + 1 - self.increment
        x_1 = x_0 + self.increment
        # Y range
        y_0 = self.position[1] - self.tile.shape[0] + 1
        y_1 = y_0 + self.tile.shape[1]
        print(x_0, x_1)
        print(y_0, y_1)
        # Create noise chunk
        chunk = opensimplex.noise2array(
            np.arange(x_0, x_1) / self.SCALE,
            np.arange(y_0, y_1) / self.SCALE,
        )
        print(self.tile.shape, chunk.shape)
        # Update position
        self.position = (x_1 - 1 + (self.tile.shape[0] - self.increment), y_1 - 1)
        # Update tile
        self.tile = np.concatenate((chunk, self.tile), axis=1)[:, : -self.increment]

    def move_right(self) -> None:
        """Moves the tiles to the right."""
        # chunk = np.empty((self.SPEED, self.tile.shape[1]))
        # for i in range(chunk.shape[0]):
        #     for j in range(chunk.shape[1]):
        #         chunk[i, j] = opensimplex.noise2(
        #             (self.position[0] + self.SPEED + i) / self.SCALE, j / self.SCALE
        #         )
        # self.position = (self.position[0] + self.SPEED, self.position[1])
        # self.tile = np.concatenate((self.tile, chunk))[self.SPEED :]

    def move_up(self) -> None:
        """Moves the tiles to the up."""
        # X range
        x_0 = self.position[0] - self.tile.shape[1] + 1
        x_1 = x_0 + self.tile.shape[1]
        # Y range
        y_0 = self.position[1] - self.tile.shape[0] + 1 - self.increment
        y_1 = y_0 + self.increment
        # Create noise chunk
        chunk = opensimplex.noise2array(
            np.arange(x_0, x_1) / self.SCALE,
            np.arange(y_0, y_1) / self.SCALE,
        )
        # Update position
        self.position = (x_1 - 1, y_1 - 1 + (self.tile.shape[0] - self.increment))
        # Update tile
        self.tile = np.concatenate((chunk, self.tile))[: -self.increment, :]

    def move_down(self) -> None:
        """Moves the tiles to the down."""
        # X range
        x_0 = self.position[0] - self.tile.shape[1] + 1
        x_1 = x_0 + self.tile.shape[1]
        # Y range
        y_0 = self.position[1]
        y_1 = y_0 + self.increment
        # Create noise chunk
        chunk = opensimplex.noise2array(
            np.arange(x_0, x_1) / self.SCALE,
            np.arange(y_0, y_1) / self.SCALE,
        )
        # Update position
        self.position = (x_1 - 1, y_1 - 1 + self.increment)
        # Update tile
        self.tile = np.concatenate((self.tile, chunk))[self.increment :, :]
