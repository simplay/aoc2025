import re
import numpy as np
from functools import reduce


def part1(lines):
    lines = [line.strip() for line in lines]
    lines = [re.split(r"\s+", line) for line in lines]

    sequences = np.array([[int(item) for item in line] for line in lines[:-1]]).T
    operators = lines[-1]

    operations = {
        "+": lambda a, b: a + b,
        "*": lambda a, b: a * b
    }

    sum = 0
    for idx, operator in enumerate(operators):
        sequence = sequences[idx]
        sum += reduce(operations[operator], sequence)

    return sum


def part2(raw_lines):
    # idea: move a scanline from right to left and intersect all column to form new numbers
    # after the grouping, perform calculations like in a)
    sequences = raw_lines[:-1]
    lines = [line.strip() for line in raw_lines]
    lines = [re.split(r"\s+", line) for line in lines]
    operators = lines[-1]

    columns = []
    col_values = []
    for idx in range(len(sequences[0])):
        # cs is used to form new numbers
        cs = [sequence[idx] for sequence in sequences]
        col_values.append("".join(cs))

        # cs2 is used to determine gaps to latter group column values for aggregations
        cs2 = [sequence[idx].strip() for sequence in sequences]
        cs2 = [0 if len(se) == 0 else 1 for se in cs2]
        columns.append(
            np.sum(cs2)
        )
    col_values = [col_val.replace(",", '').strip() for col_val in col_values]
    col_values = [int(col_val) for col_val in col_values if len(col_val.strip()) > 0]

    counter = 0
    counters = []
    for column in columns:
        if column == 0:
            counters.append(counter)
            counter = 0
        else:
            counter += 1
    counters.append(counter)

    idx = 0
    new_sequences = []
    for counter in counters:
        new_sequence = []
        for _ in range(counter):
            new_sequence.append(col_values[idx])
            idx += 1
        new_sequences.append(new_sequence)

    operations = {
        "+": lambda a, b: a + b,
        "*": lambda a, b: a * b
    }

    sum = 0
    for idx, operator in enumerate(operators):
        sequence = new_sequences[idx]
        sum += reduce(operations[operator], sequence)

    return sum


def main():
    with open("data/day06.txt") as file:
        lines = [line.replace("\n", "") for line in file.readlines()]

    print("6a = ", part1(lines))
    print("6b = ", part2(lines))


if __name__ == "__main__":
    main()
