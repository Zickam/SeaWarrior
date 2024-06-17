from __future__ import annotations
import random
import math
from types import FunctionType
from enum import Enum

import numpy as np
# import numba

# from custom_types import *
Vec2 = tuple[float | int, float | int]


class Perlin2D:
    class Normalization(Enum):
        normalization_1 = 1
        normalization_2 = 2

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

    def getPerlinAt(self, point: Vec2, octaves: int, persistence: float = 0.5) -> float:
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

    def __normalization1(self, x: float) -> float:
        return int(255 * abs(x))

    def __normalization2(self, x: float, min_val: float, max_val: float) -> float:
        offset = -min_val
        return (x + offset) / (max_val + offset)

    def __getMaxAndMinValues(self, perlin: list[list[float]]) -> tuple[float, float]:
        min_perlin = 10 ** 10
        max_perlin = -10 ** 10

        for i in perlin:
            for j in i:
                if j > max_perlin:
                    max_perlin = j
                if j < min_perlin:
                    min_perlin = j

        return max_perlin, min_perlin

    def __normalizePerlin(self, perlin: list[list[float]], normalization_func_enum: Perlin2D.Normalization.__dict__):
        match normalization_func_enum:
            case Perlin2D.Normalization.normalization_1:
                ...
            case Perlin2D.Normalization.normalization_2:
                max_val, min_val = self.__getMaxAndMinValues(perlin)

        for i in range(len(perlin)):
            for j in range(len(perlin[i])):
                match normalization_func_enum:
                    case Perlin2D.Normalization.normalization_1:
                        color = self.__normalization1(perlin[i][j])
                    case Perlin2D.Normalization.normalization_2:
                        color = self.__normalization2(perlin[i][j], min_val, max_val)
                perlin[i][j] = (color, 0, 0)

    def getPerlin(self, width: int, height: int, step: float, octaves: int, normalization_func_enum: Perlin2D.Normalization.__dict__) -> list[list[float]]:
        """Returns a matrix consisting of """
        if not (normalization_func_enum in Perlin2D.Normalization):
            raise Exception(f"Undefined normalization function: {normalization_func_enum}")

        perlin_values = []
        i = 0
        while i < width:
            j = 0
            perlin_values.append([])
            while j < height:
                point_perlin = self.getPerlinAt((i / width, j / height), 1)
                perlin_values[-1].append(point_perlin)

                j += step
            i += step

        self.__normalizePerlin(perlin_values, normalization_func_enum)

        return perlin_values

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    perlin = Perlin2D(1)

    values = perlin.getPerlin(256, 256, 1, 1, Perlin2D.Normalization.normalization_2)
    plt.title("Perlin Noise")
    plt.xlabel("Time")
    plt.ylabel("Value")
    plt.imshow(values)
    plt.subplot()
    plt.show()