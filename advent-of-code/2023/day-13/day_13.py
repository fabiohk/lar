from enum import StrEnum


class Space(StrEnum):
    ASH = "."
    ROCK = "#"
    EMPTY_SPACE = "-"

DEBUG_HORIZONTAL = False
DEBUG_VERTICAL = False
DEBUG = DEBUG_HORIZONTAL or DEBUG_VERTICAL

def print_debug(str):
    if DEBUG:
        print(str)

def print_map_debug(map):
    if DEBUG:
        print_map(map)

def print_map(map: list[list[Space]]):
    for line in map:
        for c in line:
            print(c, end="")
        print()
    print("-----")

# returns the number of columns to the left of where the reflection occurs, otherwise returns 0
def has_vertical_reflection(map: list[list[Space]], reflection_to_disconsider: int, /, print_reflection: bool = False) -> int:
    map_list = [list(row) for row in map]
    rotated_map = rotate_clowise(map_list)
    if print_reflection:
        print_map(rotated_map)
    return has_horizontal_reflection(list(list(row) for row in rotated_map), reflection_to_disconsider)

def rotate_clowise(map: list[list[Space]]) -> list[list[Space]]:
    n, m = len(map), len(map[0])
    new_map = empty_space(m, n)

    for j in range(m):
        for i in range(n):
            new_map[j][i] = map[n-i-1][j]

    return new_map

def empty_space(n: int, m: int) -> list[list[Space]]:
    map: list[list[Space]] = []

    for i in range(n):
        map.append([])
        for _ in range(m):
            map[i].append(Space.EMPTY_SPACE)

    return map

# returns the number of rows above where the reflection occurs, otherwise returns 0
def has_horizontal_reflection(map: list[list[Space]], reflection_to_disconsider: int) -> int:
    if len(map) % 2 == 0:
        number_of_rows = loop_through_inside(map)
        if number_of_rows > 0 and number_of_rows != reflection_to_disconsider:
            return number_of_rows
        number_of_rows = loop_skipping_first(map[2:], 2)
        if number_of_rows > 0 and number_of_rows != reflection_to_disconsider:
            return number_of_rows
        number_of_rows = loop_skipping_last(map[:-2])
        return number_of_rows if number_of_rows != reflection_to_disconsider else 0
    number_of_rows = loop_skipping_first(map[1:], 1)
    if number_of_rows > 0 and number_of_rows != reflection_to_disconsider:
        return number_of_rows
    number_of_rows = loop_skipping_last(map[:-1])
    return number_of_rows if number_of_rows != reflection_to_disconsider else 0
    

def loop_through_inside(map: list[list[Space]]) -> int:
    print_debug("LOOP THROUGH INSIDE")
    number_of_rows = 0
    map_in_question = map[:]
    while len(map_in_question) > 2:
        print_map_debug(map_in_question)
        if are_lines_equal(map_in_question[0], map_in_question[-1]):
            print_debug("EQUAL")
            map_in_question = map_in_question[1:-1]
            number_of_rows += 1
        else:
            break

    print_map_debug(map_in_question)
    if len(map_in_question) > 2:
        return 0
    return number_of_rows + 1 if are_lines_equal(map_in_question[0], map_in_question[-1]) else 0

def loop_skipping_first(map: list[list[Space]], skip_length: int) -> int:
    print_debug("LOOP SKIPPING FIRST")
    print_map_debug(map)
    if len(map) == 0:
        return 0

    number_of_rows = loop_through_inside(map)
    if number_of_rows > 0:
        return number_of_rows + skip_length
    number_of_rows = loop_skipping_first(map[2:], 2)
    return number_of_rows + skip_length if number_of_rows > 0 else 0

def loop_skipping_last(map: list[list[Space]]) -> int:
    if len(map) == 0:
        return 0

    number_of_rows = loop_through_inside(map)
    if number_of_rows > 0:
        return number_of_rows
    number_of_rows = loop_skipping_last(map[:-2])
    return number_of_rows



def are_lines_equal(line_a: list[Space], line_b: list[Space]) -> bool:
    print_debug("".join(line_a))
    print_debug("".join(line_b))
    return all(space_start == space_end for space_start, space_end in zip(line_a, line_b))


def read_input(input_path: str) -> list[list[list[Space]]]:
    patterns = []
    new_pattern = []

    with open(input_path) as f:
        for line in f.readlines():
            if Space.ASH not in line and Space.ROCK not in line:
                patterns.append(list(new_pattern))
                new_pattern = []
                continue
            new_pattern.append(parse_line(line))

        patterns.append(list(new_pattern))
        return patterns
    
def parse_line(line: str) -> list[Space]:
    return [c for c in line.strip()]


def summarize_notes(patterns: list[list[list[Space]]]) -> int:
    number_of_columns_with_vertical_reflection = [has_vertical_reflection(pattern, 0) for pattern in patterns] if not DEBUG_HORIZONTAL else [0]
    number_of_rows_with_horizontal_reflection = [has_horizontal_reflection(pattern, 0) for pattern in patterns] if not DEBUG_VERTICAL else [0]

    print_debug(number_of_columns_with_vertical_reflection)
    print_debug(number_of_rows_with_horizontal_reflection)
    for i, zipped in enumerate(zip(number_of_columns_with_vertical_reflection, number_of_rows_with_horizontal_reflection)):
        if zipped[0] == 0 and zipped[1] == 0:
            print_debug(i)
    return sum(number_of_columns_with_vertical_reflection) + sum(number_of_rows_with_horizontal_reflection) * 100


def find_new_reflection_smudging_space(pattern: list[list[Space]]) -> list[tuple[int, int]]:
    possible_results = []

    columns_with_vertical_reflection = has_vertical_reflection(pattern, 0)
    rows_with_horizontal_reflection = has_horizontal_reflection(pattern, 0)

    n, m = len(pattern), len(pattern[0])
    for i in range(n):
        for j in range(m):
            old_pattern = pattern[i][j]
            pattern[i][j] = Space.ASH if old_pattern == Space.ROCK else Space.ROCK
            columns_with_vertical_reflection_for_new_pattern = has_vertical_reflection(pattern, columns_with_vertical_reflection)
            rows_with_horizontal_reflection_for_new_pattern = has_horizontal_reflection(pattern, rows_with_horizontal_reflection)
            if columns_with_vertical_reflection_for_new_pattern != columns_with_vertical_reflection or rows_with_horizontal_reflection_for_new_pattern != rows_with_horizontal_reflection:
                if 0 <= i < rows_with_horizontal_reflection_for_new_pattern * 2 or 0 <= j < columns_with_vertical_reflection_for_new_pattern * 2:
                    if columns_with_vertical_reflection_for_new_pattern > 0 or rows_with_horizontal_reflection_for_new_pattern > 0:
                        possible_results.append((columns_with_vertical_reflection_for_new_pattern, rows_with_horizontal_reflection_for_new_pattern))
            pattern[i][j] = old_pattern
    
    if not possible_results:
        return [(0, 0)]
        
    final_results = []
    for columns, rows in possible_results:
        final_column = 0 if columns == columns_with_vertical_reflection else columns
        final_row = 0 if rows == rows_with_horizontal_reflection else rows
        final_results.append((final_column, final_row))
    return final_results

def summarize_notes_smudging_space(patterns: list[list[Space]]) -> int:
    number_of_columns_with_vertical_reflection = 0
    number_of_rows_with_horizontal_reflection = 0

    for pattern in patterns:
        possible_results = find_new_reflection_smudging_space(pattern)
        columns, rows = possible_results[0]
        number_of_columns_with_vertical_reflection += columns
        number_of_rows_with_horizontal_reflection += rows

    return number_of_columns_with_vertical_reflection + number_of_rows_with_horizontal_reflection * 100

patterns = read_input("./example")
print(summarize_notes(patterns))
print(summarize_notes_smudging_space(patterns))

if not DEBUG:
    patterns = read_input("./input")
    print(summarize_notes(patterns))
    print(summarize_notes_smudging_space(patterns))