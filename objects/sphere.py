import math
from typing import (
    List,
    Tuple
)

import numpy as np

from .mesh import Mesh

phiLength = math.pi * 2
thetaLength = math.pi


class Sphere(Mesh):
    def update(self):
        self.angle_x += 10
        self.angle_y += 10
        self.angle_z += 10
        self._verts.clear()

    @classmethod
    def make(
        cls,
        position: Tuple[float, float, float],
        colors: List[Tuple[int, int, int]],
        radius: float = 1.0,
        width_segments: int = 8,
        height_segments: int = 6
    ):
        index = 0
        grid: List[List[int]] = []
        vertices: List[Tuple[float, float, float]] = []
        indices: List[Tuple[int, ...]] = []

        for iy in range(height_segments + 1):
            vertices_row: List[int] = []
            v = iy / height_segments

            for ix in range(width_segments + 1):
                u = ix / width_segments

                vertices.append((
                    -radius * math.cos(u * phiLength) * math.sin(v * thetaLength),
                    radius * math.cos(v * thetaLength),
                    radius * math.sin(u * phiLength) * math.sin(v * thetaLength)
                ))
                vertices_row.append(index)
                index += 1

            grid.append(vertices_row)

        for iy in range(height_segments):
            for ix in range(width_segments):
                a = grid[iy][ix + 1]
                b = grid[iy][ix]
                c = grid[iy + 1][ix]
                d = grid[iy + 1][ix + 1]

                if iy != 0:
                    indices.append((a, b, d))

                if iy != height_segments - 1:
                    indices.append((b, c, d))

        angles = np.array([0, 0, 0])

        return cls(
            vertices=vertices,
            faces=indices,
            colors=colors,
            position=position,
            angles=angles
        )
