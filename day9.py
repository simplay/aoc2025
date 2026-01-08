import numpy as np
import itertools


def main():
    def area(pair):
        x1, x2 = pair[0][0], pair[1][0]
        width = np.abs(x1 - x2) + 1

        y1, y2 = pair[0][1], pair[1][1]
        height = np.abs(y1 - y2) + 1

        return width * height

    def is_rectangle_valid(pair, row_spans):
        p1, p2 = pair
        x_min, x_max = sorted([p1[0], p2[0]])
        y_min, y_max = sorted([p1[1], p2[1]])

        # Convert Y-range to compressed indices
        iy_start, iy_end = y_map[y_min], y_map[y_max]

        # check every compressed Y-slice the rectangle overlaps
        for j in range(iy_start, iy_end):
            # check whether any span in this slice is wide enough to contain [x_min, x_max]
            if not any(s[0] <= x_min and s[1] >= x_max for s in row_spans[j]):
                return False
        return True

    def grouped_vertical_segments(red_tiles, y_map):
        vert_edges = []
        for i in range(len(red_tiles)):
            p1, p2 = red_tiles[i], red_tiles[(i + 1) % len(red_tiles)]
            if p1[0] == p2[0]:
                y_min, y_max = sorted([p1[1], p2[1]])
                vert_edges.append((p1[0], y_map[y_min], y_map[y_max]))

        return vert_edges

    def get_row_spans(vert_edges, unique_y):
        # note that row_spans[j] corresponds to the vertical gap between unique_y[j] and unique_y[j+1]
        row_spans = {}
        for j in range(len(unique_y) - 1):
            # Find all X-coordinates of vertical walls that cross this Y-slice
            walls = sorted([e[0] for e in vert_edges if e[1] <= j < e[2]])

            # Every pair of walls defines a valid horizontal span
            # this gives us something of the form [(x_start, x_end), (x_start2, x_end2), ...]
            row_spans[j] = [(walls[k], walls[k + 1]) for k in range(0, len(walls), 2)]

        return row_spans

    with open("data/day09.txt") as file:
        red_tiles = [[int(k) for k in line.strip().split(",")] for line in file.readlines()]
        pairs = list(itertools.combinations(red_tiles, 2))

        max_area = np.max([area(pair) for pair in pairs])
        print("9a = ", max_area)

        unique_y = sorted(list(set(t[1] for t in red_tiles)))
        y_map = {y: i for i, y in enumerate(unique_y)}
        vert_edges = grouped_vertical_segments(red_tiles, y_map)
        row_spans = get_row_spans(vert_edges, unique_y)

        pairs = [pair for pair in pairs if is_rectangle_valid(pair, row_spans)]
        max_area = np.max([area(pair) for pair in pairs])
        print("9b = ", max_area)


if __name__ == "__main__":
    main()
