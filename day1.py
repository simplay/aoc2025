import numpy as np


def main():
    with (open("data/day01.txt") as file):
        def normalize(item):
            return int(item.replace("L", "-").replace("R", ""))

        lines = [normalize(item.strip()) for item in file.readlines()]

        position = 50
        overflow_count = 0
        at_zero_count = 0

        for line in lines:
            sign = np.sign(line)
            current_overflow_count = 0
            for _ in range(np.abs(line)):
                was_last_iteration = False
                position += sign
                if position % 100 == 0:
                    current_overflow_count += 1
                    # Prevent double counting: case when ended at zero
                    was_last_iteration = True

            # Remove all final counted zeros
            if was_last_iteration:
                current_overflow_count -= 1

            position = position % 100
            overflow_count += current_overflow_count

            if position == 0:
                at_zero_count += 1

        print("1a = ", at_zero_count)
        print("1b = ", overflow_count + at_zero_count)


if __name__ == '__main__':
    main()
