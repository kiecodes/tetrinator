from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

from moves import Field, Stone, Evaluation
from moves.evaluate import evaluate_field
from moves.field import FIELD_ROWS, FIELD_COLS
from moves.stone import STONE_SIZE


class StoneOutOfFieldError(Exception):
    pass


class StonesInterceptionError(Exception):
    pass


def insert_stone(field: Field, stone: Stone, x: int, y: int) -> Field:
    field_copy = deepcopy(field)
    for stone_x in range(STONE_SIZE):
        for stone_y in range(STONE_SIZE):
            field_x = x + stone_x
            field_y = y + stone_y
            if not field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                raise StoneOutOfFieldError("Stone is outside of field")

            if field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                if field.get(field_x, field_y) > 0:
                    raise StonesInterceptionError("Stone is intercepting with already dropped stones")

                field_copy.set(field_x, field_y, stone.get(stone_x, stone_y))

    return field_copy


def place_stone(field: Field, stone: Stone, col: int) -> Tuple[int, int, Field]:
    stone_offset = stone.get_height()-STONE_SIZE
    for y in range(stone_offset, FIELD_ROWS-STONE_SIZE+1):
        try:
            insert_stone(field, stone, col, y)
        except StonesInterceptionError:
            return col, y-1, insert_stone(field, stone, col, y-1)

    return col, FIELD_ROWS-STONE_SIZE, insert_stone(field, stone, col, FIELD_ROWS-STONE_SIZE)


@dataclass
class Move:
    evaluation: Evaluation
    stone_x: int
    stone_y: int
    stone_id: int


def evaluate_all_possible_moves(field: Field, stone: Stone) -> List[Move]:
    moves = []
    for _ in range(stone.num_rotations()):
        for col in range(-2, FIELD_COLS-2):
            try:
                x, y, resulting_field = place_stone(field, stone, col)
                evaluation = evaluate_field(resulting_field)
                moves.append(Move(
                    evaluation=evaluation,
                    stone_x=x,
                    stone_y=y,
                    stone_id=stone.stone_id
                ))
            except StoneOutOfFieldError:
                pass
            except StonesInterceptionError:
                pass
        stone.rotate()
    return moves
