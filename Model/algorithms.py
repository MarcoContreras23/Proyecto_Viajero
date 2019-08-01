from math import inf
from math import inf



class Algorithms:
    def __init__(self):
        self.routeEconomica =[]
        self.trabajo =  False



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
            if edge.obs is False:
                if edge.origin  is placeA:
                    temp.append(edge)
                    conection.append(edge)
        for edge in temp:
            if minCost:
                if (edge.origin.status[0] + edge.distance) < edge.destiny.status[0]:
                    for thing in edge.destiny.task:
                        if thing.type == 'mandatory':
                            cost += thing.cost
                    edge.destiny.status[0] = edge.origin.status[0] + \
                                             edge.distance + cost
                    edge.destiny.status[1] = edge.origin.label
            elif minTime:
                if (edge.origin.statusT[0] + edge.distance) < edge.destiny.statusT[0]:
                    for thing in edge.destiny.task:
                        if thing.type == 'mandatory':
                            cost += thing.time + edge.destiny.timeHere
                    edge.destiny.statusT[0] = edge.origin.statusT[0] + \
                                              edge.distance + cost
                    edge.destiny.statusT[1] = edge.origin.label
            else:
                if (edge.origin.statusD[0] + edge.distance) < edge.destiny.statusD[0]:
                    edge.destiny.statusD[0] = edge.origin.statusD[0] + edge.distance
                    edge.destiny.statusD[1] = edge.origin.label
        for edge in conection:
            if minCost:
                if edge.destiny.status[0] < minvalue and edge.destiny not in visitPlaces:
                    minvalue = edge.destiny.status[0]
                    minplace = edge.destiny
            elif minTime:
                if edge.destiny.statusT[0] < minvalue and edge.destiny not in visitPlaces:
                    minvalue = edge.destiny.statusT[0]
                    minplace = edge.destiny
            else:
                if edge.destiny.statusD[0] < minvalue and edge.destiny not in visitPlaces:
                    minvalue = edge.destiny.statusD[0]
                    minplace = edge.destiny
        visited.append(minplace)
        visitPlaces = self.Dijkstra(
            minplace, places, conection, edgesOrigin, state, visitPlaces,minCost,minTime)
        return visitPlaces


