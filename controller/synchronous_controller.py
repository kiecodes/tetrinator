from controller.base_controller import BaseController
from controller.button_action import ButtonAction


class SynchronousController(BaseController):

    def _on_new_stone(self):
        observation_data, reward, done, info = self.env.step(self.next_action.value)
        self.move = self.get_move_func(observation_data, info)
        self.next_action = ButtonAction.NOTHING  # release button at for one frame
