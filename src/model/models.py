from __future__ import annotations

import numpy as np
import pygame as pg

import view.constants
from custom_types import *
from perlin_noise import perlin
from custom_enums import *
from model.constants import *

class Ship:
    def __init__(self, size: Vec2, coordinates: Vec2, hp: float):
        self._size = size
        self._coordinates = coordinates
        self._hp = hp

        self._rect = pg.rect.Rect((self._coordinates[0] - self._size[0] + view.constants.SCREEN_RESOLUTION[0] // 2, self._coordinates[1] - self._size[1] + view.constants.SCREEN_RESOLUTION[1] // 2), self._size)

    def getCoordinates(self) -> Vec2:
        return self._coordinates

    def getRect(self) -> pg.Rect:
        return self._rect


    def changeCoordinatesBy(self, by: Vec2):
        self._coordinates[0] += by[0]
        self._coordinates[1] += by[1]

    def changeHPBy(self, by: float):
        self._hp += by

    def getHP(self) -> float | int:
        return self._hp


class Block:
    def __init__(
            self,
            block_type: custom_enums.BlockType,
            coords: Vec2,
            size: Vec2,
    ):
        self._block_type = block_type
        self._coords = coords
        self._size = size


    def getCoordinates(self) -> Vec2:
        return self._coords

    def getSize(self) -> Vec2:
        return self._size

    def getBlockType(self) -> BlockType:
        return self._block_type

    def calculateRect(self, player_coords: Vec2):
        self._rect = pg.rect.Rect(((self._coords[0]) // 2 + self._size[0] + view.constants.SCREEN_RESOLUTION[0] // 2 + player_coords[0],
                                   (self._coords[1]) // 2 + self._size[1] + view.constants.SCREEN_RESOLUTION[1] // 2 + player_coords[1]),
                                  self._size)

    def getRect(self) -> pg.rect:
        return self._rect

class Model:
    def __init__(self):
        self.__state = GameState.main_menu

        self.__enemies: set[Ship] = set()

        self.__is_pause = False



    def initBlockMap(self, seed: int = None):
        self.__perlin = perlin.Perlin2D(seed)
        self.__noise = self.__perlin.generatePerlin(MAP_SIZE, MAP_SCALE)

        # np.resize(self.__noise,  MAP_SIZE * 2)

        self.__block_map = Model.perlinToBlockMap(self.__noise)

    def getBlockMap(self) -> list[list[Block]]:
        return self.__block_map

    @staticmethod
    def perlinToBlockMap(perlin_map: np.array) -> list[list[Block]]:
        block_map = []
        for i in range(-len(perlin_map) // 2, len(perlin_map) // 2):
            block_map.append([])
            for j in range(-len(perlin_map[i]) // 2, len(perlin_map[i]) // 2):
                block_type = BlockType.island if perlin_map[i, j] >= GROUND_LEVEL else BlockType.water
                block_size = DEFAULT_BLOCK_SIZE
                block = Block(block_type,
                              (i * block_size[0], j * block_size[1]),
                              block_size)
                block_map[-1].append(block)

        return block_map

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
        self.__player = Ship(SHIP_SIZE,
                             [ + SHIP_SIZE[0] // 2,
                               + SHIP_SIZE[1] // 2],
                             PLAYER_BASE_HP)
        print(self.__player.getCoordinates())


    # def initMap(self):
