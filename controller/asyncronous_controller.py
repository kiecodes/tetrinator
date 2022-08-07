from threading import Thread
from typing import Callable, Dict

from controller.base_controller import BaseController
from environment import TetrisEnv, Observation
from moves import Move


class AsynchronousController(BaseController):
    def __init__(self, env: TetrisEnv, get_move_func: Callable[[Observation, Dict], Move]):
        super().__init__(env, get_move_func)
        self.evaluate_thread = None

    def _on_new_stone(self):
        observation_data, reward, done, info = self.env.step(self.next_action.value)
        self.evaluate_thread = Thread(
            target=self._evaluate,
            args=(observation_data, info),
            name=f"Evaluation for {self}"
        )
        self.evaluate_thread.start()

    def _evaluate(self, observation_data, info):
        self.move = None
        self.move = self.get_move_func(observation_data, info)
