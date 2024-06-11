# generator that uses perlin noise to produce
# a sea like map with islands within the whole infinite (or finite)
# sea with only two basic heights levels: 0 (sea level)
# and 1 (ground level which is higher than sea level)

import numpy as np

from custom_types import *

class PerlinNoise:
    @staticmethod
    def generate(coordinates: Vec2) -> float:
        raise NotImplementedError

class Generator:
    def __init__(self, seed: int):
        self.__seed = seed

    def getPointValue(self, coordinates: Vec2) -> float:
        raise NotImplementedError

    def getGeneratedMap(self, start: Vec2, end: Vec2) -> np.array:
        raise NotImplementedError


if __name__ == "__main__":
    generator = Generator(123)
