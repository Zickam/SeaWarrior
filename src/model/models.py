from __future__ import annotations

import numpy as np
import pygame as pg

from view.constants import SCREEN_RESOLUTION
from custom_types import *
from perlin_noise import perlin
from custom_enums import *
from model.constants import *

class Ship:
    def __init__(self, size: Vec2, coordinates: Vec2, hp: float):
        self._size = size
        self._coordinates = coordinates
        self._old_coordinates = self._coordinates
        self._hp = hp

        self._rect = pg.rect.Rect((self._coordinates[0] - self._size[0] + SCREEN_RESOLUTION[0] // 2, self._coordinates[1] - self._size[1] + SCREEN_RESOLUTION[1] // 2), self._size)

    def setOldCoordinates(self, coords: Vec2):
        self._old_coordinates = coords

    def getOldCoordinates(self) -> Vec2:
        return self._old_coordinates

    def setCoordinates(self, coords: Vec2):
        self._coordinates = coords

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
        self._is_outer = True
        self._closest_water_coords = None

    def setClosestWaterCoordinates(self, coords: Vec2):
        self._closest_water_coords = coords

    def getClosestWaterCoordinates(self) -> Vec2:
        return self._closest_water_coords


    def setIsOuter(self, is_outer: bool):
        self._is_outer = is_outer

    def getIsOuter(self) -> bool:
        return self._is_outer

    def getCoordinates(self) -> Vec2:
        return self._coords

    def getSize(self) -> Vec2:
        return self._size

    def getBlockType(self) -> BlockType:
        return self._block_type

    def calculateRect(self, relative_to_screen_coords: Vec2):
        self._rect = pg.rect.Rect(
            (
                relative_to_screen_coords[0] + self._size[0] // 2,
                relative_to_screen_coords[1] + self._size[1] // 2
            ),
            self._size
        )

    def getRect(self) -> pg.rect:
        return self._rect

    def __str__(self) -> str:
        return f"{self._coords}, {self._block_type}"

class Model:
    def __init__(self):
        self.__state = GameState.main_menu

        self.__enemies: set[Ship] = set()


    def initBlockMap(self, seed: int = None):
        self.__perlin = perlin.Perlin2D(seed)
        self.__noise = self.__perlin.generatePerlin(MAP_SIZE, MAP_SCALE)

        # np.resize(self.__noise,  MAP_SIZE * 2)

        self.__block_map = Model.perlinToBlockMap(self.__noise)

    def getBlockMap(self) -> list[list[Block]]:
        return self.__block_map

    @staticmethod
    def perlinToBlockMap(perlin_map: np.array) -> list[list[Block]]:
        block_map: list[list[Block]] = []
        for i in range(-len(perlin_map) // 2, len(perlin_map) // 2):
            block_map.append([])
            for j in range(-len(perlin_map[i]) // 2, len(perlin_map[i]) // 2):
                block_type = BlockType.island if perlin_map[i, j] >= GROUND_LEVEL else BlockType.water
                block_size = DEFAULT_BLOCK_SIZE
                block = Block(block_type,
                              (i * block_size[0], j * block_size[1]),
                              block_size)
                block_map[-1].append(block)

        for i in range(len(block_map)):
            for j in range(len(block_map[i])):
                if i == 0 or i == len(block_map) - 1 or j == 0 or j == len(block_map) - 1:
                    block_map[i][j].setIsOuter(True)
                    continue

                island_down = block_map[i + 1][j].getBlockType() == BlockType.island
                island_up = block_map[i - 1][j].getBlockType() == BlockType.island
                island_left = block_map[i][j - 1].getBlockType() == BlockType.island
                island_right = block_map[i][j + 1].getBlockType() == BlockType.island
                if block_map[i][j].getBlockType() == BlockType.island:
                    if island_down\
                         and island_up\
                         and island_left\
                         and island_right:
                        block_map[i][j].setIsOuter(False)
                    else:
                        if not island_down:
                            coords = block_map[i + 1][j].getCoordinates()
                            closest_water = [coords[0] + 1, coords[1]]
                        elif not island_up:
                            coords = block_map[i - 1][j].getCoordinates()
                            closest_water = [coords[0] - 1, coords[1]]
                        elif not island_right:
                            coords = block_map[i][j + 1].getCoordinates()
                            closest_water = [coords[0], coords[1] + 1]
                        elif not island_left:
                            coords = block_map[i][j - 1].getCoordinates()
                            closest_water = [coords[0], coords[1] - 1]
                        else:
                            raise Exception("closest_water is not defined (no matching island_*)!")
                        # print(closest_water)
                        block_map[i][j].setClosestWaterCoordinates(closest_water)

        return block_map

    def getPlayer(self) -> Ship:
        return self._player

    def getGameState(self) -> custom_enums.GameState.__dict__:
        return self.__state

    def setGameState(self, game_state: custom_enums.GameState):
        self.__state = game_state

    @staticmethod
    def restartGame(self) -> Model:
        return Model()

    def initPlayer(self):
        self._player = Ship(SHIP_SIZE,
                             [ + SHIP_SIZE[0] // 2,
                               + SHIP_SIZE[1] // 2],
                             PLAYER_BASE_HP)


    # def initMap(self):
