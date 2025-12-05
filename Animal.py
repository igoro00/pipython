class Animal():
    pos:complex
    step:float
    alive: bool = True
    
    def __init__(self, pos: complex, step:float) -> None:
        self.pos = pos
        self.step = step

    
    def dist(self, other: complex) -> float:
        return abs(self.pos - other)
    
    def json_pos(self) -> tuple[float, float] | None:
        if self.alive:
            return (self.pos.real, self.pos.imag)