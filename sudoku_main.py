import os
import random
import time

data = {}

def initialize_board():
    """Initializes an empty Sudoku board with metadata."""
    for i in range(81):
        data[i] = {
            "index": i,
            "col": i % 9,
            "row": i // 9,
            "value": 0,
            "box": (i // 27) * 3 + (i % 9) // 3,
            "pos": [1, 2, 3, 4, 5, 6, 7, 8, 9],
            "state": "ready",
        }

def remove_other(row: int, col: int, box: int, number: int):
    """Removes the possibility of a given number in the row, column, and box."""
    for i in range(81):
        if (
            number in data[i]["pos"] and 
            (data[i]["row"] == row or data[i]["col"] == col or data[i]["box"] == box)
        ):
            data[i]["pos"].remove(number)

def fill_cell(index: int):
    """Fills a cell with a value if there is only one possibility."""
    if len(data[index]["pos"]) == 1 and data[index]["state"] == "ready":
        number = data[index]["pos"].pop()
        data[index]["value"] = number
        data[index]["state"] = "checked"
        remove_other(data[index]["row"], data[index]["col"], data[index]["box"], number)

def sudoku():
    """Generates a Sudoku board by randomly filling values."""
    initialize_board()
    for _ in range(10000):  # Attempts up to 10000 times to avoid deadlocks
        try:
            for index in range(81):
                if data[index]["state"] == "ready":
                    number = random.choice(data[index]["pos"])
                    data[index]["value"] = number
                    data[index]["state"] = "checked"
                    remove_other(data[index]["row"], data[index]["col"], data[index]["box"], number)

            for index in range(81):
                fill_cell(index)
            return  # Exit the function if successful
        except Exception:
            # print("Error occurred. Restarting the board...")
            initialize_board()  # Restart the board on error


def draw(attribute: str):
    """Displays the Sudoku board on the screen with improved formatting."""
    output = ""
    for r in range(9):
        for c in range(9):
            cell_value = str(data[c + 9 * r][attribute]) if data[c + 9 * r]["value"] != 0 else "."
            if c % 3 == 2 and c != 8:
                output += f" {cell_value} |"
            else:
                output += f" {cell_value} "

        output += "\n"
        if r % 3 == 2 and r != 8:
            output += " — — — — + — — — — + — — — — \n"

    print(output)


def super_check():
    """Checks columns, rows, and boxes for uniqueness."""
    print("Columns:")
    for i in range(9):
        column_indices = {data[j]["index"] for j in range(i, 81, 9)}
        if len(column_indices) < 9:
            print(f"There is a problem with column {i}")
        else:
            print(f"Column {i} is fine")

    print("\nRows:")
    for i in range(9):
        row_indices = {data[j]["index"] for j in range(i * 9, (i + 1) * 9)}
        if len(row_indices) < 9:
            print(f"There is a problem with row {i}")
        else:
            print(f"Row {i} is fine")

    print("\nBoxes:")
    for i in range(9):
        box_indices = {data[j]["index"] for j in range(81) if data[j]["box"] == i}
        if len(box_indices) < 9:
            print(f"There is a problem with box {i}")
        else:
            print(f"Box {i} is fine")


os.system("cls" if os.name == "nt" else "clear")

# Execution
start_time = time.process_time()
sudoku()
end_time = time.process_time() - start_time
print(f"\nExecution time: {end_time:.5f} seconds\n")

# Draw the Sudoku board
draw("value")

# Check the Sudoku board
# super_check()