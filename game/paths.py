import random
from typing import Optional, Set

import pyxel

from game import SEED

random.seed(SEED)


class Path:
    """Class to handle the automatic path selection."""

    UP, DOWN, LEFT, RIGHT = 1, 2, 3, 4
    CHANGE_INCREMENT: float = 0.00001

    def __init__(self) -> None:
        """Initializes with a current direction, and director counter."""
        self.directions: Set[int] = {self.UP, self.DOWN, self.LEFT, self.RIGHT}
        self.current_direction: int = random.choice(list(self.directions))
        self.accumulator: float = 0.0

    def _opposite(self, direction: int) -> int:
        """Gets the opposite direction."""
        return {
            self.UP: self.DOWN,
            self.RIGHT: self.LEFT,
            self.DOWN: self.UP,
            self.LEFT: self.RIGHT,
        }.get(direction, direction)

    def direction(self) -> int:
        """Gets a random direction."""
        should_change = not (1.0 > random.random() > self.accumulator)
        if should_change:
            self.accumulator = 0.0
            self.current_direction = random.choice(
                list(
                    self.directions
                    - {self.current_direction, self._opposite(self.current_direction)}
                )
            )
        else:
            self.accumulator += self.CHANGE_INCREMENT
        return self.current_direction

    def manual_direction(self) -> Optional[int]:
        """Control directions using keyboard."""
        if pyxel.btn(pyxel.KEY_W):
            return self.UP
        if pyxel.btn(pyxel.KEY_D):
            return self.RIGHT
        if pyxel.btn(pyxel.KEY_A):
            return self.LEFT
        if pyxel.btn(pyxel.KEY_S):
            return self.DOWN
        return None
