class CellState(Enum):
    EMPTY = "."
    SHIP = "S"
    HIT = "X"
    MISS = "O"
    
class Ship:
    def _init_(self, name: str, size: int):
        self.name = name
        self.size = size
        self.positions: List[Tuple[int, int]] = []
        self.hits: int = 0

    def is_sunk(self) -> bool:
        return self.hits >= self.size

    def add_position(self, row: int, col: int):
        self.positions.append((row, col))

    def contains(self, row: int, col: int) -> bool:
        return (row, col) in self.positions
    
    
