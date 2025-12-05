from Animal import Animal
import random

class Sheep(Animal):
    def __init__(self, spawn_limit:float, step: float) -> None:
        pos = complex(
            random.uniform(-spawn_limit, spawn_limit), 
            random.uniform(-spawn_limit, spawn_limit)
        )
        super().__init__(pos, step)

    def update(self) -> None:
        direction = random.choice([
            (1+0j), # right
            (0+1j), # up
            (0-1j), # down
            (-1+0j) # left
        ])
        self.pos += (direction * self.step)