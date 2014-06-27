__author__ = 'harun'
import random
import pyglet
from pyglet.gl import *


class DiamondSquareTerrain():
    def __init__(self, iterations, seed, deviations, roughness, random=False):
        self.iterations = iterations
        self.seed = seed
        self.deviations = deviations
        self.roughness = roughness
        self.size = 2**iterations + 1
        self.verticles = [[0.0 for i in range(0, self.size)] for j in range(0, self.size)]
        if not random:
            self.assign_start_verticles()
        else:
            self.assign_random_verticles()
        self.wires = glGenLists(1)

    def assign_start_verticles(self):
        self.verticles[0][-1] = self.seed
        self.verticles[0][0] = self.seed
        self.verticles[-1][0] = self.seed
        self.verticles[-1][-1] = self.seed

    def assign_random_verticles(self):
        self.verticles[0][self.size - 1] = random.gauss(self.seed, self.deviation)
        self.verticles[0][0] = random.gauss(self.seed, self.deviation)
        self.verticles[self.size - 1][0] = random.gauss(self.seed, self.deviation)
        self.verticles[self.size - 1][self.size - 1] = random.gauss(self.seed, self.deviation)

    def generate_height_map(self):
        for i in range(self.iterations):
            diff_a = (self.size - 1) / (2 ** (i + 1))
            diff_b = diff_a * 2
            for x in range(i ** 2):
                for y in range(i ** 2):
                    dx = x * diff_b
                    dy = y * diff_b
                    # diamond vars / diamond step
                    a = self.verticles[dx][dy]
                    b = self.verticles[dx + diff_b][dy]
                    c = self.verticles[dx + diff_b][dy + diff_b]
                    d = self.verticles[dx][dy + diff_b]
                    e = random.gauss(((a + b + c + d) / 4.0), self.deviations)

                    if self.verticles[dx + diff_a][dy + diff_a] == 0.0:
                        self.verticles[dx + diff_a][dy + diff_a] = e

                    #square step / coutn all vert on the square form e
                    if self.verticles[dx][dy + diff_a] == 0.0:
                        self.verticles[dx][dy + diff_a] = random.gauss((a + c + e) / 3.0, self.deviations)
                    if self.verticles[dx + diff_a][dy] == 0.0:
                        self.verticles[dx + diff_a][dy] = random.gauss((a + b + e) / 3.0, self.deviations)
                    if self.verticles[dx + diff_b][dy + diff_a] == 0.0:
                        self.verticles[dx + diff_b][dy + diff_a] = random.gauss((b + d + e) / 3.0, self.deviations)
                    if self.verticles[dx + diff_a][dy + diff_b] == 0.0:
                        self.verticles[dx + diff_a][dy + diff_b] = random.gauss((c + d + e) / 3.0, self.deviations)

            self.deviations *= 2 ** -self.roughness

    def print_verticles_map(self):
        for r in self.verticles:
            print r

    def create_gl_contex(self):
        t = self.size / 2
        glNewList(self.wires, GL_COMPILE)
        glBegin(GL_LINES)
        for x in range(self.size):
            for y in range(self.size):
                glColor3f(0.0, 1.0, 0.0)
                if x > 0:
                    glVertex3f((x - 1) - t, y - t, self.verticles[x - 1][y])
                    glVertex3f(x - t, y - t, self.verticles[x][y])

                glColor3f(0.0, 0.0, 1.0)
                if y > 0:
                    glVertex3f(x - t, (y - 1) - t, self.verticles[x][y - 1])
                    glVertex3f(x - t, y - t, self.verticles[x][y])
        glEnd()
        glEndList()

    def draw_height_map(self):
        glCallList(self.wires)

if __name__ == '__main__':
    win = pyglet.window.Window(fullscreen=True)
    xrot = 60.0
    zrot = 45.0
    xtrans = win.width / 2
    ytrans = win.height / 2
    ztrans = 0.0
    zoom = 10.0

    @win.event
    def on_mouse_scroll(x, y, scroll_x, scroll_y):
        global zoom
        zoom -= scroll_y * 0.1

        if zoom > 20.0:
            zoom = 20.0
        elif zoom < 1.0:
            zoom = 1.0

    @win.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        global xrot, zrot
        xrot -= dy
        zrot += dx

        if xrot > 360.0:
            xrot = 0.0
        elif xrot < 0.0:
            xrot = 360.0

        if zrot > 360.0:
            zrot = 0.0
        elif zrot < 0.0:
            zrot = 360.0

    terrain = DiamondSquareTerrain(iterations=9, seed=0.0, deviations=60.0, roughness=1.0)
    terrain.generate_height_map()
    terrain.create_gl_contex()
    fps = pyglet.clock.ClockDisplay()

    win.dispatch_events()

    # set matrix mode to projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # set viewport to the entire window
    glViewport(0, 0, win.width, win.height)

    # set clipping volume
    glOrtho(0.0, win.width, 0.0, win.height, -500.0, 500.0)

    # set matrix mode to modelview
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    while not win.has_exit:
        win.dispatch_events()

        glLoadIdentity()

        # clear screen
        glClearColor(0.1, 0.1, 0.1, 0.5)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        fps.draw()

        # set matrix mode to modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # perform our camera orentations
        glTranslatef(xtrans, ytrans, ztrans)
        glRotatef(xrot, 1, 0, 0)
        glRotatef(zrot, 0, 0, 1)
        glScalef(zoom, zoom, zoom)

        # draw our terrain
        terrain.draw_height_map()

        pyglet.clock.tick()
        win.flip()