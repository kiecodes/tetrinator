import random
from enum import Enum

import numpy as np
from gym.spaces import Box
from nes_py import NESEnv
import gym
from numpy import uint8, ndarray

OBSERVATION_SPACE_ROWS = 20
OBSERVATION_SPACE_COLS = 10


Observation = ndarray


class StoneType(Enum):
    T = 0
    L = 1
    J = 2
    S = 3
    Z = 4
    BLOCK = 5
    I = 6


class TetrisEnv(NESEnv):
    observation_space = Box(
        low=0,
        high=5,
        shape=(OBSERVATION_SPACE_ROWS, OBSERVATION_SPACE_COLS),
        dtype=np.uint8
    )

    def __init__(self, level, starting_piece):
        super().__init__('environment/tetris-ntsc.nes')
        self.starting_speed_level = level

        self._starting_block_waiting_time = None
        if starting_piece is not None:
            self.set_starting_piece(starting_piece)

    # The initial block is determined by how many frames pass
    # when we select the level. At least that's what I found
    # most likely there is another way to set the initial seed
    # for the game
    def set_starting_piece(self, stone_type):
        waiting_time_per_stone_type = {
            StoneType.T: 0,
            StoneType.Z: 1,
            StoneType.S: 3,
            StoneType.J: 7,
            StoneType.BLOCK: 8,
            StoneType.I: 10,
            StoneType.L: 12,
        }
        self._starting_block_waiting_time = waiting_time_per_stone_type[stone_type]

    def _did_reset(self):
        self._skip_start_screens()

    def reset(self, seed=None, options=None, return_info=None):
        super().reset(seed, options, return_info)
        return self._get_observation()

    def step(self, action):
        _, reward, done, info = super().step(action)
        return self._get_observation(), reward, done, {
            "stone_x": self.stone_x,
            "stone_y": self.stone_y,
            "stone_id": self.stone_id,
            "next_stone_id": self.next_stone_id,
            "stone_index": self.num_stones
        }

    def _did_step(self, done):
        # print("\t".join(map(str, list(self.ram))))
        if done:
            return

    def _get_done(self):
        return self.is_game_over

    def _skip_start_screens(self):
        self.ram[0x00A8] = 0x00
        while self.ram[0x00A8] == 0:
            self._frame_advance(0)
        self.ram[0x00A8] = 0x00
        self._frame_advance(0)
        self._frame_advance(8)
        self._frame_advance(0)
        while self.ram[5] == 108:
            self._frame_advance(0)

        while self.ram[5] == 113:
            self._frame_advance(8)
            self._frame_advance(0)

        while self.ram[5] == 234:
            self._frame_advance(8)
            self._frame_advance(0)

        self.ram[0x67] = self.starting_speed_level
        self._frame_advance(0)

        if self._starting_block_waiting_time is not None:
            skip_frames_for_starting_block = self._starting_block_waiting_time
        else:
            skip_frames_for_starting_block = random.randint(0, 20)

        for _ in range(skip_frames_for_starting_block):
            self._frame_advance(0)

        while self.ram[5] == 253:
            self._frame_advance(8)
            self._frame_advance(0)

        while self.ram[26] == 0:
            self._frame_advance(0)
        return

    @property
    def stone_x(self):
        return self.ram[0x60]

    @stone_x.setter
    def stone_x(self, value):
        self.ram[0x60] = value

    @property
    def stone_y(self):
        return self.ram[0x61]

    @stone_y.setter
    def stone_y(self, value):
        self.ram[0x61] = value

    @property
    def stone_id(self):
        return self.ram[0x62]

    @stone_id.setter
    def stone_id(self, value):
        self.ram[0x62] = value

    @property
    def next_stone_id(self):
        return self.ram[191]

    @next_stone_id.setter
    def next_stone_id(self, value):
        self.ram[191] = value

    @property
    def num_stones(self):
        return self.ram[0x1A]-2

    @property
    def num_clearing_lines(self):
        return self.ram[0x56]

    @property
    def num_cleared_lines(self):
        return int.from_bytes(b''.join(self.ram[0x50:0x52]), byteorder="little")

    @property
    def score(self):
        return int.from_bytes(b''.join(self.ram[0x53:0x56]), byteorder="little")

    @property
    def is_game_over(self):
        return self.ram[0x58] != 0

    def _get_observation(self):
        offset = 1024

        lines = []

        for line in range(OBSERVATION_SPACE_ROWS):
            start = offset + line * OBSERVATION_SPACE_COLS
            lines.append([0 if i == 239 else 1 for i in self.ram[start:start + OBSERVATION_SPACE_COLS]])

        return np.array(lines, dtype=uint8)


def register():
    gym.envs.registration.register(
        id='Tetris-v1',
        entry_point='environment.tetris:TetrisEnv'
    )
