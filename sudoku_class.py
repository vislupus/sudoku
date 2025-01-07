import os
import random
import time
import copy


class Sudoku:

    def __init__(self, gaps: int):
        self.__board_data = {}
        self.__gaps = gaps
        self.__sudoku_board = self.__sudoku_board()
        self.__sudoku_board_gaps = self.__create_gaps(self.__sudoku_board, self.__gaps)
        self.__remove_pos()

    def __initialize_board(self):
        """Initializes an empty Sudoku board with metadata."""
        for i in range(81):
            self.__board_data[i] = {
                "index": i,
                "col": i % 9,
                "row": i // 9,
                "value": 0,
                "box": (i // 9 // 3) * 3 + (i % 9) // 3,
                "pos": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "state": "ready",
            }

    def __remove_other(self, row: int, col: int, box: int, number: int):
        """Removes the possibility of a given number in the row, column, and box."""
        for i in range(81):
            if number in self.__board_data[i]["pos"] and (
                self.__board_data[i]["row"] == row
                or self.__board_data[i]["col"] == col
                or self.__board_data[i]["box"] == box
            ):
                self.__board_data[i]["pos"].remove(number)

    def __remove_pos(self):
        """Removes invalid possibilities from empty cells based on Sudoku rules."""
        # Rows
        for i in range(9):
            row_start = i * 9
            checked_values = [
                self.__sudoku_board_gaps[row_start + j]["value"]
                for j in range(9)
                if self.__sudoku_board_gaps[row_start + j]["state"] == "checked"
            ]
            for j in range(9):
                cell = self.__sudoku_board_gaps[row_start + j]
                if cell["state"] == "empty":
                    cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

        # Columns
        for i in range(9):
            checked_values = [
                self.__sudoku_board_gaps[j * 9 + i]["value"]
                for j in range(9)
                if self.__sudoku_board_gaps[j * 9 + i]["state"] == "checked"
            ]
            for j in range(9):
                cell = self.__sudoku_board_gaps[j * 9 + i]
                if cell["state"] == "empty":
                    cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

        # Boxes
        for i in range(9):
            box_start = (i // 3) * 27 + (i % 3) * 3
            box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]
            checked_values = [
                self.__sudoku_board_gaps[idx]["value"]
                for idx in box_indices
                if self.__sudoku_board_gaps[idx]["state"] == "checked"
            ]
            for idx in box_indices:
                cell = self.__sudoku_board_gaps[idx]
                if cell["state"] == "empty":
                    cell["pos"] = [p for p in cell["pos"] if p not in checked_values]

    def __fill_cell(self, index: int):
        """Fills a cell with a value if there is only one possibility."""
        if (
            len(self.__board_data[index]["pos"]) == 1
            and self.__board_data[index]["state"] == "ready"
        ):
            number = self.__board_data[index]["pos"].pop()
            self.__board_data[index]["value"] = number
            self.__board_data[index]["state"] = "checked"
            self.__remove_other(
                self.__board_data[index]["row"],
                self.__board_data[index]["col"],
                self.__board_data[index]["box"],
                number,
            )

    def __sudoku_board(self):
        """Generates a Sudoku board by randomly filling values."""
        self.__initialize_board()
        for _ in range(10_000):  # Attempts up to 10 000 times to avoid deadlocks
            try:
                for index in range(81):
                    if self.__board_data[index]["state"] == "ready":
                        number = random.choice(self.__board_data[index]["pos"])
                        self.__board_data[index]["value"] = number
                        self.__board_data[index]["state"] = "checked"
                        self.__remove_other(
                            self.__board_data[index]["row"],
                            self.__board_data[index]["col"],
                            self.__board_data[index]["box"],
                            number,
                        )

                for index in range(81):
                    self.__fill_cell(index)
                return self.__board_data  # Exit the function if successful

            except Exception:
                self.__initialize_board()  # Restart the board on error
        else:
            raise ValueError("Sudoku generation failed: Maximum attempts reached.")

    def __create_gaps(self, data, n):
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

    def __draw_board(self, attribute, data):
        """Displays the Sudoku board on the screen with enhanced formatting."""
        output = ""
        for r in range(9):
            row = []
            for c in range(9):
                cell_value = (
                    "X"
                    if data[c + 9 * r]["state"] == "empty"
                    else f"{data[c + 9 * r][attribute]}"
                )
                row.append(cell_value.center(3))
            output += (
                " | ".join([" ".join(row[i : i + 3]) for i in range(0, 9, 3)]) + "\n"
            )
            if r % 3 == 2 and r != 8:
                output += "— — — — — — + — — — — — — + — — — — — —\n"

        print(output)

    def __draw_possibilities(self, data):
        """Displays the Sudoku board with possible values for empty cells."""
        output = ""
        for r in range(9):
            row = []
            for c in range(9):
                cell = data[c + 9 * r]
                if cell["state"] == "empty":
                    cell_value = str(cell["pos"]).replace(
                        " ", ""
                    )  # Remove spaces for compact display
                else:
                    cell_value = "[]"
                row.append(cell_value.center(9))
            output += (
                " | ".join([" ".join(row[i : i + 3]) for i in range(0, 9, 3)]) + "\n"
            )
            if r % 3 == 2 and r != 8:
                output += "— — — — — — — — — — — — — — — + — — — — — — — — — — — — — — — + — — — — — — — — — — — — — — —\n"

        print(output)

    def print_board(self, attribute):
        if attribute == "gaps":
            self.__draw_board("value", self.__sudoku_board_gaps)
        elif attribute == "solution":
            self.__draw_board("value", self.__sudoku_board)
        elif attribute == "possibilities":
            self.__draw_possibilities(self.__sudoku_board_gaps)

    def board_gaps(self, dimension="one"):
        lst = ["X" if val['state'] == 'empty' else val['value'] for _, val in self.__sudoku_board_gaps.items()]
        if dimension == "one" or dimension == "1":
            return lst
        if dimension == "two" or dimension == "2" or dimension == "multiple":
            return [lst[i:i + 9] for i in range(0, len(lst), 9)]
        
    def board_solution(self, dimension="one"):
        lst = [val['value'] for _, val in self.__sudoku_board.items()]
        if dimension == "one" or dimension == "1":
            return lst
        if dimension == "two" or dimension == "2" or dimension == "multiple":
            return [lst[i:i + 9] for i in range(0, len(lst), 9)]

    @staticmethod
    def clear_screen():
        """
        Clear the console screen.

        Use the "cls" command on Windows and "clear" on Unix/Linux/MacOS.
        """
        os.system("cls" if os.name == "nt" else "clear")


Sudoku.clear_screen()
sudoku = Sudoku(50)
sudoku.print_board("solution")
# sudoku.print_board("gaps")
# sudoku.print_board("possibilities")
# print(sudoku.board_gaps())
# for row in sudoku.board_gaps("two"):
#     print(row)
print(sudoku.board_solution())
for row in sudoku.board_solution("two"):
    print(row)
