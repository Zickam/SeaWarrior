import pygame as pg

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



