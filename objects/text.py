from typing import (
    List,
    Tuple
)

import freetype
import numpy as np

from .mesh import Mesh

FREETYPE_FLAGS = freetype.FT_LOAD_DEFAULT | freetype.FT_LOAD_NO_BITMAP


class Text(Mesh):
    @classmethod
    def from_string(
        cls,
        string: str,
        position: Tuple[float, float, float],
        colors: List[Tuple[int, int, int]],
        font: str = 'arial.ttf',
        seperator_length: float = 5.0,
        depth: float = 10.0,
        height: int = 64,
        width: int = 32
    ):
        freetype_font = freetype.Face(font)
        freetype_font.set_char_size(width, height)

        vertices: List[Tuple[float, float, float]] = []
        faces:  List[Tuple[int, ...]] = []

        for offset, char in enumerate(string):
            freetype_font.load_char(char, FREETYPE_FLAGS)
            slot = freetype_font.glyph
            outline = slot.outline.points
            if not outline:
                continue

            offset *= width + seperator_length

            outline_z = [(x + offset, y, 0) for x, y in outline]
            index = len(vertices)
            vertices.extend(outline_z)
            face = tuple(range(index, index + len(outline_z)))
            faces.append(face)

            outline_z = [(x + offset, y, depth) for x, y in outline]
            index = len(vertices)
            vertices.extend(outline_z)
            face = tuple(range(index, index + len(outline_z)))
            faces.append(face)

            faces.extend([
                (i - len(outline_z), i + 1 - len(outline_z), i + 1, i)
                for i in range(index, index + len(outline_z) - 1)
            ])

        angles = np.array([180, 0, 0])

        return cls(
            vertices=vertices,
            faces=faces,
            colors=colors,
            position=position,
            angles=angles
        )
