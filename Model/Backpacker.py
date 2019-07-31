class Backpacker:
    def __init__(self):
        self.budget = 0
        self.time = 0
        self.porcentaje_minimo = self.budget * 0.4
        self.work = self.getWork()
        self.position = None

    def getWork(self):
        if self.budget < self.porcentaje_minimo:
            return True
        else:
            return False


