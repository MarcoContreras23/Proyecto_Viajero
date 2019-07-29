from Model.Backpacker import *
from Model.algorithms import *

class Graph:

    def __init__(self):
        self.backpacker = Backpacker()
        self.country = ""
        self.name = ""
        self.place = []
        self.transport = []
        self.jobs = []
        self.task = []
        self.conection = []
        self.visited = []


    def search_node(self, label):
        for node in self.place:
            if node.label is label:
                return node

    def Get_Vertex(self, id):
        for place in self.place:
            if place.label is id:
                return place

    def Dijkstra(self):
        self.visited.clear()
        vertex = self.Get_Vertex('A')
        vertex.status[0] = 0
        vertex.status[1] = vertex.label
        self.visited = Algorithms().Dijkstra(
        vertex, self.place, [], self.conection, True, self.visited)
        show = []
        for edge in self.conection:
            if edge.origin not in show:
                print(f"{edge.origin.label} = {edge.origin.status}")
                show.append(edge.origin)
            if edge.destiny not in show:
                print(f"{edge.destiny.label} = {edge.destiny.status}")
                show.append(edge.destiny)
