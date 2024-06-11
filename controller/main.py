import model
import view.main


class PlayerInput:
    def __init__(self):
        ...

class Bot:
    def __init__(self):
        ...

class MainMenuController:
    def __init__(self, model: model.main.Game, main_menu_view: view.main.MainMenu):
        self.__model = model
        self.__main_menu_view = main_menu_view

    # def handleButtons(self):
    #     if self.__main_menu_view

class SavesMenuController:
    def __init__(self):
        ...

class GameplayController:
    def __init__(self):
        ...

class DeathScreenController:
    def __init__(self):
        ...


