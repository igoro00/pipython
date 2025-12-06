class Animal():
    _pos:complex
    step:float
    
    def __init__(self, pos: complex, step:float) -> None:
        self.pos = pos
        self.step = step

    @property
    def pos(self) -> complex:
        return self._pos
    
    @pos.setter
    def pos(self, value: complex) -> None:
        self._pos = value
    
    def dist(self, other: complex) -> float:
        return abs(self.pos - other)
    
    def json_pos(self) -> tuple[float, float]:
        return (self.pos.real, self.pos.imag)