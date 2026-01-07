from functools import cache


def visit(start, manifold, max_depth):
    if start[0] + 1 >= max_depth:
        return 0

    split_count = 0
    if manifold[start[0] + 1][start[1]] == ".":
        manifold[start[0] + 1][start[1]] = "|"
        split_count += visit((start[0] + 1, start[1]), manifold, max_depth)
    elif manifold[start[0] + 1][start[1]] == "^":
        split_count = 1

        if start[1] + 1 <= len(manifold[0]):
            manifold[start[0] + 1][start[1] + 1] = "|"
            split_count += visit((start[0] + 1, start[1] + 1), manifold, max_depth)

        if start[1] - 1 >= 0:
            manifold[start[0] + 1][start[1] - 1] = "|"
            split_count += visit((start[0] + 1, start[1] - 1), manifold, max_depth)

    return split_count


def init_manifold():
    with open("data/day07.txt") as file:
        manifold = [list(line.strip()) for line in file.readlines()]

        start = None
        for row_idx, line in enumerate(manifold):
            for col_idx, item in enumerate(line):
                if manifold[row_idx][col_idx] == "S":
                    start = (row_idx, col_idx)
                    break

    return manifold, start


def main():
    manifold, start = init_manifold()

    max_depth = len(manifold)
    total_split_count = visit(start, manifold, max_depth=max_depth)
    print("7a = ", total_split_count)

    @cache
    def count_timelines(start):
        row_idx, col_idx = start

        if row_idx + 1 >= max_depth:
            return 1

        value = manifold[row_idx + 1][col_idx]
        if value == ".":
            return count_timelines((row_idx + 1, col_idx))

        elif value == "^":
            total = 0

            if col_idx - 1 >= 0:
                total += count_timelines((row_idx + 1, col_idx - 1))

            if col_idx + 1 < len(manifold[0]):
                total += count_timelines((row_idx + 1, col_idx + 1))

            return total

        return 0

    manifold, start = init_manifold()
    total_split_count = count_timelines(start)
    print("7b = ", total_split_count)


if __name__ == "__main__":
    main()
