# run with `poetry run python src/main.py`

# ideally we only instantiate model, view, and controller here
# ideal code found below

from model import GameModel
from pygameview import GameView
from controller import GameController



if __name__ == "__main__":
    model = GameModel.default_game()
    view = GameView(model.state)

    controller = GameController(model, view)
    controller.start()

