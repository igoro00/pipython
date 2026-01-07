from Sheep import Sheep
from math import inf
import logging

logger = logging.getLogger(__name__)

class Herd():
    sheep: list[Sheep] = []
    n_sheep: int
    def __init__(self, n_sheep: int, sheep_step: float, spawn_limit:float) -> None:
        self.n_sheep = n_sheep
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
    
    def json_sheep_pos(self):
        out = [None] * self.n_sheep
        for s in self.sheep:
            out[s.i] = s.json_pos()
        return out