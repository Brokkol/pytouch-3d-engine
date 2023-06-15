import math
from random import randint
from typing import (
    List,
    Tuple
)

import numpy as np


class Mesh:
    angle_scale = math.pi / 180.0

    def __init__(
        self,
        vertices: List[Tuple[float, float, float]],
        faces: List[Tuple[int, ...]],
        colors: List[Tuple[int, int, int]],
        position: Tuple[float, float, float],
        angles: np.array
    ):
        self.vertices = vertices
        self.faces = faces

        if not colors:
            colors = [
                (randint(0, 255), randint(0, 255), randint(0, 255))
                for _ in range(len(self.faces))
            ]

        self.colors = colors
        self._position = position
        self._angles = angles
        self._verts: List[Tuple[float, float, float]] = []

    @property
    def verts(self) -> List[Tuple[float, float, float]]:
        if not self._verts:
            self._verts = [[self.position[i] + v[i] / 2 for i in range(3)] for v in np.dot(self.vertices, self.R())]
        return self._verts

    def rebuild(self):
        self._verts.clear()

    @property
    def angle_x(self) -> float:
        return self._angles[0]

    @property
    def angle_y(self) -> float:
        return self._angles[1]

    @property
    def angle_z(self) -> float:
        return self._angles[2]

    @angle_x.setter
    def angle_x(self, value: float):
        self._angles[0] = abs(value % 360)

    @angle_y.setter
    def angle_y(self, value: float):
        self._angles[1] = abs(value % 360)

    @angle_z.setter
    def angle_z(self, value: float):
        self._angles[2] = abs(value % 360)

    @property
    def angles(self):
        return self._angles

    @angles.setter
    def angles(self, value: np.array):
        self._angles = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float, float]):
        self._position = value

    def R(self):
        sx, sy, sz = np.sin(self._angles * self.angle_scale)
        cx, cy, cz = np.cos(self._angles * self.angle_scale)

        return np.array(
            [
                [cy * cz, -cy * sz, sy],
                [cx * sz + cz * sx * sy, cx * cz - sx * sy * sz, -cy * sx],
                [sx * sz - cx * cz * sy, cz * sx + cx * sy * sz, cx * cy]
            ]
        )

    def update(self):
        pass

    def scale(self, k: float):
        self.vertices = [
            tuple([r * k for r in v])
            for v in self.vertices
        ]

    def copy(self):
        return Mesh(
            self.vertices.copy(),
            self.faces.copy(),
            self.colors.copy(),
            self.position,
            self.angles.copy()
        )
