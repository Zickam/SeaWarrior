from __future__ import annotations

import numpy as np
import pygame as pg

from view.constants import SCREEN_RESOLUTION
from custom_types import *
from perlin_noise import perlin
from custom_enums import *
from model.constants import *


class Object:
    def __init__(self,  coordinates: Vec2, size: Vec2, is_physical: bool = False, hp: float = None):
        self._coordinates = coordinates
        self._size = size
        self._hp = hp

        self._rect = pg.rect.Rect(
            (SCREEN_RESOLUTION[0] // 2 - self._size[0] // 2, SCREEN_RESOLUTION[1] // 2 - self._size[1] // 2),
            self._size)
        self._is_visible = False
        self._is_physical = is_physical

    def getIsPhysical(self) -> bool:
        return self._is_physical

    def setIsPhysical(self, is_physical: bool):
        self._is_physical = is_physical

    def getSize(self) -> Vec2:
        return self._size

    def setCoordinates(self, coords: Vec2):
        self._coordinates = coords

    def getCoordinates(self) -> Vec2:
        return self._coordinates

    def calculateRect(self, screen_coords: Vec2):
        self._rect = pg.rect.Rect((screen_coords[0] + self._size[0] // 2,
                                   screen_coords[1] + self._size[1] // 2),
                                  self._size)

    def getRect(self) -> pg.Rect:
        return self._rect


    def changeCoordinatesBy(self, by: Vec2):
        self._coordinates[0] += by[0]
        self._coordinates[1] += by[1]

    def changeHPBy(self, by: float):
        self._hp += by

    def getHP(self) -> float | int:
        return self._hp

    def __hash__(self):
        return id(self)

    def getIsVisible(self) -> bool:
        return self._is_visible

    def setIsVisible(self, is_visible: bool):
        self._is_visible = is_visible


class Ship(Object):
    def __init__(self, coordinates: Vec2, size: Vec2, hp: float):
        super().__init__(coordinates, size, True, hp)


class Block(Object):
    def __init__(
            self,
            coords: Vec2,
            size: Vec2,
            block_type: custom_enums.BlockType,
    ):
        super().__init__(coords, size)

        self._block_type = block_type

    def setBlockType(self, new_type: BlockType):
        self._block_type = new_type

    def getBlockType(self) -> BlockType:
        return self._block_type

    def __str__(self) -> str:
        return f"{self._coords}, {self._block_type}"


class Model:
    def __init__(self):
        self.__state = GameState.main_menu

        self.__enemies: set[Ship] = set()
        self.__last_time_enemy_spawned = 0

    def getEnemies(self) -> set[Ship]:
        return self.__enemies

    def getLastTimeEnemySpawned(self) -> float:
        return self.__last_time_enemy_spawned

    def setLastTimeEnemySpawned(self, _time: float):
        self.__last_time_enemy_spawned = _time

    def addEnemy(self, enemy: Ship):
        self.__enemies.add(enemy)

    def initBlockMap(self, seed: int = None):
        self.__perlin = perlin.Perlin2D(seed)
        self.__noise = self.__perlin.generatePerlin(MAP_SIZE, MAP_SCALE)

        # np.resize(self.__noise,  MAP_SIZE * 2)

        self.__block_map = self.perlinToBlockMap(self.__noise)

    def getBlockMap(self) -> set[Block]:
        return self.__block_map

    def __applyCollisions(self, block_map: list[list[Block]]):
        for i in range(len(block_map)):
            for j in range(len(block_map[i])):
                if i == 0 or i == len(block_map) - 1 or j == 0 or j == len(block_map) - 1:
                    continue
                    block_map[i][j].setBlockType(BlockType.island)
                    block_map[i][j].setIsPhysical(True)
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
                        block_map[i][j].setIsPhysical(False)
                    else:
                        block_map[i][j].setIsPhysical(True)


    def perlinToBlockMap(self, perlin_map: np.array) -> set[Block]:
        block_map: list[list[Block]] = []
        for i in range(-len(perlin_map) // 2, len(perlin_map) // 2):
            block_map.append([])
            for j in range(-len(perlin_map[i]) // 2, len(perlin_map[i]) // 2):
                block_type = BlockType.island if perlin_map[i, j] >= GROUND_LEVEL else BlockType.water
                block_size = DEFAULT_BLOCK_SIZE
                block = Block(
                    (i * block_size[0], j * block_size[1]),
                    block_size,
                    block_type)
                block_map[-1].append(block)

        self.__applyCollisions(block_map)

        _island_map = set()
        for i in range(len(block_map)):
            for j in range(len(block_map[i])):
                if block_map[i][j].getBlockType() == BlockType.island:
                    _island_map.add(block_map[i][j])

        return _island_map

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
        self._player = Ship(
                             # [SHIP_SIZE[0] // 2,
                             #   + SHIP_SIZE[1] // 2],
                            [
                                0,
                                0
                            ],
            SHIP_SIZE,
                             PLAYER_BASE_HP)


    # def initMap(self):
