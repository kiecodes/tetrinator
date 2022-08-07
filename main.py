import time
from threading import Thread

import gym
import numpy as np

import environment.tetris
from controller import AsynchronousController
from model import AppState
from moves import Field, Stone, evaluate_all_possible_moves
from moves.moves import evaluate_all_possible_moves_including_next_stone
from ui.app import Tetrinator

environment.tetris.register()
video_data = np.zeros((240, 256, 3), dtype=np.uint8)

app_state = AppState()
app_state.add_generation(10, 100)
app_state.add_generation(13, 102)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)
app_state.add_generation(14, 110)


def choose_best_move(observation, stone_id, next_stone_id=None):
    field = Field(data=observation.tolist())

    if next_stone_id is None:
        moves = evaluate_all_possible_moves(field, Stone(stone_id))
    else:
        moves = evaluate_all_possible_moves_including_next_stone(field, Stone(stone_id), Stone(next_stone_id))

    rankings = [-2*m.evaluation.holes - m.evaluation.bump_ratio + 2 * m.evaluation.lines_cleared for
                m in moves]
    best_index = max(range(len(rankings)), key=rankings.__getitem__)

    return moves[best_index]


def play(env):
    global video_data
    frame_length = 1 / 60.1
    env.reset()

    done = False

    controller = AsynchronousController(
        env=env,
        get_move_func=lambda observation, info: choose_best_move(observation, info["stone_id"], info["next_stone_id"])
    )
    while not done:
        start = time.time()
        video_data = env.render(mode="rgb_array")
        if controller.action():
            end = time.time()
            time.sleep(max(0.0, frame_length - (end - start)))
        else:
            env.reset()
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

    app.update(app_state)

    app.run()
