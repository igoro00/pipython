from Sheep import Sheep
from math import inf
import logging

logger = logging.getLogger(__name__)

class Herd():
    sheep: list[Sheep] = []

    def __init__(self, n_sheep: int, sheep_step: float, spawn_limit:float) -> None:
        for i in range(n_sheep):
            self.sheep.append(Sheep(spawn_limit, sheep_step, i))
    
    def kill(self, s: Sheep):
        logger.info(f"Sheep {s.i} has been eaten")
        self.sheep.remove(s)

    def closest_sheep(self, pos: complex):
        out: Sheep | None = None
        min_dist = inf
        for s in self.sheep:
            dist = s.dist(pos)
            if dist < min_dist:
                min_dist = dist
                out = s
        if out is None:
            raise RuntimeError("Couldn't find the closest sheep")
        return out, min_dist

    def update(self):
        for s in self.sheep:
            s.update()