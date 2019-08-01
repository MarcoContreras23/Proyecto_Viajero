from pygame import Rect


class Conection:
    def __init__(self,origin ,destiny,distance ,x,y,transport):
        self.origin = origin
        self.destiny = destiny
        self.distance = distance
        self.transport = transport
        self.bi = False
        self.obs = False
        self.line = None
        self.rect = Rect(x, y, 60, 40)
        self.color = (36, 113, 163)
#        self.rect = Rect(origin.rect.x,destiny.rect.y,20,20)
