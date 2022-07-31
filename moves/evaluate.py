from dataclasses import dataclass

from moves import Field
from moves.field import FIELD_COLS, FIELD_ROWS


def _col_height(field: Field, col) -> int:
    height = 0
    for row in range(FIELD_ROWS):
        if field.get(col, FIELD_ROWS-row-1) > 0:
            height = row+1
    return height


def evaluate_height(field: Field) -> int:
    height = 0
    for x in range(FIELD_COLS):
        col_height = _col_height(field, x)
        if height < col_height:
            height = col_height

    return height


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


def evaluate_bumpiness(field: Field) -> int:
    heights = [_col_height(field, x) for x in range(FIELD_COLS)]
    bumps = [abs(a-b) for a, b in zip(heights[:-1], heights[1:])]
    return sum(bumps)


def evaluate_bumps(field: Field) -> int:
    heights = [_col_height(field, x) for x in range(FIELD_COLS)]
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


def evaluate_field(field: Field) -> Evaluation:
    bumpiness = evaluate_bumpiness(field)
    bumps = evaluate_bumps(field)

    return Evaluation(
        height=evaluate_height(field),
        lines_cleared=evaluate_lines_cleared(field),
        holes=evaluate_holes(field),
        bumpiness=evaluate_bumpiness(field),
        bumps=evaluate_bumps(field),
        bump_ratio=bumpiness/(FIELD_COLS-bumps)
    )
