import random
import time
from concurrent.futures.thread import ThreadPoolExecutor
from functools import partial
from threading import Thread
from typing import List

import gym
import numpy as np

import environment.tetris
import genetic.genetic
from controller import AsynchronousController, SynchronousController
from model import AppState
from moves import Field, Stone, evaluate_all_possible_moves
from moves.moves import evaluate_all_possible_moves_including_next_stone
from ui.app import Tetrinator
from worker import Worker

POPULATION_SIZE = 8

environment.tetris.register()
video_data = np.zeros((240, 256, 3), dtype=np.uint8)

app_state = AppState()
app_state.add_generation(10, 100)


def choose_best_move(observation, stone_id, next_stone_id=None):
    field = Field(data=observation.tolist())

    if next_stone_id is None:
        moves = evaluate_all_possible_moves(field, Stone(stone_id))
    else:
        moves = evaluate_all_possible_moves_including_next_stone(field, Stone(stone_id), Stone(next_stone_id))

    rankings = [-2 * m.evaluation.holes - m.evaluation.bump_ratio + 2 * m.evaluation.lines_cleared for
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


def choose_best_move_for_genome(genome: List[float], observation, stone_id, next_stone_id=None):
    field = Field(data=observation.tolist())

    if next_stone_id is None:
        moves = evaluate_all_possible_moves(field, Stone(stone_id))
    else:
        moves = evaluate_all_possible_moves_including_next_stone(field, Stone(stone_id), Stone(next_stone_id))

    if len(moves) > 0:
        rankings = [
            genome[0] * m.evaluation.holes +
            genome[1] * m.evaluation.lines_cleared +
            genome[2] * m.evaluation.height +
            genome[2] * m.evaluation.bump_ratio +
            genome[3] * m.evaluation.bumps +
            genome[5] * m.evaluation.bumpiness
            for m in moves]
        best_index = max(range(len(rankings)), key=rankings.__getitem__)
        return moves[best_index]
    else:
        return None

fitness_cache = {}


def genome_fitness(genome: List[float], worker: Worker) -> int:
    global fitness_cache
    if str(genome) in fitness_cache:
        return fitness_cache[str(genome)]

    idx, env = worker.acquire()

    controller = SynchronousController(
        env=env,
        get_move_func=lambda observation, info: choose_best_move_for_genome(genome, observation, info['stone_id'])
    )

    env.reset()
    done = False
    while not done:
        done = not controller.action()

    worker.release(idx)

    fitness_cache[str(genome)] = controller.score
    return controller.score


def fitness(population: genetic.Population, worker: Worker) -> List[int]:
    with ThreadPoolExecutor(max_workers=worker.count) as executor:
        fitness_data = list(executor.map(
            lambda g: genome_fitness(g, worker),
            population
        ))
    return fitness_data


def mutate(genome: List[float], num: int = 1, probability: float = 0.5, spread: float = 0.5) -> List[float]:
    for _ in range(num):
        index = random.randrange(len(genome))
        if random.random() > probability:
            genome[index] = genome[index] + random.uniform(-spread, spread)

    return genome


def print_evolution_status(generation: int, population: genetic.RatedPopulation):
    max_fitness = population[0][1]
    min_fitness = population[len(population) - 1][1]
    print(f"[{generation}] max fitness: {max_fitness}\tmin fitness: {min_fitness}")


def evolution(app: Tetrinator, worker: Worker):
    print("Starting evolution")
    genetic.run_evolution(
        populate_func=lambda: [[random.uniform(-2, 2) for _ in range(6)] for _ in range(POPULATION_SIZE)],
        fitness_func=partial(fitness, worker=worker),
        fitness_limit=50000,
        selection_func=genetic.selection_pair,
        crossover_func=genetic.single_point_crossover,
        mutation_func=mutate,
        status_func=print_evolution_status
    )
    print("Evolution DONE")


if __name__ == '__main__':
    worker = Worker(
        num_worker=16,
        creation_func=lambda: gym.make('Tetris-v1', level=5, starting_piece=None)
    )

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

    t = Thread(target=evolution, args=(app, worker), name="Evolution")
    t.start()

    app.update(app_state)

    app.run()
