def filter1(intervals):
    invalid_ids = []
    for (a, b) in intervals:
        for value in range(a, b + 1):
            if len(str(value)) % 2 == 0:
                til_left = int(0.5 * len(str(value)))
                left = str(value)[:til_left]
                right = str(value)[til_left:]
                if int(left) == int(right):
                    invalid_ids.append(value)

    return invalid_ids


def filter2(intervals):
    def get_substrings(ivalue):
        value = str(ivalue)

        substrings = []
        tmp = ""
        for l in range(len(value)):
            tmp += value[l]
            substrings.append(tmp)

        return substrings[:-1]

    invalid_ids = []
    for (a, b) in intervals:
        for value in range(a, b + 1):
            substrings = get_substrings(value)
            for idx, substring in enumerate(substrings):
                factor = int(len(str(value)) / (idx + 1))
                extended_substring = substring * factor

                if int(extended_substring) == int(value):
                    invalid_ids.append(value)
                    break

    return invalid_ids


def main():
    with open('data/day02.txt') as file:
        intervals = [interval.split("-") for interval in file.readline().strip().split(",")]
        intervals = [(int(a), int(b)) for (a, b) in intervals]

        print("2a = ", sum(filter1(intervals)))
        print("2b = ", sum(filter2(intervals)))


if __name__ == '__main__':
    main()
