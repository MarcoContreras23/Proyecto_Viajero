class Backpacker:
    def __init__(self,budget,time):
        self.budget = budget
        self.time = time
        self.porcentaje_minimo = self.budget * 0.4
        self.work = self.getWork()
        self.position = None

    def getWork(self):
        if self.budget < self.porcentaje_minimo:
            return True
        else:
            return False


