import random
from typing import List, Tuple, Optional
from enum import Enum

class CellState(Enum):
    EMPTY = "."
    SHIP = "S"
    HIT = "X"
    MISS = "O"
    
class Ship:
    def __init__(self, name: str, size: int):
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
    
    
class Board:
    def _init_(self, size: int):
        self.size = size
        self.grid = [[CellState.EMPTY for _ in range(size)] 
                     for _ in range(size)]
        self.ships: List[Ship] = []

    def is_valid_position(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size

    def can_place_ship(self, row: int, col: int, 
                       size: int, horizontal: bool) -> bool:
        if horizontal:
            if col + size > self.size:
                return False
            for c in range(col, col + size):
                if not self.is_valid_position(row, c):
                    return False
                if self.grid[row][c] != CellState.EMPTY:
                    return False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = row + dr, c + dc
                        if self.is_valid_position(nr, nc):
                            if self.grid[nr][nc] == CellState.SHIP:
                                return False
        else:
            if row + size > self.size:
                return False
            for r in range(row, row + size):
                if not self.is_valid_position(r, col):
                    return False
                if self.grid[r][col] != CellState.EMPTY:
                    return False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nr, nc = r + dr, col + dc
                        if self.is_valid_position(nr, nc):
                            if self.grid[nr][nc] == CellState.SHIP:
                                return False
        return True

    def place_ship(self, ship: Ship, row: int, col: int, 
                   horizontal: bool) -> bool:
        if not self.can_place_ship(row, col, ship.size, horizontal):
            return False

        if horizontal:
            for c in range(col, col + ship.size):
                self.grid[row][c] = CellState.SHIP
                ship.add_position(row, c)
        else:
            for r in range(row, row + ship.size):
                self.grid[r][col] = CellState.SHIP
                ship.add_position(r, col)

        self.ships.append(ship)
        return True

    def place_ship_random(self, ship: Ship) -> bool:
        attempts = 0
        max_attempts = 1000
        while attempts < max_attempts:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            horizontal = random.choice([True, False])
            if self.place_ship(ship, row, col, horizontal):
                return True
            attempts += 1
        return False

    def make_shot(self, row: int, col: int) -> Tuple[bool, Optional[Ship]]:
        if not self.is_valid_position(row, col):
            return False, None

        if self.grid[row][col] in [CellState.HIT, CellState.MISS]:
            return False, None

        if self.grid[row][col] == CellState.SHIP:
            self.grid[row][col] = CellState.HIT
            for ship in self.ships:
                if ship.contains(row, col):
                    ship.hits += 1
                    return True, ship
        else:
            self.grid[row][col] = CellState.MISS

        return True, None

    def all_ships_sunk(self) -> bool:
        return all(ship.is_sunk() for ship in self.ships)

    def get_display_grid(self, hide_ships: bool = False) -> List[List[str]]:
        display = []
        for row in self.grid:
            display_row = []
            for cell in row:
                if cell == CellState.SHIP and hide_ships:
                    display_row.append(CellState.EMPTY.value)
                else:
                    display_row.append(cell.value)
            display.append(display_row)
        return display