from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

from moves import Field, Stone, Evaluation
from moves.evaluate import evaluate_field, evaluate_height, col_heights
from moves.field import FIELD_ROWS, FIELD_COLS
from moves.stone import STONE_SIZE


class StoneOutOfFieldError(Exception):
    pass


class StonesInterceptionError(Exception):
    pass


def can_insert_stone(field: Field, stone: Stone, x: int, y: int) -> bool:
    for stone_x in range(STONE_SIZE):
        for stone_y in range(stone.get_height(), STONE_SIZE):
            field_x = x + stone_x
            field_y = y + stone_y
            if not field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                raise StoneOutOfFieldError("Stone is outside of field")

            if field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                if field.get(field_x, field_y) > 0:
                    raise StonesInterceptionError("Stone is intercepting with already dropped stones")
    return True


def insert_stone(field: Field, stone: Stone, x: int, y: int) -> Field:
    set_coordinates = []
    for stone_x in range(STONE_SIZE):
        for stone_y in range(STONE_SIZE):
            field_x = x + stone_x
            field_y = y + stone_y
            if not field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                for x, y in set_coordinates:
                    field.set(x, y, 0)
                raise StoneOutOfFieldError("Stone is outside of field")

            if field.contains(field_x, field_y) and stone.get(stone_x, stone_y) > 0:
                if field.get(field_x, field_y) > 0:
                    for x, y in set_coordinates:
                        field.set(x, y, 0)
                    raise StonesInterceptionError("Stone is intercepting with already dropped stones")

                set_coordinates.append((field_x, field_y))
                field.set(field_x, field_y, stone.get(stone_x, stone_y))

    return field


def place_stone(field: Field, stone: Stone, col: int, field_height: int) -> Tuple[int, int, Field]:
    stone_offset = stone.get_height()-STONE_SIZE
    for y in range(FIELD_ROWS-field_height+stone_offset-1, FIELD_ROWS-STONE_SIZE+1):
        try:
            can_insert_stone(field, stone, col, y)
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
    field_height = evaluate_height(col_heights(field))
    for _ in range(stone.num_rotations()):
        for col in range(-2, FIELD_COLS-2):
            try:
                x, y, resulting_field = place_stone(deepcopy(field), stone, col, field_height)
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


def evaluate_all_possible_moves_including_next_stone(field: Field, stone: Stone, next_stone: Stone) -> List[Move]:
    moves = []
    first_moves = evaluate_all_possible_moves(field, stone)
    for first_move in first_moves:
        second_moves = evaluate_all_possible_moves(first_move.evaluation.field, next_stone)
        for second_move in second_moves:
            moves.append(Move(
                evaluation=second_move.evaluation,
                stone_x=first_move.stone_x,
                stone_y=first_move.stone_y,
                stone_id=first_move.stone_id
            ))
    return moves
