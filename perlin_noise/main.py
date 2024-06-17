import random
import math

import numpy as np
import numba

# from custom_types import *
Vec2 = tuple[float | int, float | int]


class Perlin2D:
    GRADIENT_VECTORS = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1)
    )

    PERMUTATION_TABLE_SIZE = 1023

    def __init__(self, seed: int | None = None):
        if seed is None:
            seed = np.random.randint(0, 2 ** 31)
        print(f"Using seed: {seed}")

        np.random.seed(seed)
        self.__random = np.random.default_rng(seed=seed)

        self.__permutation_table = [i for i in range(self.PERMUTATION_TABLE_SIZE)]
        np.random.shuffle(self.__permutation_table)

    def __getRandomInt(self) -> int:
        return int(self.__random.random() *
                   10 ** (math.ceil(self.PERMUTATION_TABLE_SIZE ** 0.1) + 1)
                   % self.PERMUTATION_TABLE_SIZE)

    def __getRandomVectors(self) -> np.array:
        vectors = np.full((4, 2), 0)
        for i in range(4):
            sign_1 = 1 if self.__random.random() > 0.5 else -1
            sign_2 = 1 if self.__random.random() > 0.5 else -1
            vectors[i] = (self.__random.random() * sign_1,
                          self.__random.random() * sign_2)
        return vectors

    def __getPseudoRandomGradientVector(self, point: Vec2) -> Vec2:
        vector_num_idx = (((point[0] * 1836311903) ^ (point[1] * 2971215073) + 4807526976) & (self.PERMUTATION_TABLE_SIZE - 1))
        vector_num = self.__permutation_table[vector_num_idx] & 3
        return self.GRADIENT_VECTORS[vector_num]

    def __getQuintic(self, t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    def __getExtrapolated(self, a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def __getScalarProduct(self, a: Vec2, b: Vec2) -> float:
        return a[0] * b[0] + a[1] * b[1]

    def __getPerlin(self, point: Vec2) -> float:
        left = math.floor(point[0])
        top = math.floor(point[1])
        point_quad_x = point[0] - left
        point_quad_y = point[1] - top

        # print(left, top, point_quad_x, point_quad_y)

        top_left_gradient = self.__getPseudoRandomGradientVector((left, top))
        top_right_gradient = self.__getPseudoRandomGradientVector((left + 1, top))
        bottom_left_gradient = self.__getPseudoRandomGradientVector((left, top + 1))
        bottom_right_gradient = self.__getPseudoRandomGradientVector((left + 1, top + 1))

        distance_to_top_left = point_quad_x, point_quad_y
        distance_to_top_right = point_quad_x - 1, point_quad_y
        distance_to_bottom_left = point_quad_x, point_quad_y - 1
        distance_to_bottom_right = point_quad_x - 1, point_quad_y - 1

        tx1 = self.__getScalarProduct(distance_to_top_left, top_left_gradient)
        tx2 = self.__getScalarProduct(distance_to_top_right, top_right_gradient)
        bx1 = self.__getScalarProduct(distance_to_bottom_left, bottom_left_gradient)
        bx2 = self.__getScalarProduct(distance_to_bottom_right, bottom_right_gradient)

        point_quad_x = self.__getQuintic(point_quad_x)
        point_quad_y = self.__getQuintic(point_quad_y)

        tx = self.__getExtrapolated(tx1, tx2, point_quad_x)
        bx = self.__getExtrapolated(bx1, bx2, point_quad_y)
        tb = self.__getExtrapolated(tx, bx, point_quad_y)

        return tb

    def getPerlin(self, point: Vec2, octaves: int, persistence: float = 0.5) -> float:
        tmp_point = [point[0], point[1]]
        amplitude = 1
        max_val = 0
        result = 0

        while octaves > 0:
            max_val += amplitude
            result += self.__getPerlin(tmp_point) * amplitude
            amplitude *= persistence
            tmp_point[0] *= 2
            tmp_point[1] *= 2

            octaves -= 1

        return result / max_val


if __name__ == "__main__":
    # import pygame as pg
    #
    # pg.init()
    #
    # perlin = Perlin2D()
    #
    # # Set up the drawing window
    # screen = pg.display.set_mode([500, 500])
    # clock = pg.time.Clock()
    # # Run until the user asks to quit
    # running = True
    # while running:
    #
    #     # Did the user click the window close button?
    #     for event in pg.event.get():
    #         if event.type == pg.QUIT:
    #             running = False
    #
    #     # Fill the background with white
    #     screen.fill((255, 255, 255))
    #
    #     # Draw a solid blue circle in the center
    #     step = 0.1
    #     i = 0
    #
    #     while i < 16:
    #         j = 0
    #         while j < 16:
    #             point_perlin = perlin.getPerlin((i, j), 4)
    #             # print(point_perlin)
    #             color = int(256 * abs(point_perlin))
    #             print(color)
    #             pg.draw.rect(screen, (color, color, color), (int(i * 10), int(j * 10), int(i) + 1, int(j) + 1), 1)
    #             j += step
    #         i += step
    #
    #     # Flip the display
    #     pg.display.flip()
    #     clock.tick(1)
    #
    # # Done! Time to quit.
    # pg.quit()
    import cv2

    perlin = Perlin2D(1)
    i = 0
    step = 0.1
    img = np.full((160, 160, 3), 0)
    while i < 16:
        j = 0
        while j < 16:
            point_perlin = perlin.getPerlin((i, j), 4)
            color = int(256 * abs(point_perlin))
            # print(color)
            if color > 255 or color < 0:
                print("shit")
                break

            img[int(i), int(j)] = (color, color, color)
            j += step
        i += step
    print(img)
    img = img.astype(np.uint8)
    cv2.imshow("pohuy", img)
