from dataclasses import dataclass
from typing import List


@dataclass
class Generation:
    min_fitness: int
    max_fitness: int
    genome: List[float]
