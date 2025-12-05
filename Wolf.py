from Animal import Animal
from Sheep import Sheep
from Herd import Herd
import random
import cmath

class Wolf(Animal):
    herd: Herd
    def __init__(self, step: float, herd: Herd) -> None:
        self.herd = herd
        super().__init__(0+0j, step)

    def update(self) -> tuple[Sheep, bool]:
        closest_sheep, closest_dist = self.herd.closest_sheep(self.pos)
        
        # kill sheep
        if closest_dist <= self.step:
            self.pos = closest_sheep.pos
            closest_sheep.kill()
            return closest_sheep, True

        # run after a sheep
        self.pos += cmath.rect(self.step, cmath.phase(closest_sheep.pos-self.pos))
        return closest_sheep, False

