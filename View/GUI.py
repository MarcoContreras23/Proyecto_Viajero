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
        self.cursor = Cursor()
        self.mintime = False
        self.mincost = False
        self.ways = False
        self.pas = False
        self.obs = False
        self.MinMoney = True
        self.visited = []

        self.actividadesVertice= []# esta lista se va a limpiar en cuanto se llame a el algoritmo que
        #resta el costo de las actividades al mochilero para seguir al siguiente nodo

        self.startRoute = True #para establecer cuando el mochilero comenzo su ruta y se le deben ofertar actividades y trabajos
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
        # texto de botones
        obstruccion = fuente.render("Obstruir camino", True, (0, 0, 0))
        way = fuente.render("Minimum way", True,(0,0,0))

        init = None
        poss = (0, 0)
        MinCost = []
        MinTime = []

        while True:
            """for donde se ejecutan los eventos"""
            display.fill((189, 195, 199))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    """for place in self.graph.place:
                        if self.cursor.colliderect(place.rect):
                            poss = (place.x, place.y)
                            init = place
                            self.pas = True"""
                #ventanas ofertar trabajos de cada nodo
                    if self.startRoute:
                        for places in self.graph.place:
                            if self.cursor.colliderect(places.rect):
                                screenTK = Tk()
                                size = self.screen_sizeW()
                                screenTK.geometry(
                                    f"200x200+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                                screenTK.title(
                                    "Select actividad")
                                x = 40
                                y = 0
                                for t in places.task:
                                    if t.type == "optional":s
                                        y+=30
                                        Button(screenTK, text=t.name,
                                            command=lambda: self.recopilarActividades(screenTK, t)).place(x=x,y= y)
                                screenTK.mainloop()



                    if self.cursor.colliderect(boton2.rect):
                        screenTK = Tk()
                        size = self.screen_sizeW()
                        screenTK.geometry(
                            f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK.title(
                            "Select way to show")
                        Button(screenTK, text="Way the minimun cost",
                               command = lambda: self.way(screenTK, 1)).place(x=20, y=20)
                        Button(screenTK, text="Way the minimun time",
                               command = lambda: self.way(screenTK, 2)).place(x=20, y=70)
                        screenTK.mainloop()
                    elif self.mintime:
                        self.ways = True
                        screenTK2 = Tk()
                        size = self.screen_sizeW()
                        screenTK2.geometry(
                            f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK2.title(
                            "Way whit the minimun time")
                        self.time = IntVar()
                        textT = StringVar(
                            value="Write the trip time.")
                        labelT = Label(
                            screenTK2, textvariable=textT).place(x=200, y=10)
                        Time_field = Entry(
                            screenTK2, textvariable=self.time, width=25).place(x=210, y=30)
                        Button(screenTK2, text="ok",
                               command=lambda :self.way(screenTK2,2).place(x = 30 , y= 60))
                        screenTK2.mainloop()
                    elif self.mincost:
                        self.ways = True
                        screenTK3 = Tk()
                        size = self.screen_sizeW()
                        screenTK3.geometry(
                            f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK3.title(
                            "Way whit the minimun cost")
                        self.cost = IntVar()
                        textC = StringVar(
                            value="Write the backpacker budget.")
                        labelC = Label(
                            screenTK3, textvariable=textC).place(x=5, y=10)
                        Cost_field = Entry(
                            screenTK3, textvariable=self.cost, width=25).place(x=10, y=30)
                        Button(screenTK3, text="OK",
                               command=lambda: screenTK3.destroy()).place(x=170, y=70)
                        screenTK3.mainloop()
                    if self.ways:
                        for place in self.graph.place:
                            if self.cursor.colliderect(place.rect):
                                if self.mincost:
                                    MinCost = self.graph.Dijkstra(
                                        place, True, False, int(self.cost.get()))
                                if self.mintime:
                                    MinTime = self.graph.Dijkstra(
                                        place, False, True, int(self.time.get()))
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
                                        edge.color = (0, 0, 255)
                                    if edge.origin is node and edge.destiny is self.graph.Get_Vertex(node.status[1]):
                                        edge.color = (0, 0, 255)
                            self.mintime = False
                        self.ways = False

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

                for j in range(0, len(self.graph.conection)):
                    pos = self.pos_peso(j)
                    origin = self.graph.conection[j].origin
                    destiny = self.graph.conection[j].destiny
                    self.graph.conection[j].line = (pygame.draw.line(display, (36, 113, 163),
                                                                     (origin.x,
                                                                      origin.y),
                                                                     (destiny.x,
                                                                      destiny.y),3))
                    if self.graph.conection[j].obs:
                        display.blit(dead, (pos[0], pos[1]))


                for i in range(0, len(self.graph.place)):
                    """grafica nodo"""
                    font = pygame.font.Font(None, 30)
                    scoretext = font.render(str(self.graph.place[i].name_city), 1, (0, 0, 0))
                    display.blit(scoretext, (self.graph.place[i].x - 64, self.graph.place[i].y - 64))
                    self.graph.place[i].line = display.blit(city, (self.graph.place[i].x - 30,self.graph.place[i].y - 40))
            if self.pas:
                Orientation = self.MoveImage(poss, init, airplaneRight, airplaneDown, airplaneLeft, airplaneUp)
                Orientation2 = self.MoveCar(poss,init, carRight, carDown, carLeft, carUp)
                orientation3 = self.MoveDonkey(poss,init,donkeyRight,donkeyDown,donkeyLeft,donkeyUp)
                display.blit(Orientation, (poss[0] - 30, poss[1] - 30))
                for place in self.graph.place:
                    if place.x == poss[0] and place.y == poss[1]:
                        init = place
                poss = self.transportMove(init, poss)

            self.cursor.update()
            boton.update(display, self.cursor, obstruccion)
            boton2.update(display, self.cursor, way)
            pygame.display.update()


    def pos_peso(self, j):

                if self.graph.conection[j].origin.x < self.graph.conection[j].destiny.x:
                    posx = self.graph.conection[j].origin.x + \
                           ((self.graph.conection[j].destiny.x - self.graph.conection[j].destiny.x) / 2)
                    tipo = 1
                else:
                    posx = self.graph.conection[j].destiny.x + \
                           ((self.graph.conection[j].origin.x - self.graph.conection[j].destiny.x) / 2)
                    tipo = 2
                if self.graph.conection[j].origin.y < self.graph.conection[j].destiny.y:
                    posy = self.graph.conection[j].origin.y + \
                           ((self.graph.conection[j].destiny.y - self.graph.conection[j].origin.y) / 2)
                    tipo2 = 1
                else:
                    posy = self.graph.conection[j].destiny.y + \
                           ((self.graph.conection[j].origin.y - self.graph.conection[j].destiny.y) / 2)
                    tipo2 = 2

                if (tipo is 1 and tipo2 is 1) or (tipo is 2 and tipo2 is 2):
                        posx += -13
                        posy += -20
                elif (tipo is 1 and tipo2 is 2) or (tipo is 2 and tipo2 is 1):
                        posx += -13
                        posy += -30
                pos = [posx, posy]

                return pos

    def transportMove(self, init, poss):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        #pas = False
        if len(self.visited) is len(self.graph.place):
            self.visited.clear()
        for j in range(len(init.adjacencies)):
            if init.adjacencies[j].destiny not in self.visited:
                i = j
                break
        if poss[0] < init.adjacencies[i].destiny.x:
            poss = (poss[0] + speed, poss[1])
        if poss[0] > init.adjacencies[i].destiny.x:
            poss = (poss[0] - speed, poss[1])
        if poss[0] == init.adjacencies[i].destiny.x:
            if poss[1] > init.adjacencies[i].destiny.y:
                poss = (poss[0], poss[1] - speed)
            if poss[1] < init.adjacencies[i].destiny.y:
                poss = (poss[0], poss[1] + speed)
        return poss

    def MoveImage(self, poss,init,carRight,carDown,carLeft,carUp):
        if init not in self.visited:
            self.visited.append(init)
        speed = 2
        i = 0
        Orientation = carRight
        if len(self.visited) is len(self.graph.place):
            self.visited.clear()
        for j in range(len(init.adjacencies)):
            if init.adjacencies[j].destiny not in self.visited:
                i = j
                break
        if poss[0] < init.adjacencies[i].destiny.x:
            Orientation = carRight
        if poss[0] > init.adjacencies[i].destiny.x:
            Orientation = carLeft
        if poss[0] == init.adjacencies[i].destiny.x:
            if poss[1] > init.adjacencies[i].destiny.y:
                Orientation = carUp
            if poss[1] < init.adjacencies[i].destiny.y:
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