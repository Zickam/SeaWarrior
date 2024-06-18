import pygame as pg

from model.main import Model


class Presenter:
    def __init__(self, model: Model):
        self.__model = model

    def __handlePlayerControl(self, keys):
        keys = pg.key.get_pressed()

        if keys[""dawd]

    def __handleKeys(self):
        keys = pg.key.get_pressed()

    def handleEvents(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()



