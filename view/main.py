import enums
from custom_types import *
from presenter.main import Presenter
from model.main import Model
from enums import BlockType, GameState
import model
import constants

import pygame as pg
pg.init()

class Colors:
    white = (255, 255, 255)
    black = (0, 0, 0)

    water = (0, 0, 255)
    island = (211, 237, 21)
    ship = (128, 128, 128)
    bullet = (0, 0, 0)

    water_shadowed = (0, 0, 128)


class Button:
    def __init__(self, position: Vec2, size: Vec2, action: Vec2):
        self.__position = position
        self.__size = size
        self.__action = action

    def onClick(self):
        self.__action()

class MainMenuView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter

    def update(self):
        self.__screen.fill(Colors.water_shadowed)




class GameplayView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter

    def update(self):
        self.__screen.fill(Colors.water)





class View:
    def __init__(self, presenter: Presenter, model: Model, screen_resolution: Vec2):
        self.__presenter = presenter
        self.__model = model

        self.__screen = pg.display.set_mode(screen_resolution, vsync=True)
        self.__clock = pg.time.Clock()

        self.__main_menu_view = MainMenuView(self.__screen, presenter)
        self.__gameplay_view = GameplayView(self.__screen, presenter)

    def handleGUIEvents(self):
    # buttons clicking... clicking on the screen to shoot


    def update(self):
        match self.__model.getGameState():
            case enums.GameState.main_menu:
                self.__main_menu_view.update()
            case enums.GameState.gameplay:
                self.__gameplay_view.update()

        pg.display.flip()
        self.__clock.tick(constants.FPS_CAP)

