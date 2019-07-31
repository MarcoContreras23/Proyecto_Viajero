from Model.Backpacker import *
from Model.algorithms import *
from Model.Conection import *

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

        self.obstruidas = self.getObstruidad

        # atributos para reporte

        self.lugaresVisitados = []
        self.tiempoLugares = 0
        self.gastoLugares = 0
        self.gananciasLugares = 0

        self.transporteUtilizado = []
        self.gastosTransporte = 0
        self.tiempoTransporte = 0

        self.trabajos = []
        self.gananciasTrabajos = 0
        self.tiempoTrabajos = 0

        self.actividades = []
        self.gastosActividades = 0
        self.tiempoActividades = 0

    def getObstruidad(self):
        obstruidas=[]
        for i in self.conection:
            if i.obs:
                obstruidas.append(i)
                self.conection.remove(i)
                i.origin.adjacencies.remove(i)
        return obstruidas

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
            if edge.destiny is destiny and edge.origin is origin:
                return edge

    def Get_Places(self, origin, destiny):
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
        ##agregue for para actualizar colores no funciona -----------------------------------------------
        if cost:
            for conec in self.conection:
                if conec.color is (120, 255, 120):
                    conec.color = (36, 113, 163)
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
            for conec in self.conection:
                if conec.color is (0, 0, 0):
                    print("actualice color de tiempo")
                    conec.color = (36, 113, 163)
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
    def getTransporte (self,id):
        for t in self.transport:
            if t.id is id:
                return t
    def restar_costos(self, origen, destino, transporte, actividades ,trabajo, time_trabajo):
        restarCosto = 0
        restarTiempo = 0
        nodo_evaluado = None
        numero_dormidas = 0
        numero_comidas = 0

        for v in origen.adjacencies:
            if v.destiny is destino:
                nodo_evaluado = v.destiny
                restarCosto += v.distance * transporte.value
                restarTiempo += v.distance * transporte.time
                print("tiempo de camino",transporte.time)

                if (v.distance * transporte.time / 60) // 18 is not 0:
                    numero_dormidas += 1  # solo 1 porque asi cumpla varias veces la hora mientras viaja no puede dormir

                if (v.distance * transporte.time / 60) // 6 is not 0:
                    numero_comidas += v.distance * transporte.time/60 // 6  # se multiplica por todas las veces que se cumplieron las 6 horas porque puede comer asi este haciendo algo

                self.transporteUtilizado.append(transporte.name)

                self.gastosTransporte = v.distance * transporte.value
                self.tiempoTransporte = v.distance * transporte.time

        if self.backpacker.work:
            print("entre a trabajo")
            restarCosto -= trabajo.gain * time_trabajo  # resto las ganancias de los trabajos a esta variable ya que esta es quien me reune el total a restar
            # al presupuesto del muchilero
            self.trabajos.append(trabajo)
            self.gananciasTrabajos += trabajo.gain * time_trabajo
            self.tiempoTrabajos += time_trabajo
            restarTiempo += time_trabajo
            if time_trabajo // 18 is not 0:
                numero_dormidas += 1
            if time_trabajo // 6 is not 0:
                numero_comidas += time_trabajo // 6

        if actividades is not None:
            for t in actividades:
                self.actividades.append(t.name)
                self.gastosActividades += t.cost
                self.tiempoActividades += t.time
                restarCosto += t.cost
                restarTiempo += t.time
                if t.time*60 // 18 is not 0:
                    numero_dormidas += 1
                if t.time*60 // 6 is not 0:
                    numero_comidas += t.time // 6

        for obli in nodo_evaluado.task:
            if obli.name is "Sleep":
                restarCosto += obli.cost * numero_dormidas
                restarTiempo += obli.time * numero_dormidas
                self.actividades.append(obli)
                self.gastosActividades += obli.cost * numero_dormidas
                self.tiempoActividades += obli.time * numero_dormidas
            if obli.name is "Eat":
                restarCosto += obli.cost * numero_comidas
                restarTiempo += obli.time * numero_comidas
                self.actividades.append(obli)
                self.gastosActividades += obli.cost * numero_comidas
                self.tiempoActividades += obli.time * numero_comidas
        # si el tiempo minimo de estar en ese lugar no se ha cumplido despues de las actividades y trabajos se debe restar al tiempo del mochilero como tiempo de ocio
        if nodo_evaluado.timeHere < restarTiempo:
            restarTiempo += (nodo_evaluado.timeHere - restarTiempo)

        print(self.backpacker.budget)
        print(self.backpacker.time)
        self.backpacker.budget -= restarCosto
        self.backpacker.time -= restarTiempo
        self.lugaresVisitados.append(nodo_evaluado)
        self.tiempoLugares += restarTiempo
        self.gastoLugares += restarCosto
        self.gananciasLugares += self.gananciasTrabajos
        print(self.backpacker.budget,"despues")
        print(self.backpacker.time,"despues tiempo",self.tiempoLugares)