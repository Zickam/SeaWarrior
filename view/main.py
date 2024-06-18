import enums
import view.ui_arrangement
from custom_types import *
from presenter.main import Presenter
from model.models import Model
from enums import BlockType, GameState
import model
from view.constants import *

import pygame as pg
pg.init()


class MainMenuView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter
        self.__buttons = view.ui_arrangement.MainMenu

    def update(self):
        self.__screen.fill(Colors.water_shadowed)
        for btn in self.__buttons:
            btn.value.update(self.__screen)

    def handleGUIEvents(self):
        ...


class GameplayView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter

    def update(self):
        self.__screen.fill(Colors.water)

    def handleGUIEvents(self):
        ...



class View:
    def __init__(self, presenter: Presenter, model: Model, screen_resolution: Vec2):
        self.__presenter = presenter
        self.__model = model

        self.__screen = pg.display.set_mode(screen_resolution, vsync=True)
        self.__clock = pg.time.Clock()

        self.__main_menu_view = MainMenuView(self.__screen, presenter)
        self.__gameplay_view = GameplayView(self.__screen, presenter)


    def update(self):
        match self.__model.getGameState():
            case enums.GameState.main_menu:
                self.__main_menu_view.update()
                self.__main_menu_view.handleGUIEvents()
            case enums.GameState.gameplay:
                self.__gameplay_view.update()
                self.__gameplay_view.handleGUIEvents()

        pg.display.flip()
        self.__clock.tick(FPS_CAP)

