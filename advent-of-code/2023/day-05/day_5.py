from dataclasses import dataclass, field
import re
from typing import Tuple

@dataclass
class Ranges:
    destination_range_start: int
    source_range_start: int
    range_length: int


type Map = list[Ranges]

@dataclass
class Seed:
    range_start: int
    range_length: int

@dataclass
class Almanac:
    seed_to_soil: list[Map] = field(default_factory=list)
    soil_to_fertilizer: list[Map] = field(default_factory=list)
    fertilizer_to_water: list[Map] = field(default_factory=list)
    water_to_light: list[Map] = field(default_factory=list)
    light_to_temperature: list[Map] = field(default_factory=list)
    temperature_to_humidity: list[Map] = field(default_factory=list)
    humidity_to_location: list[Map] = field(default_factory=list)


def find_lowest_location(almanac: Almanac, seeds: list[int]) -> int:
    destination = [find_seed_destination(seed, almanac) for seed in seeds]
    return min(destination)

def find_seed_destination(seed: int, almanac: Almanac) -> int:
    soil = map_number(seed, almanac.seed_to_soil)
    fertilizer = map_number(soil, almanac.soil_to_fertilizer)
    water = map_number(fertilizer, almanac.fertilizer_to_water)
    light = map_number(water, almanac.water_to_light)
    temperature = map_number(light, almanac.light_to_temperature)
    humidity = map_number(temperature, almanac.temperature_to_humidity)
    return map_number(humidity, almanac.humidity_to_location)

def map_number(number: int, map: Map) -> int:
    for range in map:
        if range.source_range_start <= number < range.source_range_start + range.range_length:
            return range.destination_range_start + (number - range.source_range_start)
    return number


def read_input() -> Tuple[Almanac, list[int]]:
    almanac = Almanac()
    with open("./input") as f:
        for line in f.readlines():
            if "seeds" in line:
                seeds = [int(m.group()) for m in re.finditer(r"([0-9]+)", line)]
            if "seed-to-soil map" in line:
                ranges = almanac.seed_to_soil
            if "soil-to-fertilizer map" in line:
                ranges = almanac.soil_to_fertilizer
            if "fertilizer-to-water map" in line:
                ranges = almanac.fertilizer_to_water
            if "water-to-light map" in line:
                ranges = almanac.water_to_light
            if "light-to-temperature map" in line:
                ranges = almanac.light_to_temperature
            if "temperature-to-humidity map" in line:
                ranges = almanac.temperature_to_humidity
            if "humidity-to-location map" in line:
                ranges = almanac.humidity_to_location
            m = re.match(r"([0-9]+) ([0-9]+) ([0-9]+)", line)

            if m:
                range = Ranges(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                ranges.append(range)

    return almanac, seeds


def read_input_part_two():
    almanac = Almanac()
    with open("./input") as f:
        for line in f.readlines():
            if "seeds" in line:
                seeds_line = [(int(m.group(1)), int(m.group(2))) for m in re.finditer(r"([0-9]+) ([0-9]+)", line)]
                seeds = [Seed(range_start, range_length) for range_start, range_length in seeds_line]
            if "seed-to-soil map" in line:
                ranges = almanac.seed_to_soil
            if "soil-to-fertilizer map" in line:
                ranges = almanac.soil_to_fertilizer
            if "fertilizer-to-water map" in line:
                ranges = almanac.fertilizer_to_water
            if "water-to-light map" in line:
                ranges = almanac.water_to_light
            if "light-to-temperature map" in line:
                ranges = almanac.light_to_temperature
            if "temperature-to-humidity map" in line:
                ranges = almanac.temperature_to_humidity
            if "humidity-to-location map" in line:
                ranges = almanac.humidity_to_location
            m = re.match(r"([0-9]+) ([0-9]+) ([0-9]+)", line)

            if m:
                new_range = Ranges(int(m.group(1)), int(m.group(2)), int(m.group(3)))
                ranges.append(new_range)

    return almanac, seeds


def find_lowest_location_part_two(almanac: Almanac, seeds: list[Seed]) -> int:
    possible_lowest_location = 0
    while True:
        humidity = inverted_map(possible_lowest_location, almanac.humidity_to_location)
        temperature = inverted_map(humidity, almanac.temperature_to_humidity)
        light = inverted_map(temperature, almanac.light_to_temperature)
        water = inverted_map(light, almanac.water_to_light)
        fertilizer = inverted_map(water, almanac.fertilizer_to_water)
        soil = inverted_map(fertilizer, almanac.soil_to_fertilizer)
        possible_seed = inverted_map(soil, almanac.seed_to_soil)
        if in_given_seeds(possible_seed, seeds):
            break
        possible_lowest_location += 1

    return possible_lowest_location

def inverted_map(number: int, map: Map) -> int:
    for range in map:
        if range.destination_range_start <= number < range.destination_range_start + range.range_length:
            return range.source_range_start + (number - range.destination_range_start)
    return number

def in_given_seeds(possible_seed: int, seeds: list[Seed]) -> bool:
    for seed in seeds:
        if seed.range_start <= possible_seed < seed.range_start + seed.range_length:
            return True
    return False

almanac, seeds = read_input()
print(find_lowest_location(almanac, seeds))

almanac, seeds = read_input_part_two()
print(find_lowest_location_part_two(almanac, seeds))