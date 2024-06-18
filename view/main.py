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

        self.__buttons.start_btn.value.setActionOnClick(self.__presenter.startGameplay)
        self.__buttons.saves_btn.value.setActionOnClick(self.__presenter.openSavesMenu)
        self.__buttons.exit_btn.value.setActionOnClick(exit)

    def update(self):
        self.__screen.fill(Colors.water_shadowed)
        mouse_pressed = pg.mouse.get_pressed()
        mouse_state = MouseState(is_clicked_left=mouse_pressed[0], is_clicked_right=mouse_pressed[2], position=pg.mouse.get_pos())

        for btn in self.__buttons:
            btn.value.update(self.__screen, mouse_state)



class GameplayView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter
        self.__buttons = view.ui_arrangement.GameplayGUI

        self.__buttons.pause.value.setActionOnClick(self.__presenter.togglePause)

    def update(self):
        self.__screen.fill(Colors.water)


class SavesMenuView:
    def __init__(self, screen: pg.display, ):
        ...


class View:
    def __init__(self, presenter: Presenter, model: Model, screen_resolution: Vec2):
        self.__presenter = presenter
        self.__model = model

        self.__screen = pg.display.set_mode(screen_resolution, vsync=True)
        self.__clock = pg.time.Clock()

        self.__main_menu_view = MainMenuView(self.__screen, presenter)
        self.__gameplay_view = GameplayView(self.__screen, presenter)
        # self.__saves_menu_view = SavesMenuView(self.__screen, presenter)


    def update(self):
        match self.__model.getGameState():
            case GameState.main_menu:
                self.__main_menu_view.update()
            case GameState.saves_menu:
                self.__saves_menu_view.update()
                # self.__saves_menu_view.()
            case GameState.gameplay:
                self.__gameplay_view.update()

        pg.display.flip()
        self.__clock.tick(FPS_CAP)

