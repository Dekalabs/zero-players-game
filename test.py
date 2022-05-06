import numpy as np
import pyxel


class App:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 600
        self.blocksize = 10

        pyxel.init(self.screen_width, self.screen_height, title="Map")

        self.widthblocks = int(self.screen_width / self.blocksize)
        self.heightblocks = int(self.screen_height / self.blocksize)

        self.current_matrix = np.random.rand(self.widthblocks, self.heightblocks)

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def color(self, value):
        if value < 0.3:
            return 5
        elif value < 0.5:
            return 11
        elif value < 0.8:
            return 3
        else:
            return 7

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.current_matrix = np.random.rand(self.widthblocks, self.heightblocks)

    def draw(self):
        pyxel.cls(12)

        for x in range(self.widthblocks):
            for y in range(self.heightblocks):
                current_pos = self.current_matrix[x, y]
                current_color = self.color(current_pos)
                pyxel.rect(
                    x * self.blocksize,
                    y * self.blocksize,
                    self.blocksize,
                    self.blocksize,
                    int(current_color),
                )


App()
