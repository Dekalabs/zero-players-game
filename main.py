import numpy as np
import pyxel


class App:
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 600
        self.blocksize = 10

        pyxel.init(self.screen_width, self.screen_height, title="Map")

        self.chunksize_width = int(self.screen_width / self.blocksize)
        self.chunksize_height = int(self.screen_height / self.blocksize)

        self.viewerposition_x = self.chunksize_width
        self.viewerposition_y = self.chunksize_height

        self.tilesize_width = self.chunksize_width * 3
        self.tilesize_height = self.chunksize_height * 3

        self.current_matrix = np.random.rand(self.tilesize_width, self.tilesize_height)

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

        self.viewerposition_x += 1
        self.viewerposition_y += 1

        

    def draw(self):
        pyxel.cls(12)

        for x in range(self.viewerposition_x, self.tilesize_width):
            for y in range(self.viewerposition_y, self.tilesize_height):
                current_pos = self.current_matrix[x, y]
                current_color = self.color(current_pos)

                pyxel.rect(
                    x-self.viewerposition_x * self.blocksize,
                    y-self.viewerposition_y * self.blocksize,
                    self.blocksize,
                    self.blocksize,
                    int(current_color),
                )


App()
