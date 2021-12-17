from math import sqrt, ceil, floor


def solution(a, b):
    """
    a - x axis
    b - y axis

    1. Start with a rectangle with lines parallel with x and y axis which the diagonals crossing the (0, 0) point.
    2. Rotate it -45 degrees (315 degrees)
    3. Pick the maximum and minimum values for each axis
    4. Loop through all possible integer combinations between those max and min values
    5. To verify that a point is inside the rectangle, we can rotate the point 45 degree and verify if it's inside the
    original rectangle (the rectangle with lines parallel to the x, y axis)
    """
    max_x = a // 2
    min_x = -max_x
    max_y = b // 2
    min_y = -max_y

    combinations = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]

    rotated_combinations = [rotate_315_degrees(x, y) for x, y in combinations]

    max_possible_x = ceil(max(x for x, _ in rotated_combinations))
    min_possible_x = floor(min(x for x, _ in rotated_combinations))
    max_possible_y = ceil(max(y for _, y in rotated_combinations))
    min_possible_y = floor(min(y for _, y in rotated_combinations))

    integer_points_in_rectangle = 0
    for x in range(min_possible_x, max_possible_x + 1):
        for y in range(min_possible_y, max_possible_y + 1):
            if is_inside_rectangle(x, y, min_x, max_x, min_y, max_y):
                integer_points_in_rectangle += 1

    return integer_points_in_rectangle


def rotate_315_degrees(x, y):
    """
    x' = xcos(315)-ysin(315) = (x+y)/sqrt(2)
    y' = xsin(315)+ycos(315) = (y-x)/sqrt(2)
    """
    return (x + y) / sqrt(2), (y - x) / sqrt(2)


def is_inside_rectangle(x, y, min_x, max_x, min_y, max_y):
    rotated_x, rotated_y = rotate_45_degrees(x, y)
    return min_x < rotated_x < max_x and min_y < rotated_y < max_y


def rotate_45_degrees(x, y):
    """
    x' = xcos(45)-ysin(45) = (x-y)/sqrt(2)
    y' = xsin(45)+ycos(45) = (x+y)/sqrt(2)
    """
    return (x - y) / sqrt(2), (x + y) / sqrt(2)
