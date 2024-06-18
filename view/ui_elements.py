from types import FunctionType

from custom_types import *
from view.constants import *

import pygame as pg
pg.font.init()

class MouseState:
    def __init__(self, is_clicked: bool, mouse_pos: Vec2):
        self.__is_clicked = is_clicked
        self.__mouse_pos = mouse_pos




class Button:
    def __init__(self, position: Vec2, size: Vec2, text: str = "Plain text"):
        self.__size = size
        self.__position = position[0] - size[0] // 2, position[1] - size[1] // 2
        self.__text = text
        self.__action: FunctionType

        self.__top_left_point = self.__position[0], self.__position[1]
        self.__bottom_right_point = self.__position[0] + self.__size[0], self.__position[1] + self.__size[1]

        self.__rect = pg.Rect((self.__top_left_point[0], self.__top_left_point[1]), (self.__size[0], self.__size[1]))
        self.__font = pg.font.SysFont("Comic Sans MS", 20 )
        self.__text_box = self.__font.render(self.__text, True, Colors.black)

    def isMouseInBoundaries(self, mouse_pos: Vec2) -> bool:
        if self.__top_left_point[0] <= mouse_pos[0] <= self.__bottom_right_point[0] and \
                self.__top_left_point[1] <= mouse_pos[1] <= self.__bottom_right_point[1]:
            return True
        return False

    def setActionOnClick(self, action: FunctionType):
        if not isinstance(action, FunctionType):
            raise Exception(f"action should be FunctionType type. Actual type is {type(action)}")
        self.__action = action

    def onClick(self):
        try:
            self.__action()
        except Exception as ex:
            raise Exception(f"Action wasn't set before the actual call. {ex}")

    def isClicked(self):
        ...

    def update(self, screen: pg.display, ):
        pg.draw.rect(screen, Colors.white, self.__rect)
        screen.blit(self.__text_box, self.__position)

        d
