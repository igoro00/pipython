from Animal import Animal
from Sheep import Sheep
from Herd import Herd
import cmath
import logging

logger = logging.getLogger(__name__)

class Wolf(Animal):
    herd: Herd
    def __init__(self, step: float, herd: Herd) -> None:
        self.herd = herd
        super().__init__(0+0j, step)
    
    @property
    def pos(self):
        return super().pos

    @pos.setter
    def pos(self, value: complex) -> None:
        self._pos = value
        logger.debug(f"Wolf moved to {self.pos}")
        logger.info("Wolf moved")

    def update(self) -> tuple[Sheep, bool]:
        closest_sheep, closest_dist = self.herd.closest_sheep(self.pos)
        logger.debug(f"Determined closest sheep: {closest_sheep}, distance: {closest_dist}")
        # kill sheep
        if closest_dist <= self.step:
            self.pos = closest_sheep.pos
            self.herd.kill(closest_sheep)
            return closest_sheep, True

        # run after a sheep
        self.pos += cmath.rect(self.step, cmath.phase(closest_sheep.pos-self.pos))
        logger.info(f"Wolf is chasing sheep {closest_sheep.i}")
        return closest_sheep, False

