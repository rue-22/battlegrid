from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum, IntEnum, auto
from typing import Self, Sequence


class NetworkID(IntEnum):
    Blue = 1
    Red = 2


class Side(IntEnum):
    RED = auto()
    BLUE = auto()


class GameVerdict(StrEnum):
    CONTINUE = 'CONTINUE'
    DRAW = 'DRAW'
    RED_WINNER = 'RED_WINNER'
    BLUE_WINNER = 'BLUE_WINNER'


class MessageType(IntEnum):
    PLAYER_IN = 1
    SEND_CONFIG = 2
    MADE_ACTION = 3


@dataclass
class Location:
    row: int
    col: int

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Location):
            return False
        return self.row == other.row and self.col == other.col

    def __mul__(self, n: int) -> Location:
        return Location(self.row * n, self.col * n)


@dataclass 
class Tile: 
    piece: Piece | None
    walkable: bool


class Action(IntEnum):
    MOVE = auto()
    DROP = auto()


class Movement: 
    FORWARD = [Location(-1, 0)]
    FORWARD_DIAGONALS = [Location(-1, -1), Location(-1, +1)]

    BACKWARD = [Location(+1, 0)]
    BACKWARD_DIAGONALS = [Location(+1, -1), Location(+1, +1)] 

    SIDES = [Location(0, -1), Location(0, +1)]

    def get_deltas(self) -> list[Location]:
        ...


# movements are always relative to the BLUE side (bottom side)
class SwordsmanMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return [
            *self.FORWARD, 
            *self.FORWARD_DIAGONALS,
        ]


class LongswordMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return  [
            *self.BACKWARD, 
            *self.BACKWARD_DIAGONALS, 
            *self.FORWARD, 
            *(loc * 2 for loc in self.FORWARD),
        ]


class MageMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return [
            *self.FORWARD,
            *self.FORWARD_DIAGONALS,
            *self.BACKWARD,
            *self.BACKWARD_DIAGONALS,
            *(loc * 2 for loc in self.FORWARD),
            *(loc * 2 for loc in self.FORWARD_DIAGONALS),
        ]


class ArcherMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return [
            *self.BACKWARD,
            *self.BACKWARD_DIAGONALS,
            *(loc * 3 for loc in self.FORWARD),
            *(loc * 4 for loc in self.FORWARD),
        ]


class GuardMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return [
            *self.FORWARD,
            *self.FORWARD_DIAGONALS,
            *self.BACKWARD,
            *self.BACKWARD_DIAGONALS, 
            *self.SIDES,
        ]


class CrystalMovement(Movement):
    def get_deltas(self) -> list[Location]:
        return [
            *self.FORWARD,
            *self.BACKWARD,
            *self.SIDES,
        ]


class PieceKind(StrEnum):
    SWORDSMAN = 'Swordsman'
    MAGE = 'Mage'
    ARCHER = 'Archer'
    GUARD = 'Guard'
    LONGSWORD = 'Longsword'
    CRYSTAL = 'Crystal'


piece_mappings: dict[PieceKind, tuple[PieceKind, Movement]] = {
    PieceKind.SWORDSMAN: (PieceKind.SWORDSMAN, SwordsmanMovement()),
    PieceKind.MAGE: (PieceKind.MAGE, MageMovement()),
    PieceKind.ARCHER: (PieceKind.ARCHER, ArcherMovement()),
    PieceKind.GUARD: (PieceKind.GUARD, GuardMovement()),
    PieceKind.LONGSWORD: (PieceKind.LONGSWORD, LongswordMovement()),
    PieceKind.ARCHER: (PieceKind.ARCHER, ArcherMovement()),
    PieceKind.CRYSTAL: (PieceKind.CRYSTAL, CrystalMovement()),
}


class Player:
    def __init__(self, side: Side):
        self.side = side
        self.stored_pieces: dict[PieceKind, list[Piece]] = {
            PieceKind.SWORDSMAN: [],
            PieceKind.MAGE: [],
            PieceKind.ARCHER: [],
            PieceKind.GUARD: [],
            PieceKind.LONGSWORD: [],
        }

    def capture_piece(self, piece: Piece):
        '''Append captured piece to list of available pieces'''
        piece.side = self.side
        self.stored_pieces[piece.piece_kind].append(piece)

    def use_piece(self, piece: Piece):
        '''Use a piece that you have stored'''
        if len(self.stored_pieces[piece.piece_kind]) == 0:
            print('cannot use a piece that you don\'t have')
            return
        self.stored_pieces[piece.piece_kind].pop()


class Piece:
    def __init__(self, piece_info: tuple[PieceKind, Movement], location: Location, side: Side, is_protected_piece: bool = False):
        self._piece_kind, self._movement = piece_info
        self.side = side
        self.location = location
        self._is_protected_piece = is_protected_piece

    def can_move(self, to: Location) -> bool:
        '''Checks if a piece can move to a certain location'''
        return any(
            True for loc in self.correct_orientation(self._movement.get_deltas())
            if self.location.row + loc.row == to.row and
            self.location.col + loc.col == to.col
        )

    @property
    def piece_kind(self):
        return self._piece_kind

    @property
    def is_protected_piece(self):
        return self._is_protected_piece

    @property
    def all_possible_moves(self) -> list[Location]:
        return [Location(self.location.row + loc.row, self.location.col + loc.col) 
         for loc in self.correct_orientation(self._movement.get_deltas())]

    def correct_orientation(self, deltas: list[Location]) -> list[Location]:
        '''Reverses orientation when at red side'''
        if self.side == Side.RED:
            return [Location(-loc.row, -loc.col) for loc in deltas]
        return deltas


class GameState:
    @classmethod
    def new_board(cls, variant: int) -> Self:
        if variant == 1:
            board = RushBoard()
        elif variant == 2:
            board = WarBoard()
        elif variant == 3:
            board = PrimeBoard()
        elif variant == 4:
            board = ClassicBoard()
        else: 
            raise RuntimeError(f"Invalid variant")

        return cls(board)
    
    def __init__(self, board: Board, max_moves: int=3):
        self.red_player = Player(Side.RED)
        self.blue_player = Player(Side.BLUE)
        self.curr_player = self.blue_player         # blue side ALWAYS go first

        self.board = board
        self.moves_made = 0
        self._max_moves = max_moves 
        self.game_verdict = GameVerdict.CONTINUE

        #NETWORKING STATES
        self._network_id = 0
        self.is_P2_connected = False
        self.P1board_variant = 0                    # 0 means P1 did not yet choose

    def new_game(self) -> Self:
        return self.new_board(self.board.variant)
    
    def assign_networkID(self, nid: int): 
        self._network_id = nid

    @property 
    def network_id(self):
        return self._network_id
    
    @property
    def max_moves(self):
        return self._max_moves


'''
To add a new board variant:
- inherit Board class
- assign an integer to the "variant" property
- add texture configuration at sprites.py in the "boardtextures" dictionary
- make sure the texture configuration and board dimensions is consistent
- Let ClassicBoard = 1, format of "boardtextures" key and value can be referred at sprites.py
'''
class Board:
    def __init__(self, rows: int, cols: int, impassable_terrain: list[Location], variant: int):
        self._rows = rows
        self._cols = cols
        self._variant = variant
        self._impassable_terrain: list[Location] = impassable_terrain
        self._grid: list[list[Tile]] = [[Tile(None, False) if Location(i,j) in self._impassable_terrain else Tile(None, True) for j in range(self._cols)] for i in range(self._rows)]
        self.red_crystals: list[Piece] = []
        self.blue_crystals: list[Piece] = []
    
    def get_tile(self, location: Location) -> Tile:
        return self._grid[location.row][location.col]
    
    def get_piece(self, location: Location) -> Piece | None:
        return self.get_tile(location).piece

    # NOTE: how do we notify user of an error when placing a piece on invalid locations
    def place_piece(self, piece: Piece, location: Location):
        '''Places a specific piece at a particular location (if valid)'''
        if not self.is_valid_location(location):
            print('cannot place a piece at an invalid location')
            return
        if location in self._impassable_terrain:
            print('cannot place a piece on impassable terrain')
            return
        if self.get_tile(location).piece is not None:
            print('cannot place a piece on an occupied location')
            return
        # update crystals list
        if piece.piece_kind == PieceKind.CRYSTAL:
            crystals = self.blue_crystals if piece.side == Side.BLUE else self.red_crystals
            for c in crystals:
                if c.side == piece.side and c.location == piece.location:
                    c.location = location

        piece.location = location
        self.get_tile(location).piece = piece

    def remove_piece(self, location: Location):
        '''Removes a piece at a specified location'''
        if not self.is_valid_location(location):
            print('cannot remove a piece at an invalid location')
        self.get_tile(location).piece = None

    def is_valid_location(self, location: Location) -> bool:
        '''Checks if a location is valid (i.e., it doesn't goes out of range)'''
        if location.row >= self._rows or location.row < 0:
            return False
        elif location.col >= self._cols or location.col < 0:
            return False
        return True

    def is_valid_move(self, piece: Piece, to: Location) -> bool:
        '''Checks if a move is valid'''
        # location is invalid
        if not self.is_valid_location(to):
            return False
        # location is impassable terratin 
        if not self.get_tile(to).walkable:
            return False

        target = self.get_piece(to)
        # protected pieces can only move but cannot capture/eat other pieces
        if piece.is_protected_piece:
            return True if not target else False
        if target:
            # protected piece or ally piece
            return not (target.piece_kind == PieceKind.CRYSTAL or piece.side == target.side)
        # no target
        return True

    def get_valid_moves(self, piece: Piece) -> list[Location]:
        '''Filters all valid moves from all possible moves'''
        movelist = piece.all_possible_moves
        return [move for move in movelist if self.is_valid_move(piece, move)]
    
    def get_valid_drops(self) -> list[Location]:
        '''Gets all possible and valid drop locations'''
        all_crystals = self.red_crystals + self.blue_crystals
        valid_crystal_moves: list[Location] = []
        for crystal in all_crystals:
            valid_crystal_moves += self.get_valid_moves(crystal)

        restricted_locations = self.impassable_terrain + valid_crystal_moves

        droplist: list[Location] = []
        for i in range(self._rows):
            for j in range(self._cols):
                if self.get_piece(Location(i,j)) is None and Location(i,j) not in restricted_locations:
                    droplist.append(Location(i,j))
        
        return droplist 

    def _initialize_pieces(self, initial_positions: Sequence[Sequence[str | None]]):
        guard = piece_mappings[PieceKind.GUARD]
        mage = piece_mappings[PieceKind.MAGE]
        archer = piece_mappings[PieceKind.ARCHER]
        swordsman = piece_mappings[PieceKind.SWORDSMAN]
        longsword = piece_mappings[PieceKind.LONGSWORD]
        crystal = piece_mappings[PieceKind.CRYSTAL]

        for r in range(self.rows):
            for c in range(self.cols):
                piece = initial_positions[r][c]
                if piece:
                    side = Side.RED if piece[0] == 'R' else Side.BLUE
                    match piece[1]:
                        case 'G':
                            self.place_piece(Piece(guard, Location(r, c), side), Location(r, c))
                        case 'M':
                            self.place_piece(Piece(mage, Location(r, c), side), Location(r, c))
                        case 'A':
                            self.place_piece(Piece(archer, Location(r, c), side), Location(r, c))
                        case 'S':
                            self.place_piece(Piece(swordsman, Location(r, c), side), Location(r, c))
                        case 'L':
                            self.place_piece(Piece(longsword, Location(r, c), side), Location(r, c))
                        case 'C':
                            crystal_piece = Piece(crystal, Location(r, c), side, True)
                            self.red_crystals.append(crystal_piece) if side == side.RED else self.blue_crystals.append(crystal_piece)
                            self.place_piece(crystal_piece, Location(r, c))
                        case _:
                            pass
                
    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def variant(self) -> int:
        return self._variant

    @property
    def impassable_terrain(self) -> list[Location]:
        return self._impassable_terrain


class RushBoard(Board): 
    def __init__(self):
        rows = 16
        cols = 10
        variant = 1
        impassable_terrain = [
            Location(4, 0), 
            Location(4, 1), 
            Location(4, 2), 
            Location(4, 7), 
            Location(4, 8), 
            Location(4, 9), 
            Location(5, 0), 
            Location(5, 1), 
            Location(5, 2), 
            Location(5, 7), 
            Location(5, 8), 
            Location(5, 9), 
            Location(10, 0), 
            Location(10, 1), 
            Location(10, 2), 
            Location(10, 7), 
            Location(10, 8), 
            Location(10, 9), 
            Location(11, 0), 
            Location(11, 1), 
            Location(11, 2), 
            Location(11, 7), 
            Location(11, 8), 
            Location(11, 9)
        ]
        super().__init__(rows, cols, impassable_terrain, variant)
        self._initialize_board()

    def _initialize_board(self):
        initial_positions: list[list[str | None]] = [
            ['RG', None, None, None, None, None, None, None, None, 'RG'],
            [None, None, 'RC', None, 'RM', 'RM', None, 'RC', None, None],
            [None, 'RG', None, 'RG', None, None, 'RG', None, 'RG', None],
            ['RA', 'RA', 'RA', None, None, None, None, 'RA', 'RA', 'RA'],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, 'RL', 'RL', 'RL', 'RL', None, None, None],
            ['RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS'],
            [None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            ['BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS'],
            [None, None, None, 'BL', 'BL', 'BL', 'BL', None, None, None],
            [None, None, None, None, None, None, None, None, None, None],
            ['BA', 'BA', 'BA', None, None, None, None, 'BA', 'BA', 'BA'],
            [None, 'BG', None, 'BG', None, None, 'BG', None, 'BG', None],
            [None, None, 'BC', None, 'BM', 'BM', None, 'BC', None, None],
            ['BG', None, None, None, None, None, None, None, None, 'BG'],
        ]

        self._initialize_pieces(initial_positions)


class WarBoard(Board): 
    def __init__(self):
        rows = 19
        cols = 13
        variant = 2
        impassable_terrain = [
            Location(0, 5),
            Location(0, 6),
            Location(0, 7),
            Location(4, 0),
            Location(4, 5),
            Location(4, 6),
            Location(4, 7),
            Location(4, 12),
            Location(5, 0),
            Location(5, 1),
            Location(5, 6),
            Location(5, 11),
            Location(5, 12),
            Location(6, 0),
            Location(6, 12),
            Location(7, 3),
            Location(7, 4),
            Location(7, 6),
            Location(7, 8),
            Location(7, 9),
            Location(8, 2),
            Location(8, 4),
            Location(8, 6),
            Location(8, 8),
            Location(8, 10),
            Location(9, 0),
            Location(9, 12),
            Location(10, 2),
            Location(10, 4),
            Location(10, 6),
            Location(10, 8),
            Location(10, 10),
            Location(11, 3),
            Location(11, 4),
            Location(11, 6),
            Location(11, 8),
            Location(11, 9),
            Location(12, 0),
            Location(12, 12),
            Location(13, 0),
            Location(13, 1),
            Location(13, 6),
            Location(13, 11),
            Location(13, 12),
            Location(14, 0),
            Location(14, 5),
            Location(14, 6),
            Location(14, 7),
            Location(14, 12),
            Location(18, 5),
            Location(18, 6),
            Location(18, 7),
        ]
        super().__init__(rows, cols, impassable_terrain, variant)
        self._initialize_board()

    def _initialize_board(self):
        initial_positions: list[list[str | None]] = [
            [None, 'RG', None, 'RG', None, None, None, None, None, 'RG', None, 'RG', None],
            ['RG', None, None, None, None, None, None, None, None, None, None, None, 'RG'],
            ['RG', None, 'RC', None, None, 'RG', None, 'RG', None, None, 'RC', None, 'RG'],
            [None, None, None, None, None, None, 'RA', None, None, None, None, None, None],
            [None, 'RA', None, None, None, None, None, None, None, None, None, 'RA', None],
            [None, None, 'RS', 'RA', 'RM', None, None, None, 'RM', 'RA', 'RS', None, None],
            [None, 'RS', 'RS', 'RS', 'RL', 'RL', 'RL', 'RL', 'RL', 'RS', 'RS', 'RS', None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, 'BS', 'BS', 'BS', 'BL', 'BL', 'BL', 'BL', 'BL', 'BS', 'BS', 'BS', None],
            [None, None, 'BS', 'BA', 'BM', None, None, None, 'BM', 'BA', 'BS', None, None],
            [None, 'BA', None, None, None, None, None, None, None, None, None, 'BA', None],
            [None, None, None, None, None, None, 'BA', None, None, None, None, None, None],
            ['BG', None, 'BC', None, None, 'BG', None, 'BG', None, None, 'BC', None, 'BG'],
            ['BG', None, None, None, None, None, None, None, None, None, None, None, 'BG'],
            [None, 'BG', None, 'BG', None, None, None, None, None, 'BG', None, 'BG', None],
        ]

        self._initialize_pieces(initial_positions)


class PrimeBoard(Board):
    def __init__(self):
        rows = 16
        cols = 21
        variant = 3
        initial_board = [
            list("SSSSSSSSSSSSSSSSSSSSS"),
            list("SSSSSSSSSSSSSSSSSSSSS"),
            list("SSSSSSSSSSSSSSSSSSSSS"),
            list("SSS{--}SSSSSSS{--}SSS"),
            list("000PBBQ0000000PBBQ000"),
            list("111$BB%1111111$BB%111"),
            list("///<**>///////<**>///"),
            list("GGGGGGGGGGGGGGGGGGGGG"),
            list("GGGGGGGGGGGGGGGGGGGGG"),
            list("GGG(++)GGGGGGG(++)GGG"),
            list("222PBBQ2222222PBBQ222"),
            list("333$BB%3333333$BB%333"),
            list(",,,[==],,,,,,,[==],,,"),
            list("SSSSSSSSSSSSSSSSSSSSS"),
            list("SSSSSSSSSSSSSSSSSSSSS"),
            list("SSSSSSSSSSSSSSSSSSSSS"), 
        ]
        impassable_terrain = [ 
            Location(r, c)
            for r in range(rows)
            for c in range(cols)
            if initial_board[r][c] in ["0", "1", "2", "3"]
        ]
        super().__init__(rows, cols, impassable_terrain, variant)
        self._initialize_board()

    def _initialize_board(self):
        initial_positions: list[list[str | None]] = [
            ['RG', None, 'RG', None, None, None, None, None, None, 'RG', None, 'RG', None, None, None, None, None, None, 'RG', None, 'RG'],
            [None, 'RC', None, 'RG', None, None, 'RG', None, None, None, 'RC', None, None, None, 'RG', None, None, 'RG', None, 'RC', None],
            [None, None, None, None, 'RM', 'RM', None, None, None, None, None, None, None, None, None, 'RM', 'RM', None, None, None, None],
            ['RA', 'RA', 'RA', None, None, None, None, 'RA', 'RA', 'RA', 'RA', 'RA', 'RA', 'RA', None, None, None, None, 'RA', 'RA', 'RA'],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, 'RL', 'RL', 'RL', 'RL', None, None, None, None, None, None, None, 'RL', 'RL', 'RL', 'RL', None, None, None],
            ['RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS', 'RS'],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ['BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS', 'BS'],
            [None, None, None, 'BL', 'BL', 'BL', 'BL', None, None, None, None, None, None, None, 'BL', 'BL', 'BL', 'BL', None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
            ['BA', 'BA', 'BA', None, None, None, None, 'BA', 'BA', 'BA', 'BA', 'BA', 'BA', 'BA', None, None, None, None, 'BA', 'BA', 'BA'],
            [None, None, None, None, 'BM', 'BM', None, None, None, None, None, None, None, None, None, 'BM', 'BM', None, None, None, None],
            [None, 'BC', None, 'BG', None, None, 'BG', None, None, None, 'BC', None, None, None, 'BG', None, None, 'BG', None, 'BC', None],
            ['BG', None, 'BG', None, None, None, None, None, None, 'BG', None, 'BG', None, None, None, None, None, None, 'BG', None, 'BG'],
        ]

        self._initialize_pieces(initial_positions)

class ClassicBoard(Board):
    def __init__(self):
        rows = 17
        cols = 13
        variant = 4
        impassable_terrain = [
            Location(0, 0),
            Location(0, 1),
            Location(0, 2),
            Location(0, 10),
            Location(0, 11),
            Location(0, 12),
            Location(1, 0),
            Location(1, 1),
            Location(1, 11),
            Location(1, 12),
            Location(2, 0),
            Location(2, 12),
            Location(14, 0),
            Location(14, 12),
            Location(15, 0),
            Location(15, 1),
            Location(15, 11),
            Location(15, 12),
            Location(16, 0),
            Location(16, 1),
            Location(16, 2),
            Location(16, 10),
            Location(16, 11),
            Location(16, 12),
            Location(3, 5),
            Location(3, 6),
            Location(3, 7),
            Location(4, 5),
            Location(4, 6),
            Location(4, 7),
            Location(5, 1),
            Location(5, 3),
            Location(5, 5),
            Location(5, 6),
            Location(5, 7),
            Location(5, 9),
            Location(5, 11),
            Location(6, 1),
            Location(6, 3),
            Location(6, 6),
            Location(6, 10),
            Location(8, 1),
            Location(8, 3),
            Location(8, 5),
            Location(8, 7),
            Location(8, 9),
            Location(8, 11),
            Location(10, 1),
            Location(10, 3),
            Location(10, 6),
            Location(10, 10),
            Location(11, 1),
            Location(11, 3),
            Location(11, 5),
            Location(11, 6),
            Location(11, 7),
            Location(11, 9),
            Location(11, 11),
            Location(12, 5),
            Location(12, 6),
            Location(12, 7),
            Location(13, 5),
            Location(13, 6),
            Location(13, 7),
        ]
        super().__init__(rows, cols, impassable_terrain, variant)
        self._initialize_board()

    def _initialize_board(self):
        initial_positions: list[list[str | None]] = [
            [None, None, None, 'RG', None, None, 'RG', None, None, 'RG', None, None, None],
            [None, None, 'RG', None, 'RC', None, None, None, 'RC', None, 'RG', None, None],
            [None, None, None, 'RG', None, None, 'RG', None, None, 'RG', None, None, None],
            ['RL', None, 'RL', None, 'RL', None, None, None, 'RS', 'RM', 'RS', 'RM', 'RS'],
            ['RL', 'RA', 'RL', 'RA', 'RL', None, None, None, 'RS', 'RS', 'RS', 'RS', 'RS'],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None, None, None, None, None, None],
            ['BL', 'BA', 'BL', 'BA', 'BL', None, None, None, 'BS', 'BS', 'BS', 'BS', 'BS'],
            ['BL', None, 'BL', None, 'BL', None, None, None, 'BS', 'BM', 'BS', 'BM', 'BS'],
            [None, None, None, 'BG', None, None, 'BG', None, None, 'BG', None, None, None],
            [None, None, 'BG', None, 'BC', None, None, None, 'BC', None, 'BG', None, None],
            [None, None, None, 'BG', None, None, 'BG', None, None, 'BG', None, None, None],
        ]
        
        self._initialize_pieces(initial_positions)
