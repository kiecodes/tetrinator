from typing import Callable, Dict, Optional

from controller.button_action import ButtonAction
from environment import TetrisEnv, Observation
from moves import Move


class BaseController:
    def __init__(self, env: TetrisEnv, get_move_func: Callable[[Observation, Dict], Move]):
        self.last_stone_index = -1
        self.env = env
        self.get_move_func = get_move_func
        self.move: Optional[Move] = None
        self.next_action = ButtonAction.NOTHING
        self.score = 0

    def action(self) -> bool:
        observation_data, reward, done, info = self.env.step(self.next_action.value)
        self.score = info["score"]
        if done:
            return False

        if not info["is_animating"] and self.last_stone_index != info["stone_index"]:
            self.last_stone_index = info["stone_index"]
            self._on_new_stone()
        else:
            # if there is currently no move present, do nothing
            if self.move is None:
                self.next_action = ButtonAction.NOTHING
            else:
                target_x = self.move.stone_x + 2
                # Release Button after rotation for one frame
                if self.next_action == ButtonAction.B or info["is_animating"]:
                    self.next_action = ButtonAction.NOTHING
                elif info['stone_id'] != self.move.stone_id:
                    self.next_action = ButtonAction.B
                elif info["stone_x"] > target_x:
                    self.next_action = ButtonAction.LEFT
                elif info["stone_x"] < target_x:
                    self.next_action = ButtonAction.RIGHT
                else:
                    self.next_action = ButtonAction.DOWN

        return True

    def _on_new_stone(self):
        # Needs to be implemented in subclass
        pass
