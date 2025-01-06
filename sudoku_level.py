# Level Empty Cells 
# 1 (Easy) - 40 to 45
# 2 (Medium) - 46 to 49
# 3 (Difficult) - 50 to 53
# 4 (Extremely Difficult) - 54 to 58


import copy
import os
import random
from sudoku_main import sudoku

sudoku_board_data = sudoku()

def create_gaps(data, n):
    """Creates gaps in the Sudoku board by marking cells as empty."""
    data_new = copy.deepcopy(data)

    while n > 0:
        indices = random.sample(range(81), k=n)  # Choose n unique cells
        for i in indices:
            if data_new[i]["state"] != "empty":
                data_new[i]["state"] = "empty"
                data_new[i]["pos"] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                n -= 1
                if n == 0:
                    break
    return data_new

def draw_board(attribute, data):
    """Displays the Sudoku board on the screen with enhanced formatting."""
    output = ""
    for r in range(9):
        row = []
        for c in range(9):
            cell_value = "X" if data[c + 9 * r]["state"] == "empty" else f"{data[c + 9 * r][attribute]}"
            row.append(cell_value.center(3))
        output += " | ".join([" ".join(row[i:i+3]) for i in range(0, 9, 3)]) + "\n"
        if r % 3 == 2 and r != 8:
            output += "— — — — — — + — — — — — — + — — — — — —\n"

    print(output)

os.system("cls" if os.name == "nt" else "clear")

# data_new = create_gaps(sudoku_board_data, 50)  # Adjust number of gaps as needed

# draw_board("value", sudoku_board_data)  # Original board
# draw_board("value", data_new)  # Board with gaps
# draw_board("index", data_new)  # Board with gaps

def remove_pos(data_new):
    """Removes invalid possibilities from empty cells based on Sudoku rules."""
    # Rows
    for i in range(9):
        row_start = i * 9
        checked_values = [data_new[row_start + j]["value"] for j in range(9) if data_new[row_start + j]["state"] == "checked"]
        for j in range(9):
            cell = data_new[row_start + j]
            if cell["state"] == "empty":
                cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

    # Columns
    for i in range(9):
        checked_values = [data_new[j * 9 + i]["value"] for j in range(9) if data_new[j * 9 + i]["state"] == "checked"]
        for j in range(9):
            cell = data_new[j * 9 + i]
            if cell["state"] == "empty":
                cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

    # Boxes
    for i in range(9):
        box_start = (i // 3) * 27 + (i % 3) * 3
        box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]
        checked_values = [data_new[idx]["value"] for idx in box_indices if data_new[idx]["state"] == "checked"]
        for idx in box_indices:
            cell = data_new[idx]
            if cell["state"] == "empty":
                cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

# remove_pos(data_new)

def draw_possibilities(data):
    """Displays the Sudoku board with possible values for empty cells."""
    output = ""
    for r in range(9):
        row = []
        for c in range(9):
            cell = data[c + 9 * r]
            if cell["state"] == "empty":
                cell_value = str(cell["pos"]).replace(" ", "")  # Remove spaces for compact display
            else:
                cell_value = "[]"
            row.append(cell_value.center(9))
        output += " | ".join([" ".join(row[i:i+3]) for i in range(0, 9, 3)]) + "\n"
        if r % 3 == 2 and r != 8:
            output += "— — — — — — — — — — — — — — — + — — — — — — — — — — — — — — — + — — — — — — — — — — — — — — —\n"

    print(output)

# draw_possibilities(data_new)  # Board with gaps


def remove_other_new(r, c, b, n):
    """Removes a value from possibilities in related rows, columns, and boxes."""
    for i in range(81):
        if n in data_new[i]["pos"]:
            if data_new[i]["row"] == r or data_new[i]["col"] == c or data_new[i]["box"] == b:
                data_new[i]["pos"].remove(n)

def one_in_box():
    """Finds and processes cells with unique possibilities within boxes."""
    for k in range(9):
        obj = {i: {"value": 0, "pos": []} for i in range(1, 10)}
        box_start = (k // 3) * 27 + (k % 3) * 3
        box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

        for idx in box_indices:
            for i in range(1, 10):
                if i in data_new[idx]["pos"]:
                    obj[i]["value"] += 1
                    obj[i]["pos"].append(idx)

        for i in range(1, 10):
            if obj[i]["value"] == 1:
                unique_idx = obj[i]["pos"][0]
                data_new[unique_idx]["value_new"] = i
                data_new[unique_idx]["pos"] = []
                remove_other_new(data_new[unique_idx]["row"], data_new[unique_idx]["col"], data_new[unique_idx]["box"], i)

def one_in_row():
    """Finds and processes cells with unique possibilities within rows."""
    for r in range(9):
        obj = {i: {"value": 0, "pos": []} for i in range(1, 10)}
        row_start = r * 9
        for i in range(9):
            for n in range(1, 10):
                if n in data_new[row_start + i]["pos"]:
                    obj[n]["value"] += 1
                    obj[n]["pos"].append(row_start + i)

        for n in range(1, 10):
            if obj[n]["value"] == 1:
                unique_idx = obj[n]["pos"][0]
                data_new[unique_idx]["value_new"] = n
                data_new[unique_idx]["pos"] = []
                remove_other_new(data_new[unique_idx]["row"], data_new[unique_idx]["col"], data_new[unique_idx]["box"], n)

def one_in_col():
    """Finds and processes cells with unique possibilities within columns."""
    for c in range(9):
        obj = {i: {"value": 0, "pos": []} for i in range(1, 10)}
        for r in range(9):
            idx = r * 9 + c
            for n in range(1, 10):
                if n in data_new[idx]["pos"]:
                    obj[n]["value"] += 1
                    obj[n]["pos"].append(idx)

        for n in range(1, 10):
            if obj[n]["value"] == 1:
                unique_idx = obj[n]["pos"][0]
                data_new[unique_idx]["value_new"] = n
                data_new[unique_idx]["pos"] = []
                remove_other_new(data_new[unique_idx]["row"], data_new[unique_idx]["col"], data_new[unique_idx]["box"], n)

def naked_pair():
    """Identifies and processes naked pairs in rows, columns, and boxes."""
    for group_type in ['row', 'col', 'box']:
        for i in range(9):
            candidates = []
            if group_type == 'row':
                indices = [i * 9 + j for j in range(9)]
            elif group_type == 'col':
                indices = [j * 9 + i for j in range(9)]
            else:
                box_start = (i // 3) * 27 + (i % 3) * 3
                indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

            for idx in indices:
                if len(data_new[idx]['pos']) == 2:
                    candidates.append((idx, set(data_new[idx]['pos'])))

            for idx1, pair1 in candidates:
                for idx2, pair2 in candidates:
                    if idx1 != idx2 and pair1 == pair2:
                        for idx in indices:
                            if idx != idx1 and idx != idx2 and len(data_new[idx]['pos']) > 0:
                                data_new[idx]['pos'] = [n for n in data_new[idx]['pos'] if n not in pair1]

def hidden_pairs():
    """Identifies and processes hidden pairs in rows, columns, and boxes."""
    for group_type in ['row', 'col', 'box']:
        for i in range(9):
            if group_type == 'row':
                indices = [i * 9 + j for j in range(9)]
            elif group_type == 'col':
                indices = [j * 9 + i for j in range(9)]
            else:
                box_start = (i // 3) * 27 + (i % 3) * 3
                indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

            occurrences = {n: [] for n in range(1, 10)}
            for idx in indices:
                for n in data_new[idx]['pos']:
                    occurrences[n].append(idx)

            for pair in [(x, y) for x in range(1, 10) for y in range(x + 1, 10)]:
                if len(set(occurrences[pair[0]] + occurrences[pair[1]])) == 2:
                    shared_indices = set(occurrences[pair[0]] + occurrences[pair[1]])
                    for idx in shared_indices:
                        data_new[idx]['pos'] = [n for n in data_new[idx]['pos'] if n in pair]

def x_wing():
    """Identifies and processes X-Wing patterns in rows and columns."""
    for digit in range(1, 10):
        # Check rows
        row_positions = []
        for r in range(9):
            positions = [c for c in range(9) if digit in data_new[r * 9 + c]['pos']]
            if len(positions) == 2:
                row_positions.append((r, positions))

        for (r1, p1), (r2, p2) in [(x, y) for x in row_positions for y in row_positions if x != y]:
            if p1 == p2:
                for c in p1:
                    for r in range(9):
                        if r != r1 and r != r2 and digit in data_new[r * 9 + c]['pos']:
                            data_new[r * 9 + c]['pos'].remove(digit)

        # Check columns
        col_positions = []
        for c in range(9):
            positions = [r for r in range(9) if digit in data_new[r * 9 + c]['pos']]
            if len(positions) == 2:
                col_positions.append((c, positions))

        for (c1, p1), (c2, p2) in [(x, y) for x in col_positions for y in col_positions if x != y]:
            if p1 == p2:
                for r in p1:
                    for c in range(9):
                        if c != c1 and c != c2 and digit in data_new[r * 9 + c]['pos']:
                            data_new[r * 9 + c]['pos'].remove(digit)

def swordfish():
    """Identifies and processes Swordfish patterns in rows and columns."""
    for digit in range(1, 10):
        # Check rows
        row_candidates = {r: [c for c in range(9) if digit in data_new[r * 9 + c]['pos']] for r in range(9)}
        rows_with_candidates = [r for r, cols in row_candidates.items() if 2 <= len(cols) <= 3]

        for r1, r2, r3 in [(x, y, z) for x in rows_with_candidates for y in rows_with_candidates for z in rows_with_candidates if x < y < z]:
            common_cols = set(row_candidates[r1]) & set(row_candidates[r2]) & set(row_candidates[r3])
            if len(common_cols) == 3:
                for r in range(9):
                    if r not in [r1, r2, r3]:
                        for c in common_cols:
                            if digit in data_new[r * 9 + c]['pos']:
                                data_new[r * 9 + c]['pos'].remove(digit)

        # Check columns
        col_candidates = {c: [r for r in range(9) if digit in data_new[r * 9 + c]['pos']] for c in range(9)}
        cols_with_candidates = [c for c, rows in col_candidates.items() if 2 <= len(rows) <= 3]

        for c1, c2, c3 in [(x, y, z) for x in cols_with_candidates for y in cols_with_candidates for z in cols_with_candidates if x < y < z]:
            common_rows = set(col_candidates[c1]) & set(col_candidates[c2]) & set(col_candidates[c3])
            if len(common_rows) == 3:
                for c in range(9):
                    if c not in [c1, c2, c3]:
                        for r in common_rows:
                            if digit in data_new[r * 9 + c]['pos']:
                                data_new[r * 9 + c]['pos'].remove(digit)

def check_new():
    """Checks for cells with a single possibility and resolves them."""
    progress = False
    for i in range(81):
        if len(data_new[i]["pos"]) == 1 and data_new[i]["state"] == "empty":
            value = data_new[i]["pos"].pop()
            data_new[i]["value_new"] = value
            remove_other_new(data_new[i]["row"], data_new[i]["col"], data_new[i]["box"], value)
            progress = True
    return not progress

def solver():
    """Solves the Sudoku puzzle using logical deduction."""
    iterations = 0
    while True:
        one_in_box()
        one_in_row()
        one_in_col()

        naked_pair()
        hidden_pairs()
        swordfish()
        x_wing()

        # print(f"Iteration {iterations+1}")
        # draw_possibilities(data_new)

        if check_new():
            break
        iterations += 1
        if iterations > 50:  # Prevent infinite loops
            break

def check_pos():
    """Validates the current state of the board for any unresolved cells."""
    for i in range(81):
        if data_new[i]["state"] == "empty" and len(data_new[i]["pos"]) > 0:
            return True
    return False

# solver()

# if not check_pos():
#     print("Sudoku solved successfully!")
# else:
#     print("Sudoku could not be fully solved.")


correct = 0
wrong = 0

for _ in range(1000):
    data_new_copy = copy.deepcopy(sudoku_board_data)
    data_new = create_gaps(data_new_copy, 50)
    remove_pos(data_new)
    solver()

    if not check_pos():
        correct += 1
    else:
        wrong += 1

print(f"Correct: {correct}\nWrong: {wrong}")
