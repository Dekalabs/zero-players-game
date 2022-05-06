from typing import Optional

import numpy as np


class World:
    """Class that represents the generation of the world."""

    SPEED: int = 1

    def __init__(self, width: int, height: int, speed: Optional[int] = None):
        """Initializes the tile with the width and height given for the chunk."""
        self.width: int = width
        self.height: int = height
        self.speed: int = speed if speed is not None else self.SPEED
        self.tile: "np.ndarray" = self._generate_tile(
            width * 3, height * 3
        )  # Generates a tile with the current chunk and the nearest chunks

    def _generate_tile(self, width: int, height: int) -> "np.ndarray":
        """Generates a complete tile."""
        return np.random.rand(width, height)

    def _generate_tile_increment(self, axis: int = 0) -> "np.ndarray":
        """Generates an array with the increment for the tile."""
        if axis == 0:
            return np.random.rand(self.SPEED, self.tile.shape[1])
        elif axis == 1:
            return np.random.rand(self.tile.shape[0], self.SPEED)
        else:
            raise Exception("The value of axis have to be 0 or 1")

    def chunk(self) -> "np.ndarray":
        """Gets the central chunk."""
        return self.tile[self.width : -self.width, self.height : -self.height]

    def move_left(self) -> None:
        """Moves the tiles to the left."""
        self.tile = np.concatenate((self._generate_tile_increment(), self.tile))[
            : -self.SPEED
        ]

    def move_right(self) -> None:
        """Moves the tiles to the right."""
        self.tile = np.concatenate((self.tile, self._generate_tile_increment()))[
            self.SPEED :
        ]

    def move_up(self) -> None:
        """Moves the tiles to the up."""
        self.tile = np.concatenate(
            (self._generate_tile_increment(axis=1), self.tile), axis=1
        )[:, : -self.SPEED]

    def move_down(self) -> None:
        """Moves the tiles to the down."""
        self.tile = np.concatenate(
            (self.tile, self._generate_tile_increment(axis=1)), axis=1
        )[:, self.SPEED :]
