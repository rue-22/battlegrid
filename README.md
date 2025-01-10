![logo](python_client/src/assets/logo.png)
# Battlegrid
**Battlegrid** is a two-player board game where every move counts. Command an army of classes — from powerful mages to brave guards — across four different maps. Let the chaos begin.

## Gameplay
This game is composed of different [classes](#classes). Each class has their own movement pattern.

When a piece moves to a cell containing a piece owned by the opponent, the opponent's piece is said to be captured by the player and taken out of the board.

Captured pieces are considered as owned by the capturing player and may be dropped onto an unoccupied cell (with some restrictions of course!) to be played as a regular piece.

Each player must perform _three_ actions per turn. Skipping is **not** allowed.
+ _Move_ a piece to a valid cell.
+ _Drop_ a captured piece to a valid cell.

In order to be victorious, the player must trap **all** enemy crystals.

## Classes
Battlegrid is composed of five fighting classes and one class that must be protected at all costs — the **Crystal**. Try to play the game to discover their movement patterns!

| ![swordsman](python_client/src/assets/swordsman.png) | ![longsword](python_client/src/assets/longsword.png) | ![archer](python_client/src/assets/archer.png) | ![mage](python_client/src/assets/mage.png) | ![guard](python_client/src/assets/guard.png) | ![crystal](python_client/src/assets/crystal.png) |
|:---------------------------------------------------:|:---------------------------------------------------:|:----------------------------------------------:|:------------------------------------------:|:------------------------------------------:|:-----------------------------------------------:|
| **Swordsman**                                       | **Longsword**                                       | **Archer**                                     | **Mage**                                   | **Guard**                                   | **Crystal**                                    |

## Modes
Battlegrid offers four modes to keep the gameplay fresh and expand your strategies.
+ **Classic**: An oval-shaped 17-by-13 board with long connected bridges for epic battles.
+ **Rush**: A compact 16-by-10 board designed for quicker gameplay.
+ **War**: A 19-by-13 hourglass-shaped board with various terrains and narrower bridges for more chaotic moments.
+ **Prime**: Just like Classic but with its width doubled, offering more fun and more strategies.

## Usage
To run the game in your own desktop, do the following:

1. Run the command below inside the `go_server/` directory.
```bash
go run .
```

2. Run two instances of `main.py` inside the `python_client/` directory using the command below (in two seperate terminals). Make sure that [Poetry](https://python-poetry.org/) is installed (installation guide [here](https://python-poetry.org/docs/#installing-with-pipx)).
```bash
poetry run python src/main.py
```

The only caveat, however, is that the server is crudely implemented. Hence, it must be manually turned off when the game ends and manually turned on again when a new game is played (sorry about that!).

## Team
+ [Gaza, Judelle Clareese](https://github.com/ElleDiablo)
+ [Roy, Rodrigo Emmanuel](https://github.com/reofficial)
+ [Salces, Carl John](https://github.com/rue-22)
+ [Villamil, John Ysaac](https://github.com/LigsQt)
