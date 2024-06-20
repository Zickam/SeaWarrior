from __future__ import annotations

import numpy as np

from custom_types import *
from model import constants
from perlin_noise import perlin
from custom_enums import *

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


class Map:
    GROUND_LEVEL = 0.7
    def __init__(self, seed: int, size: Vec2, scale: float):
        self.__perlin = perlin.Perlin2D(seed)

        self.__perlin_map = self.__perlin.generatePerlin(size, scale, 1)

    def setBlockMap(self, block_map: list[list[BlockType]]):
        self.__block_map = block_map

    def getBlockMap(self) -> list[list[BlockType]]:
        return self.__block_map


class Model:
    def __init__(self):
        self.__state = GameState.main_menu

        self.__player = Ship([0, 0], 100)
        self.__enemies: set[Ship] = set()

        self.__is_pause = False

    def initBlockMap(self, seed: int = None):
        self.__perlin = perlin.Perlin2D(seed)
        self.__noise = self.__perlin.generatePerlin(constants.MAP_SIZE, constants.MAP_SCALE)
        self.__map = Model.perlinToBlockMap(self.__noise)

    @staticmethod
    def perlinToBlockMap(perlin_map: np.array) -> list[list[BlockType]]:
        block_map = []
        for i in range(len(perlin_map)):
            block_map.append([])
            for j in range(len(perlin_map[i])):
                block = BlockType.island if perlin_map[i, j] >= Map.GROUND_LEVEL else BlockType.water
                block_map[-1].append(block)

        return block_map

    def getMap(self) -> list[list[BlockType]]:
        return self.__map

    def isPause(self) -> bool:
        return self.__is_pause

    def setIsPause(self, is_pause: bool):
        self.__is_pause = is_pause

    def getPlayer(self) -> Ship:
        return self.__player

    def getGameState(self) -> custom_enums.GameState.__dict__:
        return self.__state

    def setGameState(self, game_state: custom_enums.GameState):
        self.__state = game_state

    @staticmethod
    def restartGame(self) -> Model:
        return Model()

    def initPlayer(self):
        self.__player = Ship([0, 0], constants.PLAYER_BASE_HP)

    # def initMap(self):
