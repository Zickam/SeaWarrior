from __future__ import annotations

import controller.main

from custom_types import *
import constants
import generator
import enums


class Ship:
    def __init__(self, coordinates: Vec2, controller: controller.main.Bot | controller.main.Input, hp: float | int):
        self.__coordinates = coordinates
        self.__controller = controller
        self.__hp = hp

    def getHP(self) -> float | int:
        return self.__hp

    def decreaseHP(self, by: float | int):
        self.__hp -= by

    def increaseHP(self, by: float | int):
        self.__hp += by

    def __hash__(self) -> int:
        return id(self)

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


class Game:
    def __init__(self):
        self.__state = enums.GameState.main_menu

    def postInit(self, seed: int):
        self.__enemies: set[Ship] = set()
        self.__map = Map(seed)

    def getState(self) -> enums.GameState.__dict__:
        return self.__state

    @staticmethod
    def restartGame(self) -> Game:
        return Game()

    def gameplayStart(self):
        self.__player = Ship((0, 0), controller.main.Input(), constants.player_basehp)

    def handleDeath(self):
        self.__state = enums.GameState.death_screen

