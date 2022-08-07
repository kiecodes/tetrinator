from dataclasses import dataclass, field
from typing import List

from model import Generation


@dataclass
class AppState:
    num_generations: int = 0
    generations: List[Generation] = field(default_factory=list)

    def add_generation(self, min_fitness: int, max_fitness: int):
        self.generations.append(Generation(min_fitness, max_fitness))
