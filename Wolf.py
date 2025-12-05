from Animal import Animal
from Sheep import Sheep
import random
import cmath

class Wolf(Animal):
    sheep: list[Sheep]
    def __init__(self, step: float, sheep: list[Sheep]) -> None:
        self.sheep = sheep
        super().__init__(0+0j, step)

    def update(self):
        closestSheep = self.sheep[0]
        closestDist = self.sheep[0].dist(self.pos)
        for s in self.sheep[1:]:
            d = s.dist(self.pos)
            if d < closestDist:
                closestSheep = s
                closestDist = d
        
        if closestDist <= self.step:
            self.pos = closestSheep.pos
            return

        self.pos = cmath.rect(self.step, cmath.phase(self.pos))
