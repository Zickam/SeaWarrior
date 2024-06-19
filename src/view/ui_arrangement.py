from enum import Enum

from view.ui_elements import *


class MainMenu(Enum):
    start_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 40), BTN_SIZE, "START")
    saves_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2), BTN_SIZE, "SAVES")
    exit_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), BTN_SIZE, "QUIT")

class GameplayGUI(Enum):
    pause = Button((0, 0), BTN_SIZE, "PAUSE")

class SavesMenu(Enum):
    load_save = Button((SCREEN_RESOLUTION[0] // 2 - 30, SCREEN_RESOLUTION[1] // 2 + 40), BTN_SIZE, "LOAD")
    main_menu = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), BTN_SIZE, "MAIN MENU")
    save_save = Button((SCREEN_RESOLUTION[0] // 2 + 30, SCREEN_RESOLUTION[1] // 2 + 40), BTN_SIZE, "SAVE")
