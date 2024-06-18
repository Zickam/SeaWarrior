import pygame as pg

from enums import *
from model.models import Model
from model import models


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
        self.__model.setIsPause(not self.__model.isPause())
        if self.__model.isPause():
            self.__model.setGameState(GameState.pause)
        else:
            self.__model.setGameState(GameState.gameplay)

    def openSavesMenu(self):
        self.__model.setGameState(GameState.saves_menu)