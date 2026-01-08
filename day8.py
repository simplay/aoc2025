from collections import Counter
import numpy as np


def main(filepath, top_n=1000):
    part1(filepath, top_n)
    part2(filepath)


def part2(filepath):
    with open(filepath) as file:
        boxes = [np.array([int(k) for k in line.strip().split(",")]) for line in file if line.strip()]

        num_boxes = len(boxes)
        all_edges = []

        # calculate the distances between all possible pairs
        for i in range(num_boxes):
            for j in range(i + 1, num_boxes):
                dist_sq = np.sum((boxes[i] - boxes[j]) ** 2)
                all_edges.append((dist_sq, i, j))

        # ensure that the shortest edges are first: this ensures that when we reach 1 circuit, that we have found the smallest possible "last edge".
        all_edges.sort()

        parent = list(range(num_boxes))
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]


        num_circuits = num_boxes
        last_pair = (0, 0)
        # connect until there is only one circuit remaining
        for _, i, j in all_edges:
            root_i = find(i)
            root_j = find(j)

            # ensures that we count merges of separate circuits
            if root_i != root_j:
                parent[root_i] = root_j
                num_circuits -= 1

                if num_circuits == 1:
                    last_pair = (i, j)
                    break

        box_a_x = boxes[last_pair[0]][0]
        box_b_x = boxes[last_pair[1]][0]

        print("8b = ", int(box_a_x * box_b_x))


def part1(filepath, top_n):
    with open(filepath) as file:
        boxes = [np.array([int(k) for k in line.strip().split(",")]) for line in file if line.strip()]

        num_boxes = len(boxes)
        all_edges = []

        # calculate metrics (distance, idx1, idx2) between box pairs (the edges)
        for i in range(num_boxes):
            for j in range(i + 1, num_boxes):
                dist_sq = np.sum((boxes[i] - boxes[j]) ** 2)
                all_edges.append((dist_sq, i, j))

        # only consider the shortest N edges
        all_edges.sort()
        top_1000 = all_edges[:top_n]

        # Use Union-Find datastructure similar as described in https://www.geeksforgeeks.org/dsa/introduction-to-disjoint-set-data-structure-or-union-find-algorithm/
        # helps answering to which group a specific box belongs to.
        # Union-Find organizes items into a tree structure. Each group has one "representative" (the root of the tree)
        parent = list(range(num_boxes))

        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_i] = root_j

        # Connect the boxes using the union-find datastructure
        for _, i, j in top_1000:
            union(i, j)

        group_counts = Counter(find(i) for i in range(num_boxes))
        group_counts = sorted(group_counts.values(), reverse=True)

        top_3 = group_counts[:3]
        print("8a = ", np.prod(top_3))


if __name__ == "__main__":
    main("data/day08_test.txt", top_n=10)
    main("data/day08.txt", top_n=1000)
