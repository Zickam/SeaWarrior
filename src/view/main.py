import view.ui_arrangement
from custom_types import *
from presenter.main import Presenter
from model.models import Model
from custom_enums import GameState
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

    def update(self, mouse_state: MouseState):
        self.__screen.fill(Colors.water_shadowed)

        for btn in self.__buttons:
            btn.value.update(self.__screen, mouse_state)



class GameplayView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter
        self.__buttons = view.ui_arrangement.GameplayGUI

        self.__buttons.pause.value.setActionOnClick(self.__presenter.togglePause)

    def update(self, mouse_state: MouseState):
        self.__screen.fill(Colors.water)
        self.__buttons.pause.value.update(self.__screen, mouse_state)


class SavesMenuView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter

        self.__buttons = view.ui_arrangement.SavesMenu
        self.__buttons.main_menu.value.setActionOnClick(presenter.openMainMenu)
        # self.__buttons.load_save.value.setActionOnClick(self.__presenter.)



    def update(self, mouse_state: MouseState):
        self.__screen.fill(Colors.water_shadowed)
        for btn in self.__buttons:
            btn.value.update(self.__screen, mouse_state)


class PauseMenuView:
    def __init__(self, screen: pg.display, presenter: Presenter):
        self.__screen = screen
        self.__presenter = presenter

        self.__buttons = view.ui_arrangement.PauseMenu
        self.__buttons.unpause.value.setActionOnClick(self.__presenter.togglePause)

    def update(self, mouse_state: MouseState):
        self.__screen.fill(Colors.water_shadowed)
        for btn in self.__buttons:
            btn.value.update(self.__screen, mouse_state)

class View:
    def __init__(self, presenter: Presenter, model: Model, screen_resolution: Vec2):
        self.__presenter = presenter
        self.__model = model

        self.__mouse_state = MouseState(False, False, (0, 0), 0.0)
        self.__screen = pg.display.set_mode(screen_resolution, vsync=True)
        self.__clock = pg.time.Clock()

        self.__main_menu_view = MainMenuView(self.__screen, presenter)
        self.__gameplay_view = GameplayView(self.__screen, presenter)
        self.__saves_menu_view = SavesMenuView(self.__screen, presenter)
        self.__pause_menu_view = PauseMenuView(self.__screen, presenter)

    def update(self):
        mouse_pressed = pg.mouse.get_pressed()
        self.__mouse_state.is_clicked_left = mouse_pressed[0]
        self.__mouse_state.is_clicked_right = mouse_pressed[2]
        self.__mouse_state.position = pg.mouse.get_pos()

        match self.__model.getGameState():
            case GameState.main_menu:
                self.__main_menu_view.update(self.__mouse_state)
            case GameState.saves_menu:
                self.__saves_menu_view.update(self.__mouse_state)
            case GameState.pause:
                self.__pause_menu_view.update(self.__mouse_state)
            case GameState.gameplay:
                self.__gameplay_view.update(self.__mouse_state)

        pg.display.flip()
        self.__clock.tick(FPS_CAP)

