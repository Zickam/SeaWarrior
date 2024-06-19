from typing import NamedTuple

Vec2 = tuple[int | float, int | float]

class MouseState(NamedTuple):
    is_clicked_left: bool
    is_clicked_right: bool
    position: Vec2