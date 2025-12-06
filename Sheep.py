from Animal import Animal
import random
import logging
logger = logging.getLogger(__name__)
class Sheep(Animal):
    def __init__(self, spawn_limit:float, step: float, i: int) -> None:
        pos = complex(
            random.uniform(-spawn_limit, spawn_limit), 
            random.uniform(-spawn_limit, spawn_limit)
        )
        self.i = i
        super().__init__(pos, step)

    @property
    def pos(self):
        return super().pos

    @pos.setter
    def pos(self, value: complex) -> None:
        self._pos = value
        logger.debug(f"Sheep {self.i} moved to {self.pos}")

    def update(self):
        direction = random.choice(list({
            "RIGHT":(1+0j), # right
            "UP":(0+1j), # up
            "DOWN":(0-1j), # down
            "LEFT":(-1+0j) # left
        }.items()))
        logger.debug(f"Sheep {self.i} chose direction ${direction[0]}")
        self.pos += (direction[1] * self.step)