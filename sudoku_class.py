import random
import copy
import os

class Sudoku:
    def __init__(self, level: str, gaps: int):
        """
        Initialize the Sudoku class.
        
        Parameters:
            gaps (int): Number of empty cells (gaps) in the Sudoku board.
        """
        self.__board_metadata = {}
        self.__num_gaps = gaps
        self.__complete_board = self.__generate_complete_board()
        self.__board_with_gaps = self.__apply_gaps(self.__complete_board, self.__num_gaps)
        self.__update_possibilities()

    def __initialize_metadata(self):
        """Create metadata for each cell in the Sudoku board."""
        for i in range(81):
            self.__board_metadata[i] = {
                "index": i,
                "col": i % 9,
                "row": i // 9,
                "value": 0,
                "box": (i // 9 // 3) * 3 + (i % 9) // 3,
                "possibilities": [1, 2, 3, 4, 5, 6, 7, 8, 9],
                "state": "ready",
            }

    def __update_constraints(self, row: int, col: int, box: int, number: int):
        """Update possible values for cells in the same row, column, or box."""
        for i in range(81):
            if number in self.__board_metadata[i]["possibilities"] and (
                self.__board_metadata[i]["row"] == row
                or self.__board_metadata[i]["col"] == col
                or self.__board_metadata[i]["box"] == box
            ):
                self.__board_metadata[i]["possibilities"].remove(number)

    def __update_possibilities(self):
        """Update possible values for empty cells based on Sudoku rules."""
        for i in range(9):
            # Update rows
            row_start = i * 9
            checked_values = [
                self.__board_with_gaps[row_start + j]["value"]
                for j in range(9)
                if self.__board_with_gaps[row_start + j]["state"] == "checked"
            ]
            for j in range(9):
                cell = self.__board_with_gaps[row_start + j]
                if cell["state"] == "empty":
                    cell["possibilities"] = [p for p in cell["possibilities"] if p not in checked_values]

            # Update columns
            checked_values = [
                self.__board_with_gaps[j * 9 + i]["value"]
                for j in range(9)
                if self.__board_with_gaps[j * 9 + i]["state"] == "checked"
            ]
            for j in range(9):
                cell = self.__board_with_gaps[j * 9 + i]
                if cell["state"] == "empty":
                    cell["possibilities"] = [p for p in cell["possibilities"] if p not in checked_values]

            # Update boxes
            box_start = (i // 3) * 27 + (i % 3) * 3
            box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]
            checked_values = [
                self.__board_with_gaps[idx]["value"]
                for idx in box_indices
                if self.__board_with_gaps[idx]["state"] == "checked"
            ]
            for idx in box_indices:
                cell = self.__board_with_gaps[idx]
                if cell["state"] == "empty":
                    cell["possibilities"] = [p for p in cell["possibilities"] if p not in checked_values]

    def __fill_cell(self, index: int):
        """Fill a cell if it has only one possible value."""
        cell = self.__board_metadata[index]
        if len(cell["possibilities"]) == 1 and cell["state"] == "ready":
            number = cell["possibilities"].pop()
            cell["value"] = number
            cell["state"] = "checked"
            self.__update_constraints(cell["row"], cell["col"], cell["box"], number)

    def __generate_complete_board(self):
        """Generate a complete Sudoku board."""
        self.__initialize_metadata()
        for _ in range(10_000):
            try:
                for index in range(81):
                    if self.__board_metadata[index]["state"] == "ready":
                        number = random.choice(self.__board_metadata[index]["possibilities"])
                        self.__board_metadata[index]["value"] = number
                        self.__board_metadata[index]["state"] = "checked"
                        self.__update_constraints(
                            self.__board_metadata[index]["row"],
                            self.__board_metadata[index]["col"],
                            self.__board_metadata[index]["box"],
                            number,
                        )

                for index in range(81):
                    self.__fill_cell(index)
                return self.__board_metadata  # Return if successful

            except Exception:
                self.__initialize_metadata()  # Restart on error
        else:
            raise ValueError("Sudoku generation failed after maximum attempts.")

    def __apply_gaps(self, board, num_gaps):
        """Mark a specified number of cells as empty."""
        board_copy = copy.deepcopy(board)

        while num_gaps > 0:
            indices = random.sample(range(81), k=num_gaps)
            for i in indices:
                if board_copy[i]["state"] != "empty":
                    board_copy[i]["state"] = "empty"
                    board_copy[i]["possibilities"] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                    num_gaps -= 1
                    if num_gaps == 0:
                        break
        return board_copy

    def __draw_board(self, attribute, data):
        """Print the Sudoku board."""
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
        """Display the possible values for empty cells."""
        output = ""
        for r in range(9):
            row = []
            for c in range(9):
                cell = data[c + 9 * r]
                if cell["state"] == "empty":
                    cell_value = str(cell["possibilities"]).replace(" ", "")
                else:
                    cell_value = "[]"
                row.append(cell_value.center(9))
            output += (
                " | ".join([" ".join(row[i : i + 3]) for i in range(0, 9, 3)]) + "\n"
            )
            if r % 3 == 2 and r != 8:
                output += "— — — — — — — — — — — — — — — + — — — — — — — — — — — — — — — + — — — — — — — — — — — — — — —\n"

        print(output)

    def print_board(self, mode: str):
        """Print the board based on the mode (gaps, solution, or possibilities)."""
        if mode == "gaps":
            self.__draw_board("value", self.__board_with_gaps)
        elif mode == "solution":
            self.__draw_board("value", self.__complete_board)
        elif mode == "possibilities":
            self.__draw_possibilities(self.__board_with_gaps)
        else:
            raise ValueError("Invalid mode. Use 'gaps', 'solution', or 'possibilities'.")

    def get_board_gaps(self, dimension="one"):
        """Return the Sudoku board with gaps in specified dimension (1D or 2D)."""
        flat_list = [
            "X" if cell["state"] == "empty" else cell["value"]
            for cell in self.__board_with_gaps.values()
        ]
        if dimension in ("one", "1"):
            return flat_list
        elif dimension in ("two", "2", "multiple"):
            return [flat_list[i : i + 9] for i in range(0, len(flat_list), 9)]
        else:
            raise ValueError("Invalid dimension. Use 'one' or 'two'.")

    def get_board_solution(self, dimension="one"):
        """Return the complete Sudoku solution in specified dimension (1D or 2D)."""
        flat_list = [cell["value"] for cell in self.__complete_board.values()]
        if dimension in ("one", "1"):
            return flat_list
        elif dimension in ("two", "2", "multiple"):
            return [flat_list[i : i + 9] for i in range(0, len(flat_list), 9)]
        else:
            raise ValueError("Invalid dimension. Use 'one' or 'two'.")

    @staticmethod
    def clear_screen():
        """Clear the console screen."""
        os.system("cls" if os.name == "nt" else "clear")

