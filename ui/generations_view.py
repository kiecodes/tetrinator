from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.stacklayout import StackLayout
from kivy.uix.widget import Widget

from model import AppState

Builder.load_file('ui/generations_view.kv')


class GenerationsEntryView(Widget):
    generation_id = NumericProperty()
    max_fitness = NumericProperty()
    min_fitness = NumericProperty()
    selected = BooleanProperty(False)

    click_handler = None

    def __init__(self, **kwargs):
        if "click_handler" in kwargs:
            self.click_handler = kwargs.pop("click_handler")
        super().__init__(**kwargs)

    def on_touch_up(self, touch):
        if self.click_handler and self.collide_point(*touch.pos):
            self.click_handler(self)


class GenerationsView(Widget):

    stack = ObjectProperty(None)
    generation_selected_handler = None
    selected_generation_idx = None
    entries = []

    def __init__(self, **kwargs):
        if "generation_selected_handler" in kwargs:
            self.generation_selected_handler = kwargs.pop("generation_selected_handler")
        super().__init__(**kwargs)

    def update(self, state: AppState):
        self.entries = [
            GenerationsEntryView(
                generation_id=i,
                min_fitness=g.min_fitness,
                max_fitness=g.max_fitness,
                click_handler=lambda _, i=i: self.on_generation_selected(i)
            ) for i, g in enumerate(state.generations)
        ]

        self.stack.clear_widgets()
        for entry in self.entries:
            self.stack.add_widget(entry)

    def on_generation_selected(self, generation_id: int):
        if self.generation_selected_handler:
            self.generation_selected_handler(generation_id)
