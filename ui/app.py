from kivy.app import App

from model import AppState
from ui import TrainingView


class Tetrinator(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.training_view = TrainingView()

    def build(self):
        return self.training_view

    def update(self, state: AppState):
        self.training_view.update(state)
