from types import FunctionType

from custom_types import *
import exceptions

class Button:
    def __init__(self, position: Vec2, size: Vec2):
        self.__position = position
        self.__size = size
        self.__action: FunctionType

    def setOnClick(self, action: FunctionType):
        if not isinstance(action, FunctionType):
            raise exceptions.IncorrectActionType(type(action))
        self.__action = action

    def onClick(self):
        try:
            self.__action()
        except Exception as ex:
            raise

