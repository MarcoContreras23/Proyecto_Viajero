import sys
import os
from tkinter import *
import threading
from pygame.locals import *
from Principal.Button import *
from Principal.Cursor import *
import ctypes
from Model.algorithms import *
from Model.Graph import *
from pygame import Rect

pygame.init()
pygame.font.init()


class GUI:

    def __init__(self,graph):
        self.graph = graph
        self.x = 0
        self.y = 0
        self.time = None
        self.cost = None
        self.destiny = None
        self.origin = None
        self.Nodeinit = None
        self.cursor = Cursor()
        self.mintime = False
        self.mincost = False
        self.ways = False
        self.pas = False
        self.obs = False
        self.MinMoney = False
        self.start = False
        self.begin = True
        self.visited = []
        self.waySave = []
        self.inicio = False

        self.actividadesVertice = []  # esta lista se va a limpiar en cuanto se llame a el algoritmo que
        # resta el costo de las actividades al mochilero para seguir al siguiente nodo

        self.startRoute = True # para establecer cuando el mochilero comenzo su ruta y se le deben ofertar actividades y trabajos
        self.all()
        # thread = threading.Thread(self.all())
        # thread.start()

    def screen_sizeW(self):
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        ancho, alto = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        size = (ancho, alto)
        return size

    def all(self):

        display = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
        pygame.display.set_caption("Travel!!")
        fuente = pygame.font.SysFont('Comic Sans MS', 15)

        # Cargar las images
        city = pygame.image.load("..\\Resource\\cityscape.png")
        backpacker = pygame.image.load("..\\Resource\\adventurer2.png")
        button = pygame.image.load("..\\Resource\\button.png")
        crash = pygame.image.load("..\\Resource\\car-crash.png")
        dead = pygame.image.load("..\\Resource\\DeadDonkey.png")
        # van
        carUp = pygame.image.load("..\\Resource\\carUp.png")
        carLeft = pygame.image.load("..\\Resource\\carLeft.png")
        carRight = pygame.image.load("..\\Resource\\carRight.png")
        carDown = pygame.image.load("..\\Resource\\carDown.png")
        # Donkey
        donkeyRight = pygame.image.load("..\\Resource\\donkey.png")
        donkeyLeft = pygame.image.load("..\\Resource\\donkeyLeft.png")
        donkeyUp = pygame.image.load("..\\Resource\\donkeyUp.png")
        donkeyDown = pygame.image.load("..\\Resource\\donkeyDown.png")
        # Airplane
        airplaneUp = pygame.image.load("..\\Resource\\plane.png")
        airplaneLeft = pygame.image.load("..\\Resource\\planeLeft.png")
        airplaneRight = pygame.image.load("..\\Resource\\planeRight.png")
        airplaneDown = pygame.image.load("..\\Resource\\planeDown.png")

        # escala las imagenes
        button = pygame.transform.scale(button, (140, 75))
        button2 = pygame.transform.scale(button, (110, 90))
        # Asignacion de botones
        boton = ButtonP(button, button2, 300, 60)
        boton2 = ButtonP(button, button2, 440, 60)
        boton3 = ButtonP(button,button2,160,60)
        # texto de botones
        obstruccion = fuente.render("Obstruir camino", True, (0, 0, 0))
        way = fuente.render("Minimum way", True,(0,0,0))
        travel = fuente.render("Start Travel",True,(0,0,0))
        init = None
        poss = (0, 0)
        MinCost = []
        MinTime = []
        airplane = False
        car = False
        donkey = False
        usePlane = False
        useCar = False
        useDonkey = False



        while True:
            """for donde se ejecutan los eventos"""
            display.fill((189, 195, 199))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
            #cuando comience a viajar
                    if self.startRoute:
                        if self.time is None:
                            screenTK3 = Tk()
                            size = self.screen_sizeW()
                            screenTK3.geometry(
                                f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                            screenTK3.title(
                                "Backpacker")
                            self.cost =IntVar()
                            self.time =IntVar()
                            textC = StringVar(
                                value="Write the backpacker budget.")
                            labelC = Label(
                                screenTK3, textvariable=textC).place(x=5, y=10)
                            texcT =StringVar(
                                value="Write the backpacker time")
                            labelT= Label(
                                screenTK3,textvariable=texcT).place(x=5,y=50)
                            Cost_field = Entry(
                                screenTK3, textvariable=self.cost, width=25).place(x=10, y=30)
                            time_field = Entry(
                                screenTK3, textvariable = self.time, width=25).place(x=10 , y=70)
                            Button(screenTK3, text="OK",
                                   command=lambda: screenTK3.destroy()).place(x=170, y=100)
                            screenTK3.mainloop()
                            self.graph.backpacker.time =self.time.get()
                            self.graph.backpacker.budget = self.cost.get()
                        if self.graph.backpacker.position is None:
                            if self.inicio is False:
                                alerta= Tk()
                                size = self.screen_sizeW()
                                alerta.geometry(
                                    f"430x140+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                                aviso = StringVar(
                                    value="por favor seleccione el sitio donde comenzara el viaje")
                                Label(
                                    alerta, textvariable=aviso).place(x=5, y=50)
                                Button(alerta, text="OK",
                                       command=lambda: alerta.destroy()).place(x=170, y=80)
                                alerta.mainloop()
                                self.inicio = True

                            for position in self.graph.place:
                                if self.cursor.colliderect(position.rect):
                                    self.graph.backpacker.position = position


            # todo esto lo debo hacer cuando el viajero ya haya terminado en el nodo en el que esta
                #y le de click al nodo al que quiere ir
                        for places in self.graph.place:
                            if self.cursor.colliderect(places.rect):
                # ofertar actividades
                                screenTK = Tk()
                                size = self.screen_sizeW()
                                screenTK.geometry(
                                    f"400x200+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                                screenTK.title(
                                    "Select actividad")
                                x = 40
                                y = 0

                                for t in places.task:
                                    if t.type == "optional":
                                        y+=30
                                        Button(screenTK, text=t.name,
                                            command=lambda: self.recopilarActividades(screenTK, t)).place(x=x,y= y)
                                        Button(screenTK, text="ok",
                                               command=lambda:screenTK.destroy()).place(x=x, y=90)
                                screenTK.mainloop()
                #ofertar trabajos
                                if self.graph.backpacker.getWork():#si ya gasto dismunuyo el presupuesto en un 40% oferta trabajo
                                    screenJobs = Tk()
                                    size = self.screen_sizeW()
                                    screenJobs.geometry(
                                        f"200x200+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                                    screenJobs.title(
                                        "Select Job")
                                    x = 40
                                    y = 0
                                    for t in places.jobs:
                                        y += 30
                                        Button(screenJobs, text=t.name,
                                               command=lambda: self.recopilarActividades(screenJobs, t)).place(x=x, y=y)
                                        Button(screenJobs, text="ok",
                                               command=lambda: screenJobs.destroy()).place(x=x, y=90)
                                    screenJobs.mainloop()
            #para proponer rutas
                    if self.cursor.colliderect(boton2.rect):
                        screenTK = Tk()
                        size = self.screen_sizeW()
                        screenTK.geometry(
                            f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK.title(
                            "Select way to show")
                        Button(screenTK, text="Way the minimun cost",
                               command = lambda: self.way(screenTK, 1)).place(x=150, y=20)
                        Button(screenTK, text="Way the minimun time",
                               command = lambda: self.way(screenTK, 2)).place(x=150, y=70)
                        screenTK.mainloop()
            #para ruta mas optima en tiempo
                    elif self.mintime:
                        for place in self.graph.place:
                            if self.cursor.colliderect(place.rect):
                                self.origin = place
                        self.ways = True
            #para ruta mas economica
                    elif self.mincost:
                        for place in self.graph.place:
                            if self.cursor.colliderect(place.rect):
                                self.origin = place
                        self.ways = True

                    if self.ways:
                        self.waySave.clear()
                        if self.mincost:
                            MinCost = self.graph.Dijkstra(
                                self.origin, True, False, int(self.cost.get()))
                            self.waySave = MinCost
                            for node in self.waySave:
                               if node.status[1] is self.origin.label:
                                   self.destiny = node
                                   break
                        if self.mintime:
                            MinTime = self.graph.Dijkstra(
                                self.origin, False, True, int(self.time.get()))
                            self.waySave = MinTime
                            for node in self.waySave:
                                if node.status[1] is self.origin.label:
                                    self.destiny = node
                                    break
                        if self.mincost:
                            for edge in self.graph.conection:
                                for node in MinCost:
                                    if edge.origin is self.graph.Get_Vertex(node.status[1]) and edge.destiny is node:
                                        edge.color = (120, 255, 120)
                                    if edge.origin is node and edge.destiny is self.graph.Get_Vertex(node.status[1]):
                                        edge.color = (120, 255, 120)
                            self.mincost = False
                        if self.mintime:
                            for edge in self.graph.conection:
                                for node in MinTime:
                                    if edge.origin is self.graph.Get_Vertex(node.statusT[1]) and edge.destiny is node:
                                        edge.color = (0, 0, 0)
                                    if edge.origin is node and edge.destiny is self.graph.Get_Vertex(node.status[1]):
                                        edge.color = (0, 0, 0)
                            self.mintime = False
                        self.ways = False
                        self.start = True
                    if self.start:
                        self.pas = True
                        screenTK4 = Tk()
                        size = self.screen_sizeW()
                        screenTK4.geometry(
                            f"430x260+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK4.title(
                            "Travel form")
                        edge = self.graph.Get_Edge( self.origin, self.destiny)
                        for transports in edge.transport:
                            if transports.id == 1:
                                print( "Es avion")
                                airplane = True
                                Tr1 = transports
                            if transports.id == 2:
                                print("Es carro")
                                car = True
                                Tr2 = transports
                            if transports.id == 3:
                                print("Es Burro")
                                donkey = True
                                Tr3 = transports
                        if airplane:
                            Button(screenTK4, text="Airplane",
                                   command=lambda: self.transport(screenTK4, Tr1)).place(x=20, y=50)
                            usePlane = True
                        if car:
                            Button(screenTK4, text="Car",
                                   command=lambda: self.transport(screenTK4, Tr2)).place(x=20, y=100)
                            useCar = True
                        if donkey:
                            Button(screenTK4, text="Donkey",
                                   command=lambda: self.transport(screenTK4, Tr3)).place(x=20, y=150)
                            useDonkey = True

                        screenTK4.mainloop()

                    if self.cursor.colliderect(boton.rect):
                        self.obs = True
                    elif self.obs:
                        for a in range(len(self.graph.conection)):
                            if (self.graph.conection[a].line.x < pygame.mouse.get_pos()[0]
                                    < self.graph.conection[a].line.right and self.graph.conection[a].line.y
                                    < pygame.mouse.get_pos()[1] < self.graph.conection[a].line.bottom):
                                self.graph.conection[a].obs = True
                                break
                            self.obs = False


                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            if self.graph == None:
                print("Grafo vacío, no se puede dibujar")
            else:
                """grafica las aristas"""
                show = []
                for j in range(0, len(self.graph.conection)):
                    origin = self.graph.conection[j].origin
                    destiny = self.graph.conection[j].destiny
                    if self.graph.conection[j] not in show:
                        self.graph.conection[j].line = (pygame.draw.line(display, self.graph.conection[j].color,
                                                                     (origin.x,
                                                                      origin.y),
                                                                     (destiny.x,
                                                                      destiny.y),3))
                        self.graph.Get_Edge(destiny, origin).line = self.graph.conection[j].line
                        show.append(self.graph.conection[j])
                        show.append(self.graph.Get_Edge(destiny, origin))
                    #pygame.draw.rect(display, (0, 0, 0),
                     #                (self.graph.conection[j].rect.left, self.graph.conection[j].rect.top
                      #                , self.graph.conection[j].rect.width, self.graph.conection[j].rect.height))
                    # pygame.draw.rect(display,(0,0,0),self.graph.conection[j].rect,2)
                    if self.graph.conection[j].obs:
                        self.graph.conection[j].line = (pygame.draw.line(display, (250,0,0),
                                                                         (origin.x,
                                                                          origin.y),
                                                                         (destiny.x,
                                                                          destiny.y), 3))
                        display.blit(dead, (self.graph.conection[j].line.centerx ,self.graph.conection[j].line.centery))


                for i in range(0, len(self.graph.place)):
                    """grafica nodo"""
                    font = pygame.font.Font(None, 30)
                    scoretext = font.render(str(self.graph.place[i].name_city), 1, (0, 0, 0))
                    display.blit(scoretext, (self.graph.place[i].x - 64, self.graph.place[i].y - 64))
                    self.graph.place[i].line = display.blit(city, (self.graph.place[i].x - 30,self.graph.place[i].y - 40))
                    # pinta el viajero
            if self.graph.backpacker.position is not None and self.startRoute is True:
                xB = self.graph.backpacker.position.x - 105
                yB = self.graph.backpacker.position.y - 50
                display.blit(backpacker, (xB, yB))
            if self.pas:
                Orientation = None
                if usePlane:
                    Orientation = self.MoveImage(poss, init, self.destiny, airplaneRight, airplaneDown, airplaneLeft, airplaneUp)
                elif useCar:
                    Orientation = self.MoveCar(poss,init, carRight, carDown, carLeft, carUp)
                elif useDonkey:
                    Orientation = self.MoveDonkey(poss,init,donkeyRight,donkeyDown,donkeyLeft,donkeyUp)
                display.blit(Orientation, (poss[0], poss[1]))
                for place in self.graph.place:
                    if place.x == poss[0] and place.y == poss[1]:
                        init = place
                    if init == self.destiny:
                        self.pas = False

                if self.pas:
                    poss = self.transportMove(init, self.destiny, poss)

            self.cursor.update()
            boton.update(display, self.cursor, obstruccion)
            boton2.update(display, self.cursor, way)
            boton3.update(display,self.cursor,travel)
            pygame.display.update()


    def transportMove(self, init, destiny, poss):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        if poss[0] < destiny.x:
            poss = (poss[0] + speed, poss[1])
        if poss[0] > destiny.x:
            poss = (poss[0] - speed, poss[1])
        if poss[0] == destiny.x:
            if poss[1] > destiny.y:
                poss = (poss[0], poss[1] - speed)
            if poss[1] < destiny.y:
                poss = (poss[0], poss[1] + speed)
        return poss

    def MoveImage(self, poss,init, destiny, carRight,carDown,carLeft,carUp):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        Orientation = carRight
        if poss[0] < destiny.x:
            Orientation = carRight
        if poss[0] > destiny.x:
            Orientation = carLeft
        if poss[0] == destiny.x:
            if poss[1] > destiny.y:
                Orientation = carUp
            if poss[1] < destiny.y:
                Orientation = carDown
        return Orientation

    def MoveCar(self, poss,init,airplaneRight,airplaneDown,airplaneLeft,airplaneUp):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        Orientation = airplaneRight
        if len(self.visited) is len(self.graph.place):
            self.visited.clear()
        for j in range(len(init.adjacencies)):
            if init.adjacencies[j].destiny not in self.visited:
                i = j
                break
        if poss[0] < init.adjacencies[i].destiny.x:
            Orientation = airplaneRight
        if poss[0] > init.adjacencies[i].destiny.x:
            Orientation = airplaneLeft
        if poss[0] == init.adjacencies[i].destiny.x:
            if poss[1] > init.adjacencies[i].destiny.y:
                Orientation = airplaneUp
            if poss[1] < init.adjacencies[i].destiny.y:
                Orientation = airplaneDown
        return Orientation


    def MoveDonkey(self, poss,init,donkeyRight,donkeyDown,donkeyLeft,donkeyUp):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        Orientation = donkeyRight
        if len(self.visited) is len(self.graph.place):
            self.visited.clear()
        for j in range(len(init.adjacencies)):
            if init.adjacencies[j].destiny not in self.visited:
                i = j
                break
        if poss[0] < init.adjacencies[i].destiny.x:
            Orientation = donkeyRight
        if poss[0] > init.adjacencies[i].destiny.x:
            Orientation = donkeyLeft
        if poss[0] == init.adjacencies[i].destiny.x:
            if poss[1] > init.adjacencies[i].destiny.y:
                Orientation = donkeyUp
            if poss[1] < init.adjacencies[i].destiny.y:
                Orientation = donkeyDown
        return Orientation

    def way(self, screenTK, id):
        if id == 1:
            self.mincost = True
        else:
            self.mintime = True
        screenTK.destroy()

    def transport(self, screen, transport):
        self.form = transport
        screen.destroy()

    def recopilarActividades(self,screenTK ,t):
        self.actividadesVertice.append(t)
        print (t.name)

    def min(self):
        men = self.visited[0]
        pas = True
        result = []
        variable = 0
        if self.mintime:
            variable = int(self.cost.get())
        else:
            variable = int(self.time.get())
        for node in self.visited:
            if node.status[0] > men.status[0] and men.status[0] < variable:
                men = node

        while pas:
            result.append(men)
            men = men.status[1]
            if self.graph.Get_Vertex(men.status[1]) is men:
                pas = False

        return result