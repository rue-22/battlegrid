from typing import Protocol
from classes import GameState, Action, Piece, Location


#protocol to be implemented by view:
class GameStateChangeObserver(Protocol):
    #an observer that gets notified when game state(model) is changed
    #implementation: pygame view displays the game_state argument passed onto it
    def on_state_change(self, state: GameState):
        ...

#protocols to be implemented by controller:
class ActionObserver(Protocol):
    def on_action(self, action: Action, piece: Piece, to: Location):
        ...

class NewGameObserver(Protocol):
    def on_new_game(self, variant: int):
        ...

#view protocol
class View(Protocol):
    def run(self):
        ...

    def on_state_change(self, state: GameState):
        ...
    
    def register_action_observer(self, observer: ActionObserver):
        ...
    
    def register_new_game_observer(self, observer: NewGameObserver):
        ...

