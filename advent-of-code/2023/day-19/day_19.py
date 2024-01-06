from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
from queue import SimpleQueue
import re
from typing import Optional

class Operator(StrEnum):
    LESS_THAN = "<"
    GREATER_THAN = ">"

class Result(StrEnum):
    ACCEPTED = "A"
    REJECTED = "R"

type Rating = dict[str, int]

type Rule = Callable[[Rating], str] # returns an empty string when the rule is not satisfied, otherwise returns the next workflow

@dataclass
class Operation:
    rating_key: str
    operator: Operator
    value: int

@dataclass
class RuleV2:
    next_workflow: str
    operation: Optional[Operation] = None

@dataclass
class Workflow:
    rules: list[Rule]
    rules_v2: list[RuleV2]

type Workflows = dict[str, Workflow]

@dataclass
class Interval:
    min: int
    max: int

type Intervals = dict[str, Interval]

def run_rating_through_workflow(rating: Rating, workflows: Workflows) -> Result:
    current_workflow = "in"
    while current_workflow not in [Result.ACCEPTED, Result.REJECTED]:
        workflow = workflows[current_workflow]
        for rule in workflow.rules:
            next_workflow = rule(rating)
            if next_workflow:
                current_workflow = next_workflow
                break
    return current_workflow


def read_input(input_path: str) -> tuple[Workflows, list[Rating]]:
    workflows: Workflows = {}
    ratings: list[Rating] = []
    with open(input_path) as f:
        for line in f.readlines():
            stripped_line = line.strip()
            if not stripped_line:
                continue
            if is_workflow(stripped_line):
                label, workflow = parse_workflow(stripped_line)
                workflows[label] = workflow
            if is_rating(stripped_line):
                ratings.append(parse_ratings(stripped_line))

    return workflows, ratings

def is_workflow(line: str) -> bool:
    return not is_rating(line)

def is_rating(line: str) -> bool:
    return line.startswith("{")

def parse_workflow(line: str) -> tuple[str, Workflow]:
    label, workflow = line.strip("}").split("{")
    rules = workflow.split(",")
    return label, parse_rules(rules)

def parse_rules(rules: list[str]) -> Workflow:
    return Workflow([parse_rule(rule) for rule in rules], [parse_rule_v2(rule) for rule in rules])

def parse_rule_v2(rule: str) -> RuleV2:
    if ":" in rule:
        return parse_rule_with_operator_v2(rule)
    return RuleV2(rule)

def parse_rule_with_operator_v2(rule: str) -> RuleV2:
    if "<" in rule:
        return parse_lt_condition_v2(rule)
    return parse_gt_condition_v2(rule)

def parse_lt_condition_v2(rule: str) -> RuleV2:
    condition, next_workflow = rule.split(":")
    key, value = condition.split("<")
    return RuleV2(next_workflow, Operation(key, Operator.LESS_THAN, int(value)))

def parse_gt_condition_v2(rule: str) -> RuleV2:
    condition, next_workflow = rule.split(":")
    key, value = condition.split(">")
    return RuleV2(next_workflow, Operation(key, Operator.GREATER_THAN, int(value)))

def parse_rule(rule: str) -> Rule:
    if ":" in rule:
        return parse_rule_with_operator(rule)
    return lambda _: rule

def parse_rule_with_operator(rule: str) -> Rule:
    if "<" in rule:
        return parse_lt_condition(rule)
    return parse_gt_condition(rule)

def parse_lt_condition(rule: str) -> Rule:
    condition, next_workflow = rule.split(":")
    key, value = condition.split("<")
    return lambda rating: next_workflow if rating[key] < int(value) else ""

def parse_gt_condition(rule: str) -> Rule:
    condition, next_workflow = rule.split(":")
    key, value = condition.split(">")
    return lambda rating: next_workflow if rating[key] > int(value) else ""

def parse_ratings(line: str) -> Rating:
    ratings = re.sub(r"[\{|\}]*", "", line)
    x_rating, m_rating, a_rating, s_rating = ratings.split(",")
    return {
        "x": parse_rating(x_rating),
        "m": parse_rating(m_rating),
        "a": parse_rating(a_rating),
        "s": parse_rating(s_rating),
    }

def parse_rating(rating: str) -> int:
    _, value = rating.split("=")
    return int(value)

def sum_all_ratings_from_accepted_parts(workflows: Workflows, ratings: list[Rating]) -> int:
    total_sum = 0
    for rating in ratings:
        result = run_rating_through_workflow(rating, workflows)
        if result == Result.ACCEPTED:
            total_sum += sum(value for value in rating.values())
    return total_sum


def find_accepted_intervals(workflows: Workflows) -> list[Intervals]:
    starting_intervals = {
        "x": Interval(0, 4001),
        "m": Interval(0, 4001),
        "a": Interval(0, 4001),
        "s": Interval(0, 4001)
    }
    accepted_intervals: list[Intervals] = []
    queue = SimpleQueue()
    queue.put(("in", starting_intervals))

    while not queue.empty():
        workflow, intervals = queue.get()
        if workflow == Result.ACCEPTED:
            accepted_intervals.append(intervals)
            continue
        if workflow == Result.REJECTED:
            continue
        for rule in workflows[workflow].rules_v2:
            new_intervals, intervals = adjust_intervals(intervals, rule)
            next_workflow = rule.next_workflow
            queue.put((next_workflow, new_intervals))
    return accepted_intervals

def adjust_intervals(intervals: Intervals, rule: RuleV2) -> tuple[Intervals, Intervals]:
    if not rule.operation:
        return intervals, intervals
    
    if rule.operation.operator == Operator.LESS_THAN:
        return adjust_intervals_with_lt_operator(intervals, rule.operation)
    return adjust_intervals_with_gt_operator(intervals, rule.operation)

def adjust_intervals_with_lt_operator(intervals: Intervals, operation: Operation) -> tuple[Intervals, Intervals]:
    new_intervals = {}
    opposite_intervals = {}

    for key, interval in intervals.items():
        if key != operation.rating_key:
            new_intervals[key] = interval
            opposite_intervals[key] = interval
        else:
            new_intervals[key] = Interval(interval.min, operation.value)
            opposite_intervals[key] = Interval(operation.value - 1, interval.max)
    
    return new_intervals, opposite_intervals

def adjust_intervals_with_gt_operator(intervals: Intervals, operation: Operation) -> tuple[Intervals, Intervals]:
    new_intervals = {}
    opposite_intervals = {}

    for key, interval in intervals.items():
        if key != operation.rating_key:
            new_intervals[key] = interval
            opposite_intervals[key] = interval
        else:
            new_intervals[key] = Interval(operation.value, interval.max)
            opposite_intervals[key] = Interval(interval.min, operation.value + 1)
    
    return new_intervals, opposite_intervals


def count_possible_combinations(workflows: Workflows) -> int:
    accepted_intervals = find_accepted_intervals(workflows)
    return sum(count_combination_from_intervals(intervals) for intervals in accepted_intervals)

def count_combination_from_intervals(intervals: Intervals) -> int:
    total_combinations = 1
    for interval in intervals.values():
        total_combinations *= (interval.max - interval.min - 1)
    return total_combinations

workflows, ratings = read_input("./example")
print(sum_all_ratings_from_accepted_parts(workflows, ratings))
print(count_possible_combinations(workflows))

workflows, ratings = read_input("./input")
print(sum_all_ratings_from_accepted_parts(workflows, ratings))
print(count_possible_combinations(workflows))