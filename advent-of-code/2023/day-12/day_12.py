from dataclasses import dataclass
from enum import StrEnum


class SpringCondition(StrEnum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"

type ConditionRecord = str

@dataclass
class ConditionRecords:
    condition_record: ConditionRecord
    valid_group: list[int]


def find_all_possibilities(condition_record: ConditionRecord) -> list[ConditionRecord]:
    if condition_record[0] == SpringCondition.UNKNOWN:
        possibilities = [SpringCondition.OPERATIONAL, SpringCondition.DAMAGED]    
    else:
        possibilities = [condition_record[0]]

    for condition in condition_record[1:]:
        if condition == SpringCondition.UNKNOWN:
            new_possibilities = [possibility + SpringCondition.DAMAGED for possibility in possibilities]
            new_possibilities_with_operational = [possibility + SpringCondition.OPERATIONAL for possibility in possibilities]
            new_possibilities.extend(new_possibilities_with_operational)
            possibilities = new_possibilities
        else:
            for i in range(len(possibilities)):
                possibilities[i] += condition

    return possibilities

def filter_only_valid_records(possibilities: list[ConditionRecord], valid_condition: list[int]) -> list[ConditionRecord]:
    return [possibility for possibility in possibilities if is_valid_under_condition(possibility, valid_condition)]

def is_valid_under_condition(condition_record: ConditionRecord, valid_condition: list[int]) -> bool:
    damaged_springs_group = []
    damaged_springs = ""

    for record in condition_record:
        if record == SpringCondition.DAMAGED:
            damaged_springs += record
        elif len(damaged_springs) > 0:
            damaged_springs_group.append(len(damaged_springs))
            damaged_springs = ""

    if len(damaged_springs) > 0:
        damaged_springs_group.append(len(damaged_springs))

    return len(damaged_springs_group) == len(valid_condition) and all(i == j for i, j in zip(damaged_springs_group, valid_condition))

def read_input(input_path: str) -> list[ConditionRecords]:
    with open(input_path) as f:
        return [parse_line(line.strip()) for line in f.readlines()]


def parse_line(line: str) -> ConditionRecords:
    condition_record, groups_str = line.strip().split(" ")
    valid_groups = [int(integer) for integer in groups_str.strip().split(",")]
    return ConditionRecords(condition_record, valid_groups)

def count_only_valid_possibilities(condition_records: ConditionRecords) -> int:
    all_possibilities = find_all_possibilities(condition_records.condition_record)
    only_valid_possibilities = filter_only_valid_records(all_possibilities, condition_records.valid_group)
    return len(only_valid_possibilities)


condition_records = read_input("./example")
print(sum(count_only_valid_possibilities(condition_record) for condition_record in condition_records))

condition_records = read_input("./input")
print(sum(count_only_valid_possibilities(condition_record) for condition_record in condition_records))