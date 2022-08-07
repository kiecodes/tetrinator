from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

from ui.model import AppState

Builder.load_file('ui/training_view.kv')


class TrainingView(Widget):
    generations_view = ObjectProperty(None)
    tetris_view = ObjectProperty(None)

    def update(self, state: AppState):
        if self.generations_view:
            self.generations_view.update(state)
