from copy import deepcopy
from typing import List

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


def place_stone(field: Field, stone: Stone, col: int) -> Field:
    stone_offset = stone.get_height()-STONE_SIZE
    for y in range(stone_offset, FIELD_ROWS-STONE_SIZE+1):
        try:
            insert_stone(field, stone, col, y)
        except StonesInterceptionError:
            return insert_stone(field, stone, col, y-1)

    return insert_stone(field, stone, col, FIELD_ROWS-STONE_SIZE)


def evaluate_all_possible_moves(field: Field, stone: Stone) -> List[Evaluation]:
    evaluations = []
    for _ in range(stone.num_rotations()):
        for col in range(-2, FIELD_COLS-2):
            try:
                evaluations.append(
                    evaluate_field(
                        place_stone(field, stone, col)
                    )
                )
            except StoneOutOfFieldError:
                pass
    return evaluations
