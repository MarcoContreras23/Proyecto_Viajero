from pygame import Rect
from math import inf

class Vertex:
    def __init__(self, label, name_city, timeHere,x,y):
        self.label = label
        self.name_city = name_city
        self.timeHere = timeHere
        self.x = x
        self.y = y
        self.jobs = []
        self.task = []  # tareas o cosas por hacer
        self.adjacencies = []
        self.status = [inf, None]

        self.rect = Rect(x,y,65,65)