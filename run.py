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
    
class GameController:
    def _init_(self):
        self.grid_size = 10
        self.player_board: Optional[Board] = None
        self.computer_board: Optional[Board] = None
        self.ship_config = [
            ("Aircraft Carrier", 5),
            ("Battleship", 4),
            ("Cruiser", 3),
            ("Submarine", 3),
            ("Destroyer", 2)
        ]

    def setup_game(self, size: int):
        self.grid_size = max(5, min(size, 15))
        self.player_board = Board(self.grid_size)
        self.computer_board = Board(self.grid_size)
        self._place_computer_ships()
        self._place_player_ships()

    def _place_computer_ships(self):
        for name, size in self.ship_config:
            ship = Ship(name, size)
            if not self.computer_board.place_ship_random(ship):
                raise RuntimeError("Failed to place computer ships")

    def _place_player_ships(self):
        for name, size in self.ship_config:
            ship = Ship(name, size)
            if not self.computer_board.place_ship_random(ship):
                raise RuntimeError("Failed to place player ships")

    def parse_coordinate(self, input_str: str) -> Optional[Tuple[int, int]]:
        input_str = input_str.strip().upper()
        if len(input_str) < 2:
            return None

        try:
            if input_str[0].isalpha():
                col = ord(input_str[0]) - ord('A')
                row = int(input_str[1:]) - 1
            else:
                row = int(input_str[:-1]) - 1
                col = ord(input_str[-1]) - ord('A')

            if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
                return (row, col)
        except (ValueError, IndexError):
            pass

        return None

    def display_boards(self):
        print("\n" + "=" * 80)
        print("YOUR BOARD".center(80))
        print("=" * 80)
        self._print_board(self.player_board, False)

        print("\n" + "=" * 80)
        print("COMPUTER BOARD (Your Shots)".center(80))
        print("=" * 80)
        self._print_board(self.computer_board, True)

    def _print_board(self, board: Board, hide_ships: bool):
        display = board.get_display_grid(hide_ships)
        header = "   " + " ".join([chr(65 + i) for i in range(board.size)])
        print(header)
        for i, row in enumerate(display):
            row_num = str(i + 1).rjust(2)
            row_str = " ".join(row)
            print(f"{row_num} {row_str}")

    def get_player_shot(self) -> Tuple[int, int]:
        while True:
            print("\nEnter coordinates (e.g., A1, B5): ", end="")
            try:
                user_input = input().strip()
            except EOFError:
                print("\nGame ended.")
                exit(0)

            coord = self.parse_coordinate(user_input)
            if coord is None:
                print("Invalid coordinates! Use format like A1 or 1A")
                print(f"Grid size is {self.grid_size}x{self.grid_size}")
                continue

            row, col = coord
            if not self.computer_board.is_valid_position(row, col):
                print(f"Coordinates out of bounds! Grid is {self.grid_size}x{self.grid_size}")
                continue

            if self.computer_board.grid[row][col] in [CellState.HIT, CellState.MISS]:
                print("You already shot there! Try another coordinate.")
                continue

            return row, col

    def get_computer_shot(self) -> Tuple[int, int]:
        while True:
            row = random.randint(0, self.grid_size - 1)
            col = random.randint(0, self.grid_size - 1)
            if self.player_board.grid[row][col] not in [CellState.HIT, CellState.MISS]:
                return row, col

    def play_turn(self) -> bool:
        self.display_boards()

        row, col = self.get_player_shot()
        success, ship = self.computer_board.make_shot(row, col)

        if success:
            if ship:
                if ship.is_sunk():
                    print(f"\nHit! You sunk the {ship.name}!")
                else:
                    print("\nHit!")
            else:
                print("\nMiss!")

        if self.computer_board.all_ships_sunk():
            print("\n" + "=" * 80)
            print("CONGRATULATIONS! You won!".center(80))
            print("=" * 80)
            return False

        row, col = self.get_computer_shot()
        success, ship = self.player_board.make_shot(row, col)

        if success:
            if ship:
                if ship.is_sunk():
                    print(f"\nComputer hit! Your {ship.name} was sunk!")
                else:
                    print("\nComputer hit your ship!")
            else:
                print("\nComputer missed!")

        if self.player_board.all_ships_sunk():
            print("\n" + "=" * 80)
            print("GAME OVER! Computer won!".center(80))
            print("=" * 80)
            return False

        return True