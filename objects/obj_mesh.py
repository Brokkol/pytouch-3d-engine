from typing import (
    List,
    Tuple
)

import numpy as np
from .mesh import Mesh


class ObjMesh(Mesh):
    @classmethod
    def from_file(
        cls,
        file_path: str,
        position: Tuple[float, float, float],
        colors: List[Tuple[int, int, int]],
    ):
        vertices: List[Tuple[float, float, float]] = []
        faces: List[Tuple[int, ...]] = []

        with open(
            file=file_path,
            mode='r',
            encoding='utf-8'
        ) as fh:
            for line in fh:
                if line.startswith('#'):
                    continue

                line = line.strip()
                parts = line.split(' ')
                preffix, info = parts[0].strip(), parts[1:]
                if not preffix:
                    continue

                if preffix == 'v':
                    (x, y, z,) = map(float, info)
                    vertices.append((x, y, z))
                elif preffix == 'f':
                    faces.append(tuple([
                        int(item.split('/')[0]) - 1
                        for item in info
                    ]))

        angles = np.array([0, 0, 0])

        return cls(
            vertices=vertices,
            faces=faces,
            colors=colors,
            position=position,
            angles=angles
        )
