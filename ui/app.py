from typing import Callable, List

from kivy.app import App

from ui.model import AppState, Generation
from ui import TrainingView


class Tetrinator(App):

    def __init__(self, on_generation_selected: Callable[[Generation], None], **kwargs):
        super().__init__(**kwargs)
        self.on_genome_selected = None
        self.training_view = TrainingView()
        self.app_state = AppState(
            on_generation_selected=on_generation_selected
        )

    def build(self):
        return self.training_view

    def _update(self, state: AppState):
        self.training_view.update(state)

    def add_generation(self, min_fitness: int, max_fitness: int, genome: List[float]):
        self.app_state.add_generation(Generation(min_fitness, max_fitness, genome))
        self._update(self.app_state)
