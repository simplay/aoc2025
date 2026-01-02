import numpy as np


def max_n_digits_config(banks, num_digits):
    max_digits = []
    for bank in banks:

        from_idx = 0
        max_values = []
        for n in list(range(num_digits))[::-1]:
            sublist = bank[from_idx:len(bank) - n]
            max_jolt_idx = np.argmax(sublist)

            max_value = sublist[max_jolt_idx]
            max_values.append(max_value)

            from_idx += max_jolt_idx + 1

        max_digits.append(int("".join([str(mv) for mv in max_values])))

    return max_digits


def main():
    with open('data/day03.txt') as file:
        banks = [line.strip() for line in file.readlines()]
        banks = [[int(b) for b in list(bank)] for bank in banks]

    print("3a = ", sum(max_n_digits_config(banks, 2)))
    print("3b = ", sum(max_n_digits_config(banks, 12)))


if __name__ == '__main__':
    main()
