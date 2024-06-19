import pygame as pg

from custom_enums import *
from model.models import Model


class ConfigManager:
    CONFIG_DIR = "data/config"
    def __init__(self):
        ...


class Presenter:
    def __init__(self, model: Model):
        self.__model = model

    def __handlePlayerControl(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.__model.getPlayer().changeCoordinatesBy((-1, 0))

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()

    def startGameplay(self):
        self.__model.setGameState(GameState.gameplay)

        self.__model.initMap()
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