__author__ = 'harun'
import random
import pyglet
from pyglet.gl import *


class DiamondSquareTerrain():
    def __init__(self, iterations, seed, deviations, roughness):
        self.iterations = iterations
        self.seed = seed
        self.deviations = deviations
        self.roughness = roughness
        self.size = 2**iterations + 1
        self.verticles = [[0.0 for i in range(0, self.size)]for j in range(0, self.size)]
        self.wires = glGenLists(1)

    def assign_start_verticles(self):
        self.verticles[0][self.size-1] = self.seed
        self.verticles[0][0] = self.seed
        self.verticles[self.size-1][0] = self.seed
        self.verticles[self.size-1][self.size-1] = self.seed

    def generate_height_map(self):
        for i in range(self.iterations):
            diff_a = (self.size - 1) / (2**(i+1))
            diff_b = diff_a/2
            for x in range(i**2):
                for y in range(i**2):
                    dx = x * diff_b
                    dy = y * diff_b
                    #diamond vars / diamond step
                    a = self.verticles[dx][dy]
                    b = self.verticles[dx + diff_b][dy]
                    c = self.verticles[dx + diff_b][dy + diff_b]
                    d = self.verticles[dx][dy + diff_b]
                    e = random.gauss(((a + b + c + d)/4.0), self.deviations)

                    if self.verticles[dx + diff_a][dy + diff_a] == 0.0:
                        self.verticles[dx + diff_a][dy + diff_a] = e

                    #square step / coutn all vert on the square form e
                    if self.verticles[dx][dy + diff_a] == 0.0:
                        self.verticles[dx][dy + diff_a] = random.gauss((a + c + e)/3.0, self.deviations)
                    if self.verticles[dx + diff_a][dy] == 0.0:
                        self.verticles[dx + diff_a][dy] = random.gauss((a + b + e)/3.0, self.deviations)
                    if self.verticles[dx + diff_b][dy + diff_a] == 0.0:
                        self.verticles[dx + diff_b][dy + diff_a] = random.gauss((b + d + e)/3.0, self.deviations)
                    if self.verticles[dx + diff_a][dy + diff_b] == 0.0:
                        self.verticles[dx + diff_a][dy + diff_b] = random.gauss((c + d + e)/3.0, self.deviations)

            self.deviations *= 2**-self.roughness

    def print_verticles_map(self):
        for r in self.verticles:
            print r

    def create_gl_contex(self):
        t = self.size /2

if __name__ == '__main__':
    pass
    # gen = DiamondSquareTerrain(10, 10, 6, 1.4)
    # gen.assign_start_verticles()
    # gen.generate_height_map()
    # gen.print_verticles_map()
