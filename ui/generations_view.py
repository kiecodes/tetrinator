from kivy.lang import Builder
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget

from ui.model import AppState, Generation

Builder.load_file('ui/generations_view.kv')


class GenerationsEntryView(Widget):
    generation_id = NumericProperty()
    selected = BooleanProperty(False)
    generation = ObjectProperty()

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

    def update(self, state: AppState):
        self.generation_selected_handler = state.on_generation_selected
        self.entries = [
            GenerationsEntryView(
                generation_id=i,
                selected=i == self.selected_generation_idx,
                generation=g,
                click_handler=lambda _, i=i: self.on_generation_selected(i, g)
            ) for i, g in enumerate(state.generations)
        ]

        self.stack.clear_widgets()
        for entry in self.entries:
            self.stack.add_widget(entry)

    def on_generation_selected(self, index: int, generation: Generation):
        if self.selected_generation_idx is not None:
            self.entries[self.selected_generation_idx].selected = False

        self.entries[index].selected = True
        self.selected_generation_idx = index

        if self.generation_selected_handler:
            self.generation_selected_handler(generation)
