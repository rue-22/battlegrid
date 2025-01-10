from model import GameModel
from view import View, GameStateChangeObserver
from classes import Action, Piece, Location, GameState, piece_mappings, PieceKind, Side, MessageType
from cs150241project_networking import CS150241ProjectNetworking
from typing import Optional
import threading

class GameController:
    def __init__(self, model: GameModel, view: View):
        self._model = model
        self._view = view
        self._networking = CS150241ProjectNetworking.connect('localhost', 15000)

        self._send_message(MessageType.PLAYER_IN, player_id=self._networking.player_id)
       
        self._game_state_change_observers: list[GameStateChangeObserver] = []

    def start(self):
        view = self._view

        self.register_game_state_change_observer(view)

        view.register_action_observer(self)
        view.register_new_game_observer(self)
        # view.register_game_over_observer

        self._model.assign_networkID(self._networking.player_id)
        self._on_state_change(self._model.state)
        
        threading.Thread(target=self._wait_for_messages, daemon=True).start()

        view.run()
    
    # protocol
    def on_action(self, action: Action, piece: Piece, to: Location):
        self._send_message(MessageType.MADE_ACTION, action=action, piece=piece, to=to)

    def _send_message(self, message_type: MessageType, variant: Optional[int] = None, player_id: Optional[int] = None, action: Optional[Action] = None, piece: Optional[Piece] = None, to: Optional[Location] = None):
        match message_type:
            case MessageType.PLAYER_IN:
                assert player_id is not None
                message = f'type:{message_type.value}/pid:{player_id}'

            case MessageType.SEND_CONFIG:
                assert variant is not None
                message = f'type:{message_type.value}/variant:{variant}'

            case MessageType.MADE_ACTION:
                assert action is not None
                assert piece is not None
                assert to is not None
                message = f'type:{message_type.value}/moves:{self._model.state.moves_made}/action:{action.value}/pkind:{piece.piece_kind.value}/pside:{piece.side.value}/prow:{piece.location.row}/pcol:{piece.location.col}/torow:{to.row}/toloc:{to.col}'

        self._networking.send(message)

    def _wait_for_messages(self):
        while True:
            for msg in self._networking.recv():
                self._decipher_message(msg.payload)

    def _decipher_message(self, payload: str):
        tokens = payload.strip().split('/')
        message_type = tokens[0].split(':')[1]
        
        match MessageType(int(message_type)):
            case MessageType.PLAYER_IN:
                if self._networking.player_id == 1:
                    pid = tokens[1].split(':')[1]
                    if int(pid) == 2:
                        self._model.p2_connected()
                        self._on_state_change(self._model.state)

            case MessageType.SEND_CONFIG:
                variant = tokens[1].split(':')[1]
                self._model.p1_board_initializd(int(variant))
                self._on_state_change(self._model.state)
                
            case MessageType.MADE_ACTION:
                moves, action, pkind, pside, prow, pcol, torow, tocol = [token.split(':')[1] for token in tokens[1:]]

                self._model.state.moves_made = int(moves)

                piece = Piece(piece_mappings[PieceKind(pkind)], Location(int(prow), int(pcol)), Side(int(pside)))
                to = Location(int(torow), int(tocol))

                self._perform_action(Action(int(action)), piece, to)

    def _perform_action(self, action: Action, piece: Piece, to: Location):
        self._model.next_move(action, piece, to)
        if self._model.state.moves_made >= self._model.state.max_moves:
            self._model.next_turn()
        self._model.check_game_result()
        self._on_state_change(self._model.state)
        
    def _on_state_change(self, game_state: GameState):
        for observer in self._game_state_change_observers:
            observer.on_state_change(game_state)
    
    def on_new_game(self, variant: int):
        self._send_message(MessageType.SEND_CONFIG, variant=variant)
        self._model.new_game_variant(variant)
        self._model.assign_networkID(self._networking.player_id)
        self._on_state_change(self._model.state)
    
    def register_game_state_change_observer(self, observer: GameStateChangeObserver):
        self._game_state_change_observers.append(observer)
