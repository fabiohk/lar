from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum
import re


class Result(StrEnum):
    ACCEPTED = "A"
    REJECTED = "R"

type Rating = dict[str, int]

type Rule = Callable[[Rating], str] # returns an empty string when the rule is not satisfied, otherwise returns the next workflow

@dataclass
class Workflow:
    rules: list[Rule]

type Workflows = dict[str, Workflow]

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
    return Workflow([parse_rule(rule) for rule in rules])

def parse_rule(rule: str) -> Rule:
    if ":" in rule:
        return parse_rule_with_operator(rule)
    return lambda _: rule

def parse_rule_with_operator(rule: str) -> Rule:
    if "<" in rule:
        return parse_le_condition(rule)
    return parse_gt_condition(rule)

def parse_le_condition(rule: str) -> Rule:
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


workflows, ratings = read_input("./example")
print(sum_all_ratings_from_accepted_parts(workflows, ratings))

workflows, ratings = read_input("./input")
print(sum_all_ratings_from_accepted_parts(workflows, ratings))