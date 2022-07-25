import numpy as np
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.graphics.texture import Texture
from kivy.uix.widget import Widget

RES_W = 256
RES_H = 240
CROP_LEFT = 88
CROP_RIGHT = 72
CROP_BOTTOM = 25
CROP_TOP = 15
FPS = 25.


class TetrisView(Widget):
    def __init__(self, **kwargs):
        self.get_video_func = None
        if "get_video_func" in kwargs:
            self.get_video_func = kwargs.pop("get_video_func")

        super().__init__(**kwargs)

        self.viewport_size = (RES_W - CROP_LEFT - CROP_RIGHT, RES_H - CROP_TOP - CROP_BOTTOM)
        self.texture = Texture.create(size=self.viewport_size)
        self.event = Clock.schedule_interval(self.render, 1 / FPS)

        with self.canvas:
            Color(rgb=(1, 1, 1))
            self.rect = Rectangle(texture=self.texture, pos=(0, 0), size=(100, 100))
        self.bind(pos=self.layout, size=self.layout)

    def layout(self, *args):
        width = self.height / self.viewport_size[1] * self.viewport_size[0]

        self.rect.size = (width, self.height)
        self.rect.pos = (0, self.y)

    def render(self, dt):
        if self.get_video_func is None:
            raise TypeError("get_video_func not set for TetrisView")

        data = self.get_video_func()
        data = data[CROP_TOP:-CROP_BOTTOM, CROP_LEFT:-CROP_RIGHT]
        buf = np.flipud(data).reshape(1, self.viewport_size[0] * self.viewport_size[1] * 3).squeeze()
        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.canvas.ask_update()
