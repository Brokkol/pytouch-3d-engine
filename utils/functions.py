import random
from typing import List, Tuple


def random_color():
    return (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def gradient(start=(0, 0, 0), end=(0, 0, 0), n: int = 10) -> List[Tuple[int, int, int]]:
    p = [(end[i] - start[i]) // n for i in range(3)]
    return [
        (
            start[0] + p[0] * i,
            start[1] + p[1] * i,
            start[2] + p[2] * i,
        )
        for i in range(n)
    ]
