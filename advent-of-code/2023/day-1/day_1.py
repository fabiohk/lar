digits_letters_map = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}
valid_letters = digits_letters_map.keys()

def is_digit(char: str) -> bool:
    return '0' <= char <= '9'

def retrieve_calibration_value_from_line_first_part(line: str) -> int:
    digits_in_line = [c for c in line if is_digit(c)]

    first_digit = digits_in_line[0]
    last_digit = digits_in_line[-1]

    return int(first_digit) * 10 + int(last_digit)

def is_possible_digit(possible_digit: str) -> bool:
    return any(valid_letter.find(possible_digit) == 0 for valid_letter in valid_letters)

def retrieve_calibration_value_from_line_second_part(line: str) -> int:
    digits_in_line = []
    possible_digit = ''

    for c in line:
        possible_digit += c
        if is_digit(c):
            digits_in_line.append(c)
            possible_digit = ''
        elif not is_possible_digit(possible_digit):
            while len(possible_digit) > 0 and not is_possible_digit(possible_digit):
                possible_digit = possible_digit[1:]
        elif possible_digit in valid_letters:
            digit = digits_letters_map[possible_digit]
            digits_in_line.append(digit)
            
            if possible_digit in ('one', 'three', 'five', 'nine'):
                possible_digit = 'e'
            elif possible_digit in ('seven'):
                possible_digit = 'n'
            elif possible_digit in ('eight'):
                possible_digit = 't'
            elif possible_digit in ('two'):
                possible_digit = 'o'
            else:
                possible_digit = ''

    first_digit = digits_in_line[0]
    last_digit = digits_in_line[-1]

    print(int(first_digit) * 10 + int(last_digit))
    return int(first_digit) * 10 + int(last_digit)


def sum_calibration_values_from_document(document: list[str]) -> int:
    return sum([retrieve_calibration_value_from_line_second_part(line) for line in document])

def read_input() -> list[str]:
    with open('./input') as f:
        return f.readlines()


document = read_input()
calibration_values_sum = sum_calibration_values_from_document(document)
print(calibration_values_sum)