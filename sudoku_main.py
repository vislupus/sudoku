import os
import random
import time
from matplotlib import pyplot as plt

data = {}

def initialize_board():
    """Initializes an empty Sudoku board with metadata."""
    for i in range(81):
        data[i] = {
            "index": i,
            "col": i % 9,
            "row": i // 9,
            "value": 0,
            "box": (i // 9 // 3) * 3 + (i % 9) // 3,
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
    for _ in range(10000):  # Attempts up to 100 times to avoid deadlocks
        try:
            for index in range(81):
                if data[index]["state"] == "ready":
                    number = random.choice(data[index]["pos"])
                    data[index]["value"] = number
                    data[index]["state"] = "checked"
                    remove_other(data[index]["row"], data[index]["col"], data[index]["box"], number)

            for index in range(81):
                fill_cell(index)
            return data # Exit the function if successful

        except Exception:
            initialize_board()  # Restart the board on error
    else:
        raise ValueError("Sudoku generation failed: Maximum attempts reached.")


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

def run_multiple_tests(test_runs=1000):
    """Runs multiple tests to evaluate Sudoku generation and tracks performance."""
    worked = 0
    wrong = 0
    times = []

    for _ in range(test_runs):
        try:
            start = time.process_time()
            sudoku()
            worked += 1
            times.append(time.process_time() - start)
        except Exception:
            wrong += 1

    avg_time = sum(times) / len(times) if times else 0
    print(f"\nTests run: {test_runs}\nSuccessful: {worked}\nFailed: {wrong}\nMax time: {max(times):.4f} seconds\nAverage time: {avg_time:.4f} seconds\n")

def measure_performance(times):
    """Measures the performance of the Sudoku generator for different iterations."""
    results = []

    for count in times:
        start = time.process_time()
        for _ in range(count):
            sudoku()
        results.append(time.process_time() - start)
        print(f"{count}: {results[-1]:.4f} s")

    return results


def plot_results(times, results):
    """Plots the performance results."""
    f, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].plot(times, results, color='green', marker='o', markersize=5, linestyle='dashed', linewidth=2)
    axs[0].set_title('Linear Scale')
    axs[0].set_xlabel('Number of Iterations')
    axs[0].set_ylabel('Time (s)')
    axs[0].grid()

    axs[1].loglog(times, results, color='blue', marker='o', markersize=5, linewidth=2)
    axs[1].set_title('Log-Log Scale')
    axs[1].set_xlabel('Number of Iterations (log)')
    axs[1].set_ylabel('Time (log)')
    axs[1].grid()

    plt.tight_layout()
    plt.show()


# os.system("cls" if os.name == "nt" else "clear")

# # Execution
# start_time = time.process_time()
# sudoku()
# end_time = time.process_time() - start_time
# print(f"\nExecution time: {end_time:.5f} seconds\n")

# # Draw the Sudoku board
# draw("value")

# # Check the Sudoku board
# super_check()

# Testing
# run_multiple_tests(test_runs=1000)

# iteration_counts = [1, 50, 100, 300, 500, 700, 1000]
# performance_results = measure_performance(iteration_counts)
# plot_results(iteration_counts, performance_results)