from enum import Enum
from typing import Callable, Dict, Optional

from environment import TetrisEnv, Observation
from moves import Move


class ButtonAction(Enum):
    NOTHING = int("00000000", 2),
    RIGHT = int("10000000", 2),
    LEFT = int("01000000", 2),
    DOWN = int("00100000", 2),
    UP = int("00010000", 2),
    START = int("00001000", 2),
    SELECT = int("00000100", 2),
    B = int("00000010", 2),
    A = int("00000001", 2)


class Controller:
    def __init__(self, env: TetrisEnv, get_move_func: Callable[[Observation, Dict], Move]):
        self.last_stone_index = -1
        self.env = env
        self.get_move_func = get_move_func
        self.move: Optional[Move] = None
        self.next_action = ButtonAction.NOTHING

    def action(self):
        observation_data, reward, done, info = self.env.step(self.next_action.value)
        if self.last_stone_index < info["stone_index"]:
            self.last_stone_index = info["stone_index"]
            print("next move")
            self.move = self.get_move_func(observation_data, info)

        if info["stone_id"] != self.move.stone_id:
            self.next_action = ButtonAction.A
        elif info["stone_x"] > self.move.stone_x:
            self.next_action =  ButtonAction.LEFT
        elif info["stone_x"] < self.move.stone_x:
            self.next_action = ButtonAction.RIGHT
        else:
            self.next_action = ButtonAction.NOTHING
