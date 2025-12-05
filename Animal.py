class Animal():
    pos:complex
    step:float
    
    def __init__(self, pos: complex, step:float) -> None:
        self.pos = pos
        self.pos = step

    def update(self) -> None:
        raise NotImplementedError()
    
    def dist(self, other: complex) -> float:
        return abs(self.pos - other)