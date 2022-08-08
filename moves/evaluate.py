from dataclasses import dataclass
from typing import Optional, List

from moves import Field
from moves.field import FIELD_COLS, FIELD_ROWS


def _col_height(field: Field, col) -> int:
    height = 0
    for row in range(FIELD_ROWS):
        if field.get(col, FIELD_ROWS-row-1) > 0:
            height = row+1
    return height


def col_heights(field: Field) -> List[int]:
    return [_col_height(field, x) for x in range(FIELD_COLS)]


def evaluate_height(heights) -> int:
    return max(heights)


def evaluate_lines_cleared(field: Field) -> int:
    num_cleared = 0
    for y in range(FIELD_ROWS):
        if all(field.get_row(y)):
            num_cleared = num_cleared+1
    return num_cleared


def evaluate_holes(field: Field) -> int:
    num_holes = 0
    for x in range(FIELD_COLS):
        hole = False
        for y in range(FIELD_ROWS-1, -1, -1):
            if field.get(x, y) == 0:
                hole = True
            else:
                if hole:
                    num_holes = num_holes+1
                    hole = False

    return num_holes


def evaluate_bumpiness(heights) -> int:
    bumps = [abs(a-b) for a, b in zip(heights[:-1], heights[1:])]
    return sum(bumps)


def evaluate_bumps(heights) -> int:
    bumps = [a != b for a, b in zip(heights[:-1], heights[1:])]
    return sum(bumps)


@dataclass
class Evaluation:
    height: int
    lines_cleared: int
    holes: int
    bumpiness: int
    bumps: int
    bump_ratio: float
    field: Field


def evaluate_field(field: Field) -> Evaluation:
    heights = col_heights(field)
    bumpiness = evaluate_bumpiness(heights)
    bumps = evaluate_bumps(heights)

    return Evaluation(
        height=evaluate_height(heights),
        lines_cleared=evaluate_lines_cleared(field),
        holes=evaluate_holes(field),
        bumpiness=bumpiness,
        bumps=bumps,
        bump_ratio=bumpiness/(FIELD_COLS-bumps),
        field=field
    )
