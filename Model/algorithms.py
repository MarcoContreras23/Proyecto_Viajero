from math import inf
from math import inf



class Algorithms:
    def __init__(self):
        self.routeEconomica =[]

    def BFS(self, visited, trail):
        if len(trail) == 0:
            return visited
        for place in trail[0].adjacencies:
            if place.label not in visited and place not in trail:
                trail.append(place)
        visited.append(trail[0].label)
        trail.remove(trail[0])
        return self.BFS(visited, trail)

    def DFS(self, visited, place):
        if place.label in visited:
            return visited

        visited.append(place.label)
        for adjacency in place.adjacencies:
            visited = self.DFS(visited, adjacency)
        return visited

    def Dijkstra(self, placeA, places, conection, edgesOrigin, state, visitPlaces,minCost,minTime):
        temp = []
        visited = []
        minplace = None
        minvalue = inf
        cost = 0
        visitPlaces.append(placeA)
        if len(visitPlaces) == len(places):
            return visitPlaces
        for edge in edgesOrigin:
            if edge.origin  is placeA:
                temp.append(edge)
                conection.append(edge)
        for edge in temp:
            if (edge.origin.status[0] + edge.distance) < edge.destiny.status[0]:
                if minCost:
                    for thing in edge.destiny.task:
                        if thing.type == 'mandatory':
                            cost += thing.cost
                if minTime:
                    for thing in edge.destiny.task:
                        if thing.type == 'mandatory':
                            cost += thing.time + edge.destiny.TimeHere
                edge.destiny.status[0] = edge.origin.status[0] + edge.distance + cost
                edge.origin.status[1] = edge.origin.label
        for edge in conection:
            if edge.destiny.status[0] < minvalue and edge.destiny not in visitPlaces:
                minvalue = edge.destiny.status[0]
                minplace = edge.destiny
        visited.append(minplace)
        visitPlaces = self.Dijkstra(
            minplace, places, conection, edgesOrigin, state, visitPlaces,minCost,minTime)
        return visitPlaces

    def llenarRoute(self,origen,backpacker):
        mayor = 0
        for i in self.place:
            if i.status[1] <= backpacker.budget and mayor.status[1] < i.status[1]:
                mayor = i
        aux = mayor.status[0]
        while aux is not origen:
            self.routeEconomica.append(aux)
            aux = self.buscar_Vertice(aux.status[0])

        self.ordenar_ruta()

    def ordenar_ruta(self):
        tem=[]
        for i in range(len(self.routeEconomica), -1, -1):
            tem.append(self.routeEconomica[i])
        self.routeEconomica = tem

#punto 3
    def restar_costos(self, origen, destino,transporte,actividades,backpacker):
        restarCosto = 0
        restarTiempo = 0
        for v in origen.adjacencies:
            if v.destiny is destino:
                restarCosto += v.Distance*transporte.value
                restarTiempo += v.distance*transporte.time
        for t in actividades:
            restarCosto += t.cost
            restarTiempo += t.time

        backpacker.budget -= restarCosto
        backpacker.time -= restarTiempo