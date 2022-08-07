from dataclasses import dataclass, field
from typing import List, Callable

from ui.model.generation import Generation


@dataclass
class AppState:
    num_generations: int = 0
    generations: List[Generation] = field(default_factory=list)
    on_generation_selected: Callable[[Generation], None] = None

    def add_generation(self, generation: Generation):
        self.generations.append(generation)
