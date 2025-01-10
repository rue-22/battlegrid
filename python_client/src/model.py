from classes import (GameState, ClassicBoard, Action, Piece, Location, GameVerdict)
from typing import Self


class GameModel:
    @classmethod
    def default_game(cls) -> Self:
        MainBoard = ClassicBoard()
        MainGame = GameState(MainBoard)

        return cls(MainGame)
    
    def __init__(self, state: GameState):
        self._state = state
    
    def next_move(self, action: Action, piece: Piece, to: Location):
        if self._state.moves_made >= self._state.max_moves:
            self.next_turn()

        match action:
            case Action.MOVE:
                target = self._state.board.get_piece(to)
                # eat enemy piece and store to available pieces
                if target:
                    self._state.curr_player.capture_piece(target)
                    self._state.board.remove_piece(to)
                    self._state.board.remove_piece(piece.location)
                    self._state.board.place_piece(piece, to)
                # else, just move the piece
                else:
                    self._state.board.remove_piece(piece.location)
                    self._state.board.place_piece(piece, to)

            case Action.DROP:
                self._state.curr_player.use_piece(piece)
                self._state.board.place_piece(piece, to)

        self._state.moves_made += 1
        
    def next_turn(self):
        self._state.curr_player = self._state.red_player if self._state.curr_player == self._state.blue_player else self._state.blue_player
        self._state.moves_made = 0
        
    def check_game_result(self):
        valid_moves_for_blue_crystals = [len(self._state.board.get_valid_moves(crystal)) for crystal in self._state.board.blue_crystals]
        valid_moves_for_red_crystals = [len(self._state.board.get_valid_moves(crystal)) for crystal in self._state.board.red_crystals]

        can_blue_still_move = any(valid_moves_for_blue_crystals)
        can_red_still_move = any(valid_moves_for_red_crystals)

        if not can_blue_still_move and not can_red_still_move:
            self._state.game_verdict = GameVerdict.DRAW
        elif not can_blue_still_move:
            self._state.game_verdict = GameVerdict.RED_WINNER
        elif not can_red_still_move:
            self._state.game_verdict = GameVerdict.BLUE_WINNER
        else:
            self._state.game_verdict = GameVerdict.CONTINUE

    def new_game(self):
        state = self._state.new_board(self._state.board.variant)
        self._state = state

    def new_game_variant(self, variant: int):
        state = self._state.new_board(variant)
        self._state = state

    def assign_networkID(self, nid: int):
        self._state.assign_networkID(nid)

    def p2_connected(self):
        self._state.is_P2_connected = True

    def p1_board_initializd(self, variant: int):
        self._state.P1board_variant = variant

    @property
    def state(self):
        return self._state
