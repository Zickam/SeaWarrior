import pygame as pg
import numpy as np

from custom_enums import *
from model.models import Model, Block
from custom_types import Vec2
from model.constants import MAP_SIZE
from view.constants import *
from model.constants import PLAYER_SPEED, VISIBLE_SCREEN_MARGIN


class ConfigManager:
    CONFIG_DIR = "data/config"
    def __init__(self):
        ...


class Presenter:
    def __init__(self, model: Model):
        self.__model = model

    def getVisibleBlockMap(self) -> dict[Vec2, Block]:
        block_map = self.__model.getBlockMap()
        player_coords = self.__model.getPlayer().getCoordinates()

        visible_block_map_top_left_coordinates = player_coords[0] - SCREEN_RESOLUTION[0] // 2, player_coords[1] - SCREEN_RESOLUTION[1] // 2
        visible_block_map_bottom_right_coordinates = player_coords[0] // 2 + SCREEN_RESOLUTION[0] // 2, player_coords[1] // 2 + SCREEN_RESOLUTION[1] // 2

        visible_block_map = {}

        for row in block_map:
            for block in row:
                block_coords = block.getCoordinates()
                if visible_block_map_top_left_coordinates[0] + VISIBLE_SCREEN_MARGIN[0] <= block_coords[0] <= visible_block_map_bottom_right_coordinates[0] - VISIBLE_SCREEN_MARGIN[0] and \
                    visible_block_map_top_left_coordinates[1] + VISIBLE_SCREEN_MARGIN[1] <= block_coords[1] <= visible_block_map_bottom_right_coordinates[1] - VISIBLE_SCREEN_MARGIN[1]:
                    block_relative_to_player_coords = block.getCoordinates()[0] - player_coords[0], block.getCoordinates()[1] - player_coords[1]
                    block_relative_to_screen_coords = block_relative_to_player_coords[0] + SCREEN_RESOLUTION[0] // 2, block_relative_to_player_coords[1] + SCREEN_RESOLUTION[1] // 2
                    block.calculateRect(block_relative_to_screen_coords)
                    visible_block_map[block_coords] = block


        return visible_block_map

    def getPlayer(self):
        return self.__model.getPlayer()

    def __handlePlayerControl(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_d]:
            self.__model.getPlayer().changeCoordinatesBy((+PLAYER_SPEED, 0))
        if keys[pg.K_a]:
            self.__model.getPlayer().changeCoordinatesBy((-PLAYER_SPEED, 0))
        if keys[pg.K_w]:
            self.__model.getPlayer().changeCoordinatesBy((0, -PLAYER_SPEED))
        if keys[pg.K_s]:
            self.__model.getPlayer().changeCoordinatesBy((0, +PLAYER_SPEED))


    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

        self.__handlePlayerControl()

    def startGameplay(self):
        self.__model.setGameState(GameState.gameplay)

        self.__model.initBlockMap(1)
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

