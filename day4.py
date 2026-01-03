import numpy as np
from scipy.signal import convolve


def task4a(rows):
    A = np.array(rows)
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])

    convolved = convolve(A, kernel, mode='same')

    return np.sum(convolved[A == 1] < 4)


def task4b(rows):
    total_removed = 0

    A = np.array(rows)
    kernel = np.array([
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ])

    while True:
        convolved = convolve(A, kernel, mode='same')
        removed_items = np.sum(convolved[A == 1] < 4)
        masked_convolved = np.multiply(convolved, A)

        total_removed += removed_items
        if removed_items == 0:
            break

        keep = ~(masked_convolved < 4)
        A = A * keep

    return total_removed


def main():
    with open('data/day04.txt') as file:
        rows = []
        for line in file.readlines():
            row = [0 if item == "." else 1 for item in list(line.strip())]
            rows.append(row)

    print("4a = ", task4a(rows))
    print("4b = ", task4b(rows))


if __name__ == "__main__":
    main()
