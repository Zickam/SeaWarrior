from enum import Enum

from view.ui_elements import *
from view.constants import *


class MainMenu(Enum):
    start_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 - 40), BTN_SIZE, "START")
    saves_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2), BTN_SIZE, "SAVES")
    exit_btn = Button((SCREEN_RESOLUTION[0] // 2, SCREEN_RESOLUTION[1] // 2 + 40), BTN_SIZE, "QUIT")



