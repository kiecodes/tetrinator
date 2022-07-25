from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget

Builder.load_file('ui/training_view.kv')


class TrainingView(Widget):
    tetris_view = ObjectProperty(None)
