from math import inf
from math import inf



class Algorithms:
    def __init__(self):
        self.routeEconomica =[]
        self.trabajo =  False
        #atributos para reporte

        self.lugaresVisitados = []
        self.tiempoLugares = 0
        self.gastoLugares = 0
        self.gananciasLugares = 0

        self.transporteUtilizado = []
        self.gastosTransporte = 0
        self.tiempoTransporte =0

        self.trabajos = []
        self.gananciasTrabajos = 0
        self.tiempoTrabajos = 0

        self.actividades  = []
        self.gastosActividades = 0
        self.tiempoActividades = 0


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
#se llama despues de dijkstra para que cree la ruta
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

# llamar para saber si se envian atributos trabajos y time_trabajo  en la siguiente funcion
    def evaluar_presupuesto(self, backpacker):
        if backpacker.budget <= backpacker.porcentaje_minimo:
            return True
        else:
            return False
#se llama cuando el mochilero comience a seguir la ruta por cada vertice que avance
    def empezar_viaje(self, origen, destino, transporte, actividades, backpacker, trabajos, time_trabajo):
        self.restar_costos(origen, destino,transporte,actividades,backpacker, trabajos, time_trabajo)

#como el mochilero no puede dormir mientras viaja o hace una actividad se debe tener en cuenta de que si el tiempo que demoro lo que hacia el mochilero
#paso las 18 horas el debe dormir al terminar
    def restar_costos(self, origen, destino,transporte,actividades,backpacker, trabajo, time_trabajo):
        restarCosto = 0
        restarTiempo = 0
        nodo_evaluado =None
        numero_dormidas=0
        numero_comidas = 0



        for v in origen.adjacencies:
            if v.destiny is destino:
                nodo_evaluado =v.destiny
                restarCosto += v.Distance*transporte.value
                restarTiempo += v.distance*transporte.time

                if v.distance*transporte.time // 18 is not 0:
                    numero_dormidas += 1 #solo 1 porque asi cumpla varias veces la hora mientras viaja no puede dormir

                if v.distance*transporte.time // 6 is not 0:
                    numero_comidas += v.distance*transporte.time // 6 #se multiplica por todas las veces que se cumplieron las 6 horas porque puede comer asi este haciendo algo

                self.transporteUtilizado.append(transporte)
                self.gastosTransporte = v.Distance * transporte.value
                self.tiempoTransporte = v.Distance * transporte.time


        if trabajo is not None:
                restarCosto -= trabajo.gain*time_trabajo # resto las ganancias de los trabajos a esta variable ya que esta es quien me reune el total a restar
                #al presupuesto del muchilero
                self.trabajos.append(trabajo)
                self.gananciasTrabajos +=  trabajo.gain*time_trabajo
                self.tiempoTrabajos += time_trabajo
                restarTiempo += time_trabajo
                if time_trabajo // 18 is not 0:
                    numero_dormidas += 1
                if time_trabajo // 6 is not 0:
                    numero_comidas += time_trabajo // 6

        if actividades is not None:
            for t in actividades:
                self.actividades.append(t)
                self.gastosActividades += t.cost
                self.tiempoActividades += t.time
                restarCosto += t.cost
                restarTiempo += t.time
                if t.time // 18 is not 0:
                    numero_dormidas += 1
                if t.time // 6 is not 0:
                    numero_comidas += t.time // 6

        for obli in nodo_evaluado.task:
            if obli.name is "Sleep":
                restarCosto += obli.cost*numero_dormidas
                restarTiempo += obli.time *numero_dormidas
                self.actividades.append(obli)
                self.gastosActividades += obli.cost*numero_dormidas
                self.tiempoActividades += obli.time *numero_dormidas
            if obli.name is "Eat":
                restarCosto += obli.cost * numero_comidas
                restarTiempo += obli.time * numero_comidas
                self.actividades.append(obli)
                self.gastosActividades += obli.cost * numero_comidas
                self.tiempoActividades += obli.time * numero_comidas
    # si el tiempo minimo de estar en ese lugar no se ha cumplido despues de las actividades y trabajos se debe restar al tiempo del mochilero como tiempo de ocio
        if nodo_evaluado.timeHere < backpacker.time - restarTiempo:
            restarTiempo += (backpacker.time - restarTiempo)

        backpacker.budget -= restarCosto
        backpacker.time -= restarTiempo
        self.lugaresVisitados.append(nodo_evaluado)
        self.tiempoLugares += restarTiempo
        self.gastoLugares += restarCosto
        self.gananciasLugares += self.gananciasTrabajos