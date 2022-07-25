import time
from threading import Thread

import gym
import numpy as np

import environment.tetris
from ui.app import Tetrinator

environment.tetris.register()
video_data = np.zeros((240, 256, 3), dtype=np.uint8)


def play(env):
    global video_data
    frame_length = 1 / 60.1
    env.reset()

    done = False
    while not done:
        start = time.time()
        video_data = env.render(mode="rgb_array")
        observation_data, reward, done, info = env.step(0)
        end = time.time()
        time.sleep(max(0.0, frame_length - (end - start)))
    exit(0)


if __name__ == '__main__':

    print(f"Starting game")
    env = gym.make('Tetris-v1', level=5, starting_piece=None)

    app = Tetrinator()
    app.training_view.tetris_view.get_video_func = lambda: video_data

    play_thread = Thread(
        target=play,
        args=(env,),
        name="Playback"
    )
    play_thread.start()

    app.run()
