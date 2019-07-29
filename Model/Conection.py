from pygame import Rect


class Conection:
    def __init__(self,origin ,destiny ,x,y,transport,Distance = 0):
        self.origin = origin
        self.destiny = destiny
        self.distance = Distance
        self.transport = transport
        self.bi = False
        self.obs = False
        self.rect = Rect(x, y, 60, 40)
#        self.rect = Rect(origin.rect.x,destiny.rect.y,20,20)
