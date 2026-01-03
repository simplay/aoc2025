import bisect


class IntervalTree:
    def __init__(self):
        # list of disjointa and sorted intervals.
        self.intervals = []

    def search(self, point):
        # Find the first interval that starts after the point
        start_idx = bisect.bisect_right(self.intervals, (point, float('inf')))

        # point is before the very first interval
        if start_idx == 0:
            return False

        interval_start, interval_end = self.intervals[start_idx - 1]
        return [interval_start, interval_end] if point <= interval_end else []

    def add(self, start, end):
        if start > end:
            return

        # find the first index for which interval.start >= start
        start_idx = bisect.bisect_left(self.intervals, (start, end))

        # Check overlap with left neighbor (predecessor):
        # If the new start is <= the previous interval's end, they merge.
        if start_idx > 0 and self.intervals[start_idx - 1][1] >= start:
            # move index back to the predecessor
            start_idx -= 1
            # Extend our start to the predecessor's start
            start = self.intervals[start_idx][0]
            # Extend our end to the max of both
            end = max(end, self.intervals[start_idx][1])

        # check overlap with right neighbors (successor): merge all subsequent intervals that start before and when our new "end" finishes.
        end_idx = start_idx
        while end_idx < len(self.intervals) and self.intervals[end_idx][0] <= end:
            # extend our new end if the successor goes further
            end = max(end, self.intervals[end_idx][1])
            end_idx += 1

        # update
        self.intervals[start_idx:end_idx] = [(start, end)]

    def __repr__(self):
        return f"IntervalTree({self.intervals})"

    def __iter__(self):
        return iter(self.intervals)

    def __getitem__(self, index):
        return self.intervals[index]

    def __len__(self):
        return len(self.intervals)


def main():
    with open("data/day05.txt") as file:
        tree = IntervalTree()
        lines = [line.strip() for line in file.readlines()]

        ranges = []
        tests = []
        alter = False
        for line in lines:
            if len(line) == 0:
                alter = True

            if alter and len(line) > 0:
                tests.append(int(line))
            elif len(line) > 0:
                left, right = line.split("-")
                ranges.append(range(int(left), int(right) + 1))
                tree.add(int(left), int(right))

        counter = 0
        for test in tests:
            for _range in ranges:
                if test in _range:
                    counter += 1
                    break

        print("5a = ", counter)

        sum = 0
        for interval in tree.intervals:
            sum += interval[1] - interval[0] + 1

        print("5b = ", sum)


if __name__ == "__main__":
    main()
