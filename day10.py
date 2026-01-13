import numpy as np

def main():
    with open("data/day10.txt") as file:
        lines = [line.strip() for line in file.readlines()]

        def extract_data(line):
            light_diagram, *buttons, requirements = line.split(" ")

            light_diagram = list(light_diagram.replace("[", "").replace("]", ""))
            light_diagram = [True if diag == '#' else False for diag in light_diagram]

            buttons = [button.replace("(", "").replace(")", "") for button in buttons]
            buttons = [[int(bs) for bs in button.split(",")] for button in buttons]

            requirements = list(requirements.replace("{", "").replace("}", "").replace(",", ""))
            requirements = [int(requirement) for requirement in requirements if len(requirement) > 0]

            return light_diagram, buttons, requirements

        def solve_machine_backtracking(num_lights, buttons, light_diagram):
            A = np.zeros((num_lights, len(buttons)), dtype=int)
            for col_idx, button_toggles in enumerate(buttons):
                for light_idx in button_toggles:
                    A[light_idx, col_idx] = 1

            b = np.array(light_diagram, dtype=int).reshape(-1, 1)
            M = np.hstack((A, b))
            rows, cols = M.shape
            num_vars = cols - 1

            # apply the gauss Jordan elimination
            pivot_row = 0
            pivots = []
            for j in range(num_vars):
                if pivot_row >= rows: break
                k = np.argmax(M[pivot_row:, j]) + pivot_row
                if M[k, j] == 0: continue
                M[[pivot_row, k]] = M[[k, pivot_row]]
                for i in range(rows):
                    if i != pivot_row and M[i, j] == 1:
                        M[i] ^= M[pivot_row]
                pivots.append((pivot_row, j))
                pivot_row += 1

            pivot_cols = [pivot[1] for pivot in pivots]
            free_cols = [col for col in range(num_vars) if col not in pivot_cols]

            best_presses = [num_vars + 1]
            current_free_assignment = np.zeros(num_vars, dtype=int)

            def backtrack(free_idx, current_count):
                if current_count >= best_presses[0]:
                    return

                if free_idx == len(free_cols):
                    total_presses = current_count

                    # determine values of pivot buttons based on these free buttons
                    for row_idx, _ in pivots:

                        # get the sum of assigned free variables in this row
                        value = M[row_idx, -1]

                        # calculate vectorized XOR sum of free variables for current row
                        value ^= np.bitwise_xor.reduce(M[row_idx, free_cols] & current_free_assignment[free_cols])
                        if value == 1:
                            total_presses += 1

                    if total_presses < best_presses[0]:
                        best_presses[0] = total_presses

                    return

                curr_col = free_cols[free_idx]

                # handle choice that the button was not pressed
                current_free_assignment[curr_col] = 0
                backtrack(free_idx + 1, current_count)

                # handle choice that the button was pressed
                current_free_assignment[curr_col] = 1
                backtrack(free_idx + 1, current_count + 1)

            backtrack(0, 0)
            return best_presses[0]

    count = 0
    for line in lines:
        light_diagram, buttons, _ = extract_data(line)
        count += solve_machine_backtracking(len(light_diagram), buttons, light_diagram)

    print("10a = ", count)

if __name__ == "__main__":
    main()
