from dataclasses import dataclass
from enum import StrEnum
from functools import cache


class SpringCondition(StrEnum):
    OPERATIONAL = "."
    DAMAGED = "#"
    UNKNOWN = "?"

type ConditionRecord = str

@dataclass
class ConditionRecords:
    condition_record: ConditionRecord
    valid_group: list[int]


@dataclass
class Auxiliar:
    condition_record: ConditionRecord
    damaged_group: ConditionRecord
    current_group_index: int

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

def unfold_condition_records(condition_records: ConditionRecords) -> ConditionRecords:
    new_condition_records = "?".join([condition_records.condition_record] * 5)
    new_valid_group = condition_records.valid_group * 5
    return ConditionRecords(new_condition_records, new_valid_group)


def find_only_valid_records(condition_records: ConditionRecords) -> list[ConditionRecord]:
    condition_record = condition_records.condition_record

    if condition_record[0] == SpringCondition.UNKNOWN:
        possibilities = [Auxiliar(SpringCondition.OPERATIONAL, "", 0), Auxiliar(SpringCondition.DAMAGED, SpringCondition.DAMAGED, 0)]
    else:
        possibilities = [Auxiliar(condition_record[0], "" if SpringCondition.OPERATIONAL else SpringCondition.DAMAGED, 0)]

    for condition in condition_record[1:]:
        if condition == SpringCondition.UNKNOWN:
            new_possibilities = [Auxiliar(possibility.condition_record + SpringCondition.DAMAGED, possibility.damaged_group + SpringCondition.DAMAGED, possibility.current_group_index) for possibility in possibilities]
            new_possibilities_with_operational = [Auxiliar(possibility.condition_record + SpringCondition.OPERATIONAL, possibility.damaged_group, possibility.current_group_index) for possibility in possibilities]
            new_possibilities.extend(new_possibilities_with_operational)
            possibilities = new_possibilities
        else:
            for i in range(len(possibilities)):
                possibilities[i].condition_record += condition
                possibilities[i].damaged_group += condition if condition == SpringCondition.DAMAGED else ""

        possibilities = filter_only_still_valid_conditions(possibilities, condition_records.valid_group)

    
    return filter_only_valid_records([possibility.condition_record for possibility in possibilities], condition_records.valid_group)


def filter_only_still_valid_conditions(conditions_records: list[Auxiliar], valid_group: list[int]) -> list[Auxiliar]:
    filtered_records = []

    for condition_record in conditions_records:
        if condition_record.current_group_index >= len(valid_group) and condition_record.condition_record[-1] == SpringCondition.DAMAGED:
            continue
        if condition_record.current_group_index >= len(valid_group) and condition_record.condition_record[-1] == SpringCondition.OPERATIONAL:
            filtered_records.append(condition_record)
            continue
        if len(condition_record.damaged_group) == 0:
            filtered_records.append(condition_record)
        if condition_record.condition_record[-1] == SpringCondition.OPERATIONAL and len(condition_record.damaged_group) == valid_group[condition_record.current_group_index]:
            new_auxiliar = Auxiliar(condition_record.condition_record, "", condition_record.current_group_index+1)
            filtered_records.append(new_auxiliar)
        if condition_record.condition_record[-1] == SpringCondition.DAMAGED and len(condition_record.damaged_group) <= valid_group[condition_record.current_group_index]:
            filtered_records.append(condition_record)

    return filtered_records


def count_only_valid_possibilities_part_two(condition_record: ConditionRecords) -> int:
    valid_records = find_only_valid_records(condition_record)
    return len(valid_records)

@cache
def count_only_valid_possibilities_part_two_recursion(condition_record: ConditionRecord, valid_group: tuple) -> int:
    if not valid_group:
        return 1 if SpringCondition.DAMAGED not in condition_record else 0
    
    if len(condition_record) + 1 < sum(valid_group) + len(valid_group):
        return 0
    
    has_operational = SpringCondition.OPERATIONAL in condition_record[:valid_group[0]]
    if len(condition_record) == valid_group[0] and len(valid_group) == 1:
        return 1 if not has_operational else 0
    
    can_use = not has_operational and condition_record[valid_group[0]] != SpringCondition.DAMAGED
    if condition_record[0] == SpringCondition.DAMAGED:
        return count_only_valid_possibilities_part_two_recursion(condition_record[valid_group[0]+1:].lstrip(SpringCondition.OPERATIONAL), tuple(valid_group[1:])) if can_use else 0
    skip = count_only_valid_possibilities_part_two_recursion(condition_record[1:].lstrip(SpringCondition.OPERATIONAL), valid_group)
    if not can_use:
        return skip
    return skip + count_only_valid_possibilities_part_two_recursion(condition_record[valid_group[0]+1:].lstrip(SpringCondition.OPERATIONAL), tuple(valid_group[1:]))

condition_records = read_input("./example")
print(sum(count_only_valid_possibilities(condition_record) for condition_record in condition_records))
print(sum(count_only_valid_possibilities_part_two(condition_record) for condition_record in condition_records))
print(sum(count_only_valid_possibilities_part_two_recursion(condition_record.condition_record.lstrip(SpringCondition.OPERATIONAL), tuple(condition_record.valid_group)) for condition_record in condition_records))
unfolded_condition_records = [unfold_condition_records(condition_record) for condition_record in condition_records]
print(sum(count_only_valid_possibilities_part_two_recursion(condition_record.condition_record.lstrip(SpringCondition.OPERATIONAL), tuple(condition_record.valid_group)) for condition_record in unfolded_condition_records))

condition_records = read_input("./input")
print(sum(count_only_valid_possibilities(condition_record) for condition_record in condition_records))
print(sum(count_only_valid_possibilities_part_two_recursion(condition_record.condition_record.lstrip(SpringCondition.OPERATIONAL), tuple(condition_record.valid_group)) for condition_record in condition_records))
unfolded_condition_records = [unfold_condition_records(condition_record) for condition_record in condition_records]
print(sum(count_only_valid_possibilities_part_two_recursion(condition_record.condition_record.lstrip(SpringCondition.OPERATIONAL), tuple(condition_record.valid_group)) for condition_record in unfolded_condition_records))