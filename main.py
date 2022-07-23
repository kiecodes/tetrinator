import gym
from nes_py.app.play_human import play_human
import environment.tetris

environment.tetris.register()

env = gym.make('Tetris-v1', level=5)

play_human(env)
