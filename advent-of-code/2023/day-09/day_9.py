def next_value(history: list[int]) -> int:
    sequences = [history]
    current_history = history.copy()
    any_step_is_not_zero = True

    while any_step_is_not_zero:
        steps = [b-a for a, b in zip(current_history, current_history[1:])]
        any_step_is_not_zero = any(step != 0 for step in steps)
        sequences.append(steps)
        current_history = steps.copy()

    next_value_from_sequence = 0
    for sequence in sequences[-2::-1]:
        sequence.append(next_value_from_sequence + sequence[-1])
        next_value_from_sequence = sequence[-1]

    return next_value_from_sequence

def read_input() -> list[list[int]]:
    with open("./input") as f:
        return [parse_line(line) for line in f.readlines()]
    
def parse_line(line: str) -> list[int]:
    return [int(number) for number in line.strip().split(" ")]

def previous_value(history: list[int]) -> int:
    sequences = [history]
    current_history = history.copy()
    any_step_is_not_zero = True

    while any_step_is_not_zero:
        steps = [b-a for a, b in zip(current_history, current_history[1:])]
        any_step_is_not_zero = any(step != 0 for step in steps)
        sequences.append(steps)
        current_history = steps.copy()

    next_value_from_sequence = 0
    for sequence in sequences[-2::-1]:
        sequence.append(sequence[0] - next_value_from_sequence)
        next_value_from_sequence = sequence[-1]

    return next_value_from_sequence

histories = read_input()
next_values = [next_value(history) for history in histories]
print(sum(next_values))

previous_values = [previous_value(history) for history in histories]
print(sum(previous_values))