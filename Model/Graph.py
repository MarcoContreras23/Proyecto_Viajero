from Model.Backpacker import *
from Model.algorithms import *
from Model.Conection import *

class Graph:

    def __init__(self):
        self.backpacker = Backpacker(10000,20000)
        self.country = ""
        self.name = ""
        self.place = []
        self.transport = []
        self.jobs = []
        self.task = []
        self.conection = []
        self.visited = []


    def add_conection(self,distance ,origin,destiny,transport,x,y):
        newConection = Conection(distance,origin,destiny,transport,x,y)
        newConectionB = Conection(distance,origin,destiny,transport,x,y)
        pas = True
        pas1 = False
        for conection in self.conection:
            if newConection == conection:
                pas = False
            if newConectionB == conection:
                pas1 = False
                conection.bi = True
        if pas1:
            origin.adjacences.append(destiny)
        if pas and not pas1:
            self.conection.append(newConection)
            origin.adjacences.append(destiny)

    def Get_Edge(self, origin, destiny):
        for edge in self.conection:
            if edge.origin is origin and edge.destiny is destiny:
                return edge

    def search_node(self, label):
        for node in self.place:
            if node.label is label:
                return node

    def Get_Vertex(self, id):
        for place in self.place:
            if place.label is id:
                return place

    def Dijkstra(self, vertex, cost, time, variable):
        self.visited.clear()
        vertex = vertex
        vertex.status[0] = 0
        vertex.status[1] = vertex.label
        vertex.statusT[0] = 0
        vertex.statusT[1] = vertex.label
        self.visited = Algorithms().Dijkstra(
            vertex, self.place, [], self.conection, True, self.visited, cost, time)
        way = []
        cont = True
        men = self.visited[0]
        if cost:
            for node in self.visited:
                if node.status[0] > men.status[0] and node.status[0] < variable:
                    men = node
            while cont:
                way.append(men)
                if self.Get_Vertex(men.status[1]) is not men:
                    men = self.Get_Vertex(men.status[1])
                else:
                    cont = False
        if time:
            for node in self.visited:
                if node.statusT[0] > men.statusT[0] and node.statusT[0] < variable:
                    men = node
            while cont:
                way.append(men)
                if self.Get_Vertex(men.statusT[1]) is not men:
                    men = self.Get_Vertex(men.statusT[1])
                else:
                    cont = False
        return way
