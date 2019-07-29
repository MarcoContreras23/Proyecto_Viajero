import sys
from tkinter import *
import threading
from pygame.locals import *
from Principal.Button import *
from Principal.Cursor import *
import ctypes
from pygame import Rect

pygame.init()
pygame.font.init()


class GUI:

    def __init__(self,graph):
        self.graph = graph
        self.x = 0
        self.y = 0
        self.cursor = Cursor()
        self.obs = False
        self.visited = []
        self.MinMoney = True
        self.pas = False
        thread = threading.Thread(self.all())
        thread.start()

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
        van = pygame.image.load("..\\Resource\\van.png")
        vanLeft = pygame.image.load("..\\Resource\\vanLeft.png")
        vanUp = pygame.image.load("..\\Resource\\vanUp.png")
        vanDown = pygame.image.load("..\\Resource\\vanDown.png")
        # Donkey
        donkey = pygame.image.load("..\\Resource\\donkey.png")
        donkeyLeft = pygame.image.load("..\\Resource\\donkeyLeft.png")
        donkeyUp = pygame.image.load("..\\Resource\\donkeyUp.png")
        donkeyDown = pygame.image.load("..\\Resource\\donkeyDown.png")
        # Airplane
        airplane = pygame.image.load("..\\Resource\\airplanes.png")
        airplaneLeft = pygame.image.load("..\\Resource\\airplanesLeft.png")
        airplaneUp = pygame.image.load("..\\Resource\\airplanesUp.png")
        airplaneDown = pygame.image.load("..\\Resource\\airplanesDown.png")

        # escala las imagenes
        button = pygame.transform.scale(button, (140, 75))
        button2 = pygame.transform.scale(button, (110, 90))
        # Asignacion de botones
        boton = Button(button, button2, 300, 60)
        boton2 = Button(button, button2, 440, 60)
        # texto de botones
        obstruccion = fuente.render("Obstruir camino", True, (0, 0, 0))
        way = fuente.render("Minimum way", True,(0,0,0))


        init = None
        poss = (0, 0)

        while True:
            """for donde se ejecutan los eventos"""
            display.fill((189, 195, 199))
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for place in self.graph.place:
                        if self.cursor.colliderect(place.rect):
                            poss = (place.x, place.y)
                            init = place
                            self.pas = True
                    if self.cursor.colliderect(boton2.rect):
                        screenTK = Tk()
                        size = self.screen_sizeW()
                        screenTK.geometry(
                            f"430x110+{int(size[0] / 2) - 230}+{int(size[1] / 2) - 100}")
                        screenTK.title("Minimum way")
                        self.cost = IntVar()
                        self.time = IntVar()
                        textCost = StringVar(
                            value="Choose the cost between city and city")
                        textTime = StringVar(
                            value="Choose the time between city and city"
                        )
                        labelCost = Label(
                            screenTK, textvariable=textCost).place(x=5, y=5)
                        labelTime = Label(
                            screenTK, textvariable = textTime).place(x = 10 , y = 50)

                        Time_field = Entry(
                            screenTK, textvariable = self.time, width = 25).place(x = 10, y = 70)
                        Cost_field = Entry(
                            screenTK, textvariable=self.cost, width=25).place(x=10, y=30)
                        screenTK.mainloop()

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
            if self.pas:
                display.blit(van, poss)
                for place in self.graph.place:
                    if place.x == poss[0] and place.y == poss[1]:
                        init = place
                poss = self.transportMove(init, poss)


            """for  node in self.graph.place:
                if poss[0] < node.x:
                    poss = (poss[0] + speed , poss[1])#x
                if poss[0] > node.x:
                    poss = (poss[0] - speed , poss[1])
                if poss[0] == node.x:
                    if poss[1] > node.y:
                        poss = (poss[0] , poss[1] - speed)
                    if poss[1] < node.y:
                        poss = (poss[0] , poss[1] + speed)
                """

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
                poss = (poss[0] + speed, poss[1])  # x
            if poss[0] > init.adjacencies[i].destiny.x:
                poss = (poss[0] - speed, poss[1])
            if poss[0] == init.adjacencies[i].destiny.x:
                if poss[1] > init.adjacencies[i].destiny.y:
                    poss = (poss[0], poss[1] - speed)
                if poss[1] < init.adjacencies[i].destiny.y:
                    poss = (poss[0], poss[1] + speed)
        return poss