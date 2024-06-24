import random
import time

import numpy as np
import pygame as pg

import model.models
from custom_enums import *
from model.constants import *
from model.models import Model, Block
from model.models import Ship
from perlin_noise import perlin
from view.constants import *


class ConfigManager:
    CONFIG_DIR = "data/config"
    def __init__(self):
        ...


class Presenter:
    def __init__(self, model: Model):
        self.__model = model

    def getPlayer(self):
        return self.__model.getPlayer()

    def getEnemies(self):
        return self.__model.getEnemies()

    def getVisibleBlockMap(self):
        # if not hasattr(self, "_visible_block_map"):
        #     self.__updateVisibleBlockMap()
        return self._visible_block_map

    def startGameplay(self):
        self.__model.setGameState(GameState.gameplay)

        self.__initBlockMap()
        self.__initPlayer()

    def togglePause(self):
        if self.__model.getGameState() == GameState.pause:
            self.__model.setGameState(GameState.gameplay)
        else:
            self.__model.setGameState(GameState.pause)

    def openSavesMenu(self):
        self.__model.setGameState(GameState.saves_menu)

    def openMainMenu(self):
        self.__model.setGameState(GameState.main_menu)

    def tickGameplay(self):
        if hasattr(self.__model, "_player"):
            self.__updateVisibleBlockMap()
            self.__handlePlayerControl()

            self.__handleCollisions()

        self.__handleEnemies()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def __updateVisibleObjects(self):
        raise NotImplementedError

    def __updateVisibleBlockMap(self):
        player_coords = tuple(self.__model.getPlayer().getCoordinates())

        block_map = self.__model.getBlockMap()

        visible_block_map_top_left_coordinates = player_coords[0] - SCREEN_RESOLUTION[0] // 2, player_coords[1] - SCREEN_RESOLUTION[1] // 2
        visible_block_map_bottom_right_coordinates = player_coords[0] + SCREEN_RESOLUTION[0] // 2, player_coords[1] + SCREEN_RESOLUTION[1] // 2

        visible_block_map = {}

        for block in block_map:
            block_coords = block.getCoordinates()
            if visible_block_map_top_left_coordinates[0] + VISIBLE_SCREEN_MARGIN[0] <= block_coords[0] <= visible_block_map_bottom_right_coordinates[0] - VISIBLE_SCREEN_MARGIN[0] and \
                visible_block_map_top_left_coordinates[1] + VISIBLE_SCREEN_MARGIN[1] <= block_coords[1] <= visible_block_map_bottom_right_coordinates[1] - VISIBLE_SCREEN_MARGIN[1]:
                block_relative_to_player_coords = block.getCoordinates()[0] - player_coords[0], block.getCoordinates()[1] - player_coords[1]
                block_relative_to_screen_coords = block_relative_to_player_coords[0] + SCREEN_RESOLUTION[0] // 2, block_relative_to_player_coords[1] + SCREEN_RESOLUTION[1] // 2
                block.calculateRect(block_relative_to_screen_coords)
                visible_block_map[block_coords] = block

        self._visible_block_map = visible_block_map

    def __handlePlayerControl(self):
        keys = pg.key.get_pressed()

        player_acceleration_vec = [0, 0] # up, down, left, right
        player = self.__model.getPlayer()

        if keys[pg.K_d]:
            player.changeCoordinatesBy((+PLAYER_SPEED, 0))
            player_acceleration_vec[0] += PLAYER_SPEED
        if keys[pg.K_a]:
            player.changeCoordinatesBy((-PLAYER_SPEED, 0))
            player_acceleration_vec[0] += -PLAYER_SPEED
        if keys[pg.K_w]:
            player.changeCoordinatesBy((0, -PLAYER_SPEED))
            player_acceleration_vec[1] += -PLAYER_SPEED
        if keys[pg.K_s]:
            player.changeCoordinatesBy((0, +PLAYER_SPEED))
            player_acceleration_vec[1] += PLAYER_SPEED

        player.setAcceleration(player_acceleration_vec)

    def __handleCollisions(self):
        entities = {self.__model.getPlayer()}
        for enemy in self.__model.getEnemies():
            entities.add(enemy)

        for block in self.getVisibleBlockMap().values():
            for entity in entities:
                self.__handleObjectCollisions(entity, block)

        for entity1 in entities:
            for entity2 in entities:
                if entity1 != entity2:
                    self.__handleObjectCollisions(entity1, entity2)

    def __handleObjectCollisions(self, _object1: Ship | Block, _object2: Ship | Block):
        _object1_coords = _object1.getCoordinates()
        _object2_coords = _object2.getCoordinates()

        distance = ((_object2_coords[0] - _object1_coords[0]) ** 2 + (
                _object2_coords[1] - _object1_coords[1]) ** 2) ** 0.5

        if distance <= COLLISION_DETECTION_RADIUS:
            do_collide = _object1.getRect().colliderect(_object2.getRect())
            if do_collide:
                object1_acceleration_vec = _object1.getAcceleration()
                object1_anti_acceleration_vec = []
                for i in object1_acceleration_vec:
                    object1_anti_acceleration_vec.append(5 * -i)

                _object1.changeCoordinatesBy((0, object1_anti_acceleration_vec[1]))
                _object1.changeCoordinatesBy((object1_anti_acceleration_vec[0], 0))

    @staticmethod
    def __applyCollisionsToBlockMap(block_map: list[list[Block]]):
        for i in range(len(block_map)):
            for j in range(len(block_map[i])):
                if i == 0 or i == len(block_map) - 1 or j == 0 or j == len(block_map) - 1:
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

    def __initBlockMap(self, seed: int = None):
        _perlin = perlin.Perlin2D(seed)
        _noise = _perlin.generatePerlin(MAP_SIZE, MAP_SCALE)

        block_map = self.__perlinToBlockMap(_noise)
        self.__model.setBlockMap(block_map)

    @staticmethod
    def __perlinToBlockMap(perlin_map: np.array) -> set[Block]:
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

        Presenter.__applyCollisionsToBlockMap(block_map)

        _island_map = set()
        for i in range(len(block_map)):
            for j in range(len(block_map[i])):
                if block_map[i][j].getBlockType() == BlockType.island:
                    _island_map.add(block_map[i][j])

        return _island_map

    def __initPlayer(self):
        player = Ship(
            [0, 0],
            SHIP_SIZE,
            PLAYER_BASE_HP)
        self.__model.setPlayer(player)


    def _calculateEnemiesRect(self):
        player_coords = tuple(self.__model.getPlayer().getCoordinates())

        visible_block_map_top_left_coordinates = player_coords[0] - SCREEN_RESOLUTION[0] // 2, player_coords[1] - \
                                                 SCREEN_RESOLUTION[1] // 2
        visible_block_map_bottom_right_coordinates = player_coords[0] + SCREEN_RESOLUTION[0] // 2, player_coords[1] + \
                                                     SCREEN_RESOLUTION[1] // 2

        for enemy in self.__model.getEnemies():
            enemy_coords = enemy.getCoordinates()
            if visible_block_map_top_left_coordinates[0] <= enemy_coords[0] <= visible_block_map_bottom_right_coordinates[0] and \
                visible_block_map_top_left_coordinates[1] <= enemy_coords[1] <= visible_block_map_bottom_right_coordinates[1]:
                enemy_relative_to_player_coords = enemy.getCoordinates()[0] - player_coords[0], enemy.getCoordinates()[1] - player_coords[1]
                enemy_relative_to_screen_coords = enemy_relative_to_player_coords[0] + SCREEN_RESOLUTION[0] // 2, enemy_relative_to_player_coords[1] + SCREEN_RESOLUTION[1] // 2

                enemy.calculateRect(enemy_relative_to_screen_coords)
                enemy.setIsVisible(True)
            else:
                enemy.setIsVisible(False)

    def _handleEnemiesMoving(self):
        player_coords = self.__model.getPlayer().getCoordinates()
        for enemy in self.__model.getEnemies():
            enemy_coords = enemy.getCoordinates()
            enemy_to_player_vec = [enemy_coords[0] - player_coords[0],
                                   enemy_coords[1] - player_coords[1]]
            if enemy_to_player_vec[0] >= 0:
                enemy_to_player_vec[0] = -ENEMY_SPEED
            else:
                enemy_to_player_vec[0] = +ENEMY_SPEED
            if enemy_to_player_vec[1] >= 0:
                enemy_to_player_vec[1] = -ENEMY_SPEED
            else:
                enemy_to_player_vec[1] = +ENEMY_SPEED

            enemy.setAcceleration(enemy_to_player_vec)
            enemy.changeCoordinatesBy(enemy_to_player_vec)

    def __handleEnemies(self):
        if self.__model.getLastTimeEnemySpawned() + ENEMY_SPAWN_INTERVAL <= time.monotonic():
            enemy_pos_x = random.randint(-MAP_SIZE[0] * DEFAULT_BLOCK_SIZE[0] // 2, MAP_SIZE[0] * DEFAULT_BLOCK_SIZE[0] // 2)
            enemy_pos_y = random.randint(-MAP_SIZE[1] * DEFAULT_BLOCK_SIZE[1] // 2,
                                         MAP_SIZE[1] * DEFAULT_BLOCK_SIZE[1] // 2)
            enemy = model.models.Ship(
                [enemy_pos_x, enemy_pos_y],
                SHIP_SIZE,
                BOT_BASE_HP
            )
            self.__model.addEnemy(enemy)
            self.__model.setLastTimeEnemySpawned(time.monotonic())

        self._handleEnemiesMoving()

        self._calculateEnemiesRect()