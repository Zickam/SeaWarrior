from __future__ import annotations

import custom_enums
from custom_enums import *
from custom_types import *
from view.constants import SCREEN_RESOLUTION

import pygame as pg

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
        self._acceleration = 0, 0

    def getAcceleration(self) -> Vec2:
        return self._acceleration

    def setAcceleration(self, acceleration: Vec2):
        self._acceleration = acceleration

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

    def getBlockMap(self) -> set[Block]:
        return self._block_map

    def setBlockMap(self, block_map: set[Block]):
        self._block_map = block_map

    def getPlayer(self) -> Ship:
        return self._player

    def setPlayer(self, player: Ship):
        self._player = player

    def getGameState(self) -> custom_enums.GameState.__dict__:
        return self.__state

    def setGameState(self, game_state: custom_enums.GameState):
        self.__state = game_state

    @staticmethod
    def restartGame() -> Model:
        return Model()

