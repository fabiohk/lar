def solution(l, r):
    confortables_map = calculate_confortables_map(l, r)
    confortables_pair_count = 0

    for a, confortables in confortables_map.items():
        for b in confortables:
            if a in confortables_map.get(b, []):
                confortables_pair_count += 1

    return confortables_pair_count // 2


def calculate_confortables_map(l, r):
    return {i: calculate_confortables(i) for i in range(l, r + 1)}


def calculate_confortables(integer):
    digits_sum = calculate_digits_sum(integer)

    return [
        i for i in range(integer - digits_sum, integer + digits_sum + 1) if i != integer
    ]


def calculate_digits_sum(integer):
    digits_sum = 0

    while integer > 0:
        digit = integer % 10
        digits_sum += digit
        integer //= 10

    return digits_sum
