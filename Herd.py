from Sheep import Sheep
from math import inf

class Herd():
    sheep: list[Sheep] = []

    def __init__(self, n_sheep: int, sheep_step: float, spawn_limit:float) -> None:
        for _ in range(n_sheep):
            self.sheep.append(Sheep(spawn_limit, sheep_step))
    

    # TODO: should probably be memoized
    @property
    def alive_sheep(self):
        return [x for x in self.sheep if x.alive]
    
    def kill(self, s: Sheep):
        # TODO: update alive_sheep
        s.kill()

    def closest_sheep(self, pos: complex):
        out: Sheep | None = None
        min_dist = inf
        for s in self.alive_sheep:
            if not s.alive:
                continue
            dist = s.dist(pos)
            if dist < min_dist:
                min_dist = dist
                out = s
        if out is None:
            raise RuntimeError("Couldn't find the closest sheep")
        return out, min_dist
