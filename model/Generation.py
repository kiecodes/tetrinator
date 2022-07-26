from dataclasses import dataclass


@dataclass
class Generation:
    min_fitness: int
    max_fitness: int