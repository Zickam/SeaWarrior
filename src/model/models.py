from __future__ import annotations

from src.custom_types import *
from src.model import constants
from src import enums


class Ship:
    def __init__(self, coordinates: Vec2, hp: float):
        self._coordinates = coordinates
        self._hp = hp

    def changeCoordinatesBy(self, by: Vec2):
        self._coordinates[0] += by[0]
        self._coordinates[1] += by[1]

    def changeHPBy(self, by: float):
        self._hp += by

    def getHP(self) -> float | int:
        return self._hp


class Chunk:
    def __init__(self):
        self.__elements: dict[Vec2, enums.BlockType] = dict()


class Map:
    def __init__(self, seed: int):
        self.__map: dict[Vec2, Chunk] = dict()
        self.__generator = generator.Generator(seed)

    def saveChunk(self, coordinates: Vec2):
        ...

    def generateChunk(self, coordinates: Vec2):
        ...

    def loadChunk(self, coordinates: Vec2):
        ...


class Model:
    def __init__(self):
        self.__state = enums.GameState.main_menu

        self.__player = Ship((0, 0), 100)
        self.__enemies: set[Ship] = set()

        self.__is_pause = False

    def isPause(self) -> bool:
        return self.__is_pause

    def setIsPause(self, is_pause: bool):
        self.__is_pause = is_pause

    def getPlayer(self) -> Ship:
        return self.__player


    def getGameState(self) -> enums.GameState.__dict__:
        return self.__state

    def setGameState(self, game_state: enums.GameState):
        self.__state = game_state

    @staticmethod
    def restartGame(self) -> Model:
        return Model()

    def initPlayer(self):
        self.__player = Ship((0, 0), constants.PLAYER_BASE_HP)

    def initMap(self):
        ...
