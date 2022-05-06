import numpy as np
import pyxel


class World:
    chunks_number = 9
    speed = 1

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile = self.generate_chunk(width * 3, height * 3)

    def generate_chunk(self, width, height):
        return np.random.rand(width, height)
    
    def current_chunk(self):
        return self.tile[self.width: -self.width, self.height: -self.height]

    def move_left(self):
        self.tile = np.concatenate((np.random.rand(self.speed, self.tile.shape[1]), self.tile))[:-self.speed]

    def move_right(self):
        self.tile = np.concatenate((self.tile, np.random.rand(self.speed, self.tile.shape[1])))[self.speed:]

    def move_up(self):
        self.tile = np.concatenate((np.random.rand(self.tile.shape[0], self.speed), self.tile), axis=1)[:, :-self.speed]

    def move_down(self):
        self.tile = np.concatenate((self.tile, np.random.rand(self.tile.shape[0], self.speed)), axis=1)[:, self.speed:]
    
class App:
    def __init__(self):
        self.screen_width = 1024
        self.screen_height = 600
        self.blocksize = 2

        pyxel.init(self.screen_width, self.screen_height, title="Zero Players Game")

        self.world = World(self.screen_width // self.blocksize, self.screen_height // self.blocksize)
        
        self.chunksize_width = int(self.screen_width / self.blocksize)
        self.chunksize_height = int(self.screen_height / self.blocksize)

        self.viewerposition_x = self.chunksize_width
        self.viewerposition_y = self.chunksize_height

        self.tilesize_width = self.chunksize_width * 3
        self.tilesize_height = self.chunksize_height * 3

        self.current_matrix = self.world.current_chunk()

        pyxel.playm(0, loop=True)
        pyxel.run(self.update_world, self.draw_world)


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

        self.viewerposition_y += 1

    def update_world(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.world.move_down()

    
    def draw_world(self):
        pyxel.cls(12)
        self.current_matrix = self.world.current_chunk()

        for x in range(self.current_matrix.shape[0]):
            for y in range(self.current_matrix.shape[1]):
                current_pos = self.current_matrix[x, y]
                current_color = self.color(current_pos)

                pyxel.rect(
                    x * self.blocksize,
                    y * self.blocksize,
                    self.blocksize,
                    self.blocksize,
                    int(current_color),
                )


    def draw(self):
        pyxel.cls(12)

        for x in range(self.viewerposition_x, self.viewerposition_x+self.chunksize_width):
            for y in range(self.viewerposition_y, self.viewerposition_y+self.chunksize_height):
                if self.current_matrix.shape[0] > x & self.current_matrix.shape[1] > y:
                    current_pos = self.current_matrix[x, y]
                    current_color = self.color(current_pos)

                    pyxel.rect(
                        (x-self.viewerposition_x) * self.blocksize,
                        (y-self.viewerposition_y) * self.blocksize,
                        self.blocksize,
                        self.blocksize,
                        int(current_color),
                    )

                    print ((x-self.viewerposition_x)*self.blocksize, (y-self.viewerposition_y)*self.blocksize, current_color)


App()
