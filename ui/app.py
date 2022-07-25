from kivy.app import App

from ui.training_view import TrainingView


class Tetrinator(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.training_view = TrainingView()

    def build(self):
        return self.training_view
