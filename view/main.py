import enums

import model
from custom_types import *
from presenter.main import Presenter

class Window:
    def __init__(self, game: model.main.Game, resolution: Vec2, position: Vec2 = None):
        self.__game = game
        self.__resolution = resolution
        if position is None:
            position = self.__resolution[0] / 2, self.__resolution[1] // 2
        self.__position = position

        self.__main_menu = MainMenu()

    def update(self):
        match self.__game.getState():
            case enums.GameState.main_menu:
                self.__main_menu.update()
            case enums.GameState.gameplay:
                raise NotImplementedError

class Button:
    def __init__(self, position: Vec2, size: Vec2, action: Vec2):
        self.__position = position
        self.__size = size
        self.__action = action

    def onClick(self):
        self.__action()

class MainMenuView:
    def __init__(self, presenter):
        self.button_start = Button(
            (0, 0),
            (100, 200),
            # lambda controller.
        )


class GameplayView:
    def __init__(self):
        ...


class View:
    def __init__(self, presenter: Presenter):
        self.__main_menu_view = MainMenuView(presenter)
        self.__gameplay_view = GameplayView(presenter)