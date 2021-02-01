import numpy, pygame
from enum import Enum

x = 0


class Direction(Enum):
    TOP = [-1, 0]
    RIGHT = [0, 1]
    BOTTOM = [1, 0]
    LEFT = [0, -1]

color_of_object = {
    ".": (0,165,231),
    "X": (255,0,0),
    "@": (0, 0, 0),
    "%": (0,102,31),
    "/": (0,239,35)
}



class Map:
    def __init__(self, file):
        self.matrix = numpy.array([[*x] for x in numpy.genfromtxt(file, dtype='str')])
        self.car = self.get_object_pos("%")
        self.dump = self.get_object_pos("@")
        self.solvable = True
        self.display = pygame.Surface(self.matrix.shape)
        self.draw_map()

    def draw_map(self):
        for i, row in enumerate(self.matrix):
            for j, object in enumerate(row):
                pygame.draw.rect(self.display, color_of_object[object], (j, i, 1, 1))

    def get_object_pos(self, object):
        res = None
        for i, x in enumerate(self.matrix):
            for j, y in enumerate(x):
                if y == object:
                    res = [i, j]
        return res

    def get_surrounded(self, pos):
        surr = []
        for dir in Direction:
            new_pos = [pos[0] + dir.value[0], pos[1] + dir.value[1]]
            if abs(new_pos[0]) < self.matrix.shape[0] and abs(new_pos[1]) < self.matrix.shape[1] and new_pos[0] >= 0 and new_pos[1] >= 0:
                obj = self.matrix[new_pos[0]][new_pos[1]]
                surr.append(new_pos if obj == "." or obj == "@" else [])
            else:
                surr.append([])
        return surr