import random
import time

import pygame as pg
import numpy as np

import model.models
from custom_enums import *
from model.models import Model, Block
from custom_types import Vec2
from model.constants import MAP_SIZE
from view.constants import *
from model.constants import PLAYER_SPEED, VISIBLE_SCREEN_MARGIN, COLLISION_DETECTION_RADIUS, ENEMY_SPAWN_INTERVAL
from model.constants import *

class ConfigManager:
    CONFIG_DIR = "data/config"
    def __init__(self):
        ...


class Presenter:
    def __init__(self, model: Model):
        self.__model = model
        # self._visible_block_map = self.__updateVisibleBlockMap()

    def getEnemies(self):
        return self.__model.getEnemies()

    def getVisibleBlockMap(self):
        return self._visible_block_map

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

    def getPlayer(self):
        return self.__model.getPlayer()

    def __handlePlayerControl(self):
        keys = pg.key.get_pressed()

        player_acceleration_vec = [0, 0, 0, 0] # up, down, left, right

        if keys[pg.K_d]:
            self.__model.getPlayer().changeCoordinatesBy((+PLAYER_SPEED, 0))
            player_acceleration_vec[3] = PLAYER_SPEED
        if keys[pg.K_a]:
            self.__model.getPlayer().changeCoordinatesBy((-PLAYER_SPEED, 0))
            player_acceleration_vec[2] = -PLAYER_SPEED
        if keys[pg.K_w]:
            self.__model.getPlayer().changeCoordinatesBy((0, -PLAYER_SPEED))
            player_acceleration_vec[0] = -PLAYER_SPEED
        if keys[pg.K_s]:
            self.__model.getPlayer().changeCoordinatesBy((0, +PLAYER_SPEED))
            player_acceleration_vec[1] = PLAYER_SPEED

        self.__handleCollisions(player_acceleration_vec)


    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def __handleCollisions(self, player_acceleration_vec: list[int]):

        player_anti_acceleration_vec = []
        for i in player_acceleration_vec:
            player_anti_acceleration_vec.append(5 * -i)

        player_coords = tuple(self.__model.getPlayer().getCoordinates())
        player_rect = self.__model.getPlayer().getRect()

        for block_coords, block in self.getVisibleBlockMap().items():
            if block.getBlockType() == BlockType.island and block.getIsPhysical():
                distance = ((block_coords[0] - player_coords[0]) ** 2 + (block_coords[1] - player_coords[1]) ** 2) ** 0.5

                if distance <= COLLISION_DETECTION_RADIUS:
                    do_collide = block.getRect().colliderect(player_rect)
                    if do_collide:
                        self.__model.getPlayer().changeCoordinatesBy((0, player_anti_acceleration_vec[0]))
                        self.__model.getPlayer().changeCoordinatesBy((0, player_anti_acceleration_vec[1]))
                        self.__model.getPlayer().changeCoordinatesBy((player_anti_acceleration_vec[2], 0))
                        self.__model.getPlayer().changeCoordinatesBy((player_anti_acceleration_vec[3], 0))

                        # print(f"colission")

    def startGameplay(self):
        self.__model.setGameState(GameState.gameplay)

        self.__model.initBlockMap()
        self.__model.initPlayer()

    def togglePause(self):
        if self.__model.getGameState() == GameState.pause:
            self.__model.setGameState(GameState.gameplay)
        else:
            self.__model.setGameState(GameState.pause)


    def openSavesMenu(self):
        self.__model.setGameState(GameState.saves_menu)

    def openMainMenu(self):
        self.__model.setGameState(GameState.main_menu)

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
                print(enemy_relative_to_player_coords)
                enemy_relative_to_screen_coords = enemy_relative_to_player_coords[0] + SCREEN_RESOLUTION[0] // 2, enemy_relative_to_player_coords[1] + SCREEN_RESOLUTION[1] // 2
                enemy.calculateRect(enemy_relative_to_screen_coords)
                enemy.setIsVisible(True)
            else:
                enemy.setIsVisible(False)

    def _handleEnemiesMoving(self):
        ...
        for enemy in self.__model.getEnemies():
            enemy.changeCoordinatesBy((0.01, 0))

    def __handleEnemies(self):
        if self.__model.getLastTimeEnemySpawned() + ENEMY_SPAWN_INTERVAL <= time.monotonic():
            enemy_pos_x = random.randint(-MAP_SIZE[0] * DEFAULT_BLOCK_SIZE[0] // 2, MAP_SIZE[0] * DEFAULT_BLOCK_SIZE[0] // 2)
            enemy_pos_y = random.randint(-MAP_SIZE[1] * DEFAULT_BLOCK_SIZE[1] // 2,
                                         MAP_SIZE[1] * DEFAULT_BLOCK_SIZE[1] // 2)
            enemy = model.models.Ship(
                SHIP_SIZE,
                [enemy_pos_x, enemy_pos_y],
                BOT_BASE_HP
            )
            self.__model.addEnemy(enemy)
            self.__model.setLastTimeEnemySpawned(time.monotonic())

        self._handleEnemiesMoving()

        self._calculateEnemiesRect()


    def tickGameplay(self):
        if hasattr(self.__model, "_player"):
            self.__updateVisibleBlockMap()
            self.__handlePlayerControl()

        self.__handleEnemies()



