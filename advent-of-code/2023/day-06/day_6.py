import re

def calculate_margin_of_error(times: list[int], record_distances: list[int]) -> int:
    ways_to_beat_the_record = get_ways_to_beat_record(times[0], record_distances[0])
    number_of_ways_to_beat_the_record = len(ways_to_beat_the_record)
    margin_of_error = number_of_ways_to_beat_the_record

    for i, _ in enumerate(times[1:], start=1):
        ways_to_beat_the_record = get_ways_to_beat_record(times[i], record_distances[i])
        number_of_ways_to_beat_the_record = len(ways_to_beat_the_record)
        margin_of_error *= number_of_ways_to_beat_the_record

    return margin_of_error

def get_ways_to_beat_record(time: int, record: int) -> list[int]:
    ways_to_beat_record = []

    for i in range(time+1):
        distance = i * (time - i)
        if distance > record:
            ways_to_beat_record.append(i)

    return ways_to_beat_record

def read_input() -> tuple[int, int]:
    with open("./input") as f:
        times_line, records_line = f.readlines()
        times = [int(number) for number in re.findall(r"([0-9]+)", times_line)]
        records = [int(number) for number in re.findall(r"([0-9]+)", records_line)]
        return times, records
    

def read_input_part_two() -> tuple[int, int]:
    with open("./input") as f:
        times_line, records_line = f.readlines()
        time = int(re.search(r"([0-9]+)", times_line.replace(" ", "")).group())
        record = int(re.search(r"([0-9]+)", records_line.replace(" ", "")).group())
        return time, record

times, records = read_input()
print(calculate_margin_of_error(times, records))

time, record = read_input_part_two()
print(len(get_ways_to_beat_record(time, record)))