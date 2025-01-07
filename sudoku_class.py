import random
import copy
import os


class Sudoku:
    """Sudoku class for generating Sudoku puzzles."""

    def __init__(self, gaps: int):
        """
        Initialize the Sudoku class.

        Parameters:
            gaps (int): Number of empty cells (gaps) in the Sudoku board.
        """
        self.__board_metadata = {}
        self.__num_gaps = gaps
        self.__complete_board = self.__generate_complete_board()
        self.__board_with_gaps = self.__apply_gaps(
            self.__complete_board, self.__num_gaps
        )
        self._update_possibilities(self.__board_with_gaps)

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

    @staticmethod
    def _update_possibilities(data):
        """Update possible values for empty cells based on Sudoku rules."""
        for i in range(9):
            # Update rows
            row_start = i * 9
            checked_values = [
                data[row_start + j]["value"]
                for j in range(9)
                if data[row_start + j]["state"] == "checked"
            ]
            for j in range(9):
                cell = data[row_start + j]
                if cell["state"] == "empty":
                    cell["possibilities"] = [
                        p for p in cell["possibilities"] if p not in checked_values
                    ]

            # Update columns
            checked_values = [
                data[j * 9 + i]["value"]
                for j in range(9)
                if data[j * 9 + i]["state"] == "checked"
            ]
            for j in range(9):
                cell = data[j * 9 + i]
                if cell["state"] == "empty":
                    cell["possibilities"] = [
                        p for p in cell["possibilities"] if p not in checked_values
                    ]

            # Update boxes
            box_start = (i // 3) * 27 + (i % 3) * 3
            box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]
            checked_values = [
                data[idx]["value"]
                for idx in box_indices
                if data[idx]["state"] == "checked"
            ]
            for idx in box_indices:
                cell = data[idx]
                if cell["state"] == "empty":
                    cell["possibilities"] = [
                        p for p in cell["possibilities"] if p not in checked_values
                    ]

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
                        number = random.choice(
                            self.__board_metadata[index]["possibilities"]
                        )
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
            raise ValueError(
                "Invalid mode. Use 'gaps', 'solution', or 'possibilities'."
            )

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

class SudokuSolver:
    """Sudoku class for solving Sudoku puzzles."""

    @staticmethod
    def __convert_list_to_metadata(board_list):
        """
        Converts a 1D list of Sudoku values into a metadata dictionary.

        Parameters:
            board_list (list): A list of 81 values representing the Sudoku board.
                            Use 'X' or None for empty cells.

        Returns:
            dict: A dictionary containing metadata for each cell.
        """
        if len(board_list) != 81:
            raise ValueError("Input list must contain exactly 81 elements.")

        metadata = {}
        for i, value in enumerate(board_list):
            metadata[i] = {
                "index": i,
                "col": i % 9,
                "row": i // 9,
                "value": 0 if value == "X" or value is None else value,
                "box": (i // 9 // 3) * 3 + (i % 9) // 3,
                "possibilities": (
                    []
                    if value != "X" and value is not None
                    else [1, 2, 3, 4, 5, 6, 7, 8, 9]
                ),
                "state": "checked" if value != "X" and value is not None else "empty",
            }
        return metadata

    def __remove_value_from_related_cells(self, row, column, box, number):
        """Removes a value from possibilities in related rows, columns, and boxes."""
        for i in range(81):
            if number in self.__board_metadata_solver[i]["possibilities"]:
                if (
                    self.__board_metadata_solver[i]["row"] == row
                    or self.__board_metadata_solver[i]["col"] == column
                    or self.__board_metadata_solver[i]["box"] == box
                ):
                    self.__board_metadata_solver[i]["possibilities"].remove(number)

    def __process_unique_possibilities_in_box(self):
        """Finds and processes cells with unique possibilities within boxes."""
        for k in range(9):
            obj = {i: {"value": 0, "possibilities": []} for i in range(1, 10)}
            box_start = (k // 3) * 27 + (k % 3) * 3
            box_indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

            for idx in box_indices:
                for i in range(1, 10):
                    if i in self.__board_metadata_solver[idx]["possibilities"]:
                        obj[i]["value"] += 1
                        obj[i]["possibilities"].append(idx)

            for i in range(1, 10):
                if obj[i]["value"] == 1:
                    unique_idx = obj[i]["possibilities"][0]
                    self.__board_metadata_solver[unique_idx]["value_new"] = i
                    self.__board_metadata_solver[unique_idx]["possibilities"] = []
                    self.__remove_value_from_related_cells(
                        self.__board_metadata_solver[unique_idx]["row"],
                        self.__board_metadata_solver[unique_idx]["col"],
                        self.__board_metadata_solver[unique_idx]["box"],
                        i,
                    )

    def __process_unique_possibilities_in_row(self):
        """Finds and processes cells with unique possibilities within rows."""
        for r in range(9):
            obj = {i: {"value": 0, "possibilities": []} for i in range(1, 10)}
            row_start = r * 9
            for i in range(9):
                for n in range(1, 10):
                    if (
                        n
                        in self.__board_metadata_solver[row_start + i]["possibilities"]
                    ):
                        obj[n]["value"] += 1
                        obj[n]["possibilities"].append(row_start + i)

            for n in range(1, 10):
                if obj[n]["value"] == 1:
                    unique_idx = obj[n]["possibilities"][0]
                    self.__board_metadata_solver[unique_idx]["value_new"] = n
                    self.__board_metadata_solver[unique_idx]["possibilities"] = []
                    self.__remove_value_from_related_cells(
                        self.__board_metadata_solver[unique_idx]["row"],
                        self.__board_metadata_solver[unique_idx]["col"],
                        self.__board_metadata_solver[unique_idx]["box"],
                        n,
                    )

    def __process_unique_possibilities_in_column(self):
        """Finds and processes cells with unique possibilities within columns."""
        for c in range(9):
            obj = {i: {"value": 0, "possibilities": []} for i in range(1, 10)}
            for r in range(9):
                idx = r * 9 + c
                for n in range(1, 10):
                    if n in self.__board_metadata_solver[idx]["possibilities"]:
                        obj[n]["value"] += 1
                        obj[n]["possibilities"].append(idx)

            for n in range(1, 10):
                if obj[n]["value"] == 1:
                    unique_idx = obj[n]["possibilities"][0]
                    self.__board_metadata_solver[unique_idx]["value_new"] = n
                    self.__board_metadata_solver[unique_idx]["possibilities"] = []
                    self.__remove_value_from_related_cells(
                        self.__board_metadata_solver[unique_idx]["row"],
                        self.__board_metadata_solver[unique_idx]["col"],
                        self.__board_metadata_solver[unique_idx]["box"],
                        n,
                    )

    def __process_naked_pairs(self):
        """Identifies and processes naked pairs in rows, columns, and boxes."""
        for group_type in ["row", "col", "box"]:
            for i in range(9):
                candidates = []
                if group_type == "row":
                    indices = [i * 9 + j for j in range(9)]
                elif group_type == "col":
                    indices = [j * 9 + i for j in range(9)]
                else:
                    box_start = (i // 3) * 27 + (i % 3) * 3
                    indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

                for idx in indices:
                    if len(self.__board_metadata_solver[idx]["possibilities"]) == 2:
                        candidates.append(
                            (
                                idx,
                                set(self.__board_metadata_solver[idx]["possibilities"]),
                            )
                        )

                for idx1, pair1 in candidates:
                    for idx2, pair2 in candidates:
                        if idx1 != idx2 and pair1 == pair2:
                            for idx in indices:
                                if (
                                    idx != idx1
                                    and idx != idx2
                                    and len(
                                        self.__board_metadata_solver[idx][
                                            "possibilities"
                                        ]
                                    )
                                    > 0
                                ):
                                    self.__board_metadata_solver[idx][
                                        "possibilities"
                                    ] = [
                                        n
                                        for n in self.__board_metadata_solver[idx][
                                            "possibilities"
                                        ]
                                        if n not in pair1
                                    ]

    def __process_naked_pairs(self):
        """Identifies and processes hidden pairs in rows, columns, and boxes."""
        for group_type in ["row", "col", "box"]:
            for i in range(9):
                if group_type == "row":
                    indices = [i * 9 + j for j in range(9)]
                elif group_type == "col":
                    indices = [j * 9 + i for j in range(9)]
                else:
                    box_start = (i // 3) * 27 + (i % 3) * 3
                    indices = [box_start + (j // 3) * 9 + (j % 3) for j in range(9)]

                occurrences = {n: [] for n in range(1, 10)}
                for idx in indices:
                    for n in self.__board_metadata_solver[idx]["possibilities"]:
                        occurrences[n].append(idx)

                for pair in [(x, y) for x in range(1, 10) for y in range(x + 1, 10)]:
                    if len(set(occurrences[pair[0]] + occurrences[pair[1]])) == 2:
                        shared_indices = set(
                            occurrences[pair[0]] + occurrences[pair[1]]
                        )
                        for idx in shared_indices:
                            self.__board_metadata_solver[idx]["possibilities"] = [
                                n
                                for n in self.__board_metadata_solver[idx][
                                    "possibilities"
                                ]
                                if n in pair
                            ]

    def __process_x_wing(self):
        """Identifies and processes X-Wing patterns in rows and columns."""
        for digit in range(1, 10):
            # Check rows
            row_positions = []
            for r in range(9):
                positions = [
                    c
                    for c in range(9)
                    if digit in self.__board_metadata_solver[r * 9 + c]["possibilities"]
                ]
                if len(positions) == 2:
                    row_positions.append((r, positions))

            for (r1, p1), (r2, p2) in [
                (x, y) for x in row_positions for y in row_positions if x != y
            ]:
                if p1 == p2:
                    for c in p1:
                        for r in range(9):
                            if (
                                r != r1
                                and r != r2
                                and digit
                                in self.__board_metadata_solver[r * 9 + c][
                                    "possibilities"
                                ]
                            ):
                                self.__board_metadata_solver[r * 9 + c][
                                    "possibilities"
                                ].remove(digit)

            # Check columns
            col_positions = []
            for c in range(9):
                positions = [
                    r
                    for r in range(9)
                    if digit in self.__board_metadata_solver[r * 9 + c]["possibilities"]
                ]
                if len(positions) == 2:
                    col_positions.append((c, positions))

            for (c1, p1), (c2, p2) in [
                (x, y) for x in col_positions for y in col_positions if x != y
            ]:
                if p1 == p2:
                    for r in p1:
                        for c in range(9):
                            if (
                                c != c1
                                and c != c2
                                and digit
                                in self.__board_metadata_solver[r * 9 + c][
                                    "possibilities"
                                ]
                            ):
                                self.__board_metadata_solver[r * 9 + c][
                                    "possibilities"
                                ].remove(digit)

    def __process_swordfish(self):
        """Identifies and processes Swordfish patterns in rows and columns."""
        for digit in range(1, 10):
            # Check rows
            row_candidates = {
                r: [
                    c
                    for c in range(9)
                    if digit in self.__board_metadata_solver[r * 9 + c]["possibilities"]
                ]
                for r in range(9)
            }
            rows_with_candidates = [
                r for r, cols in row_candidates.items() if 2 <= len(cols) <= 3
            ]

            for r1, r2, r3 in [
                (x, y, z)
                for x in rows_with_candidates
                for y in rows_with_candidates
                for z in rows_with_candidates
                if x < y < z
            ]:
                common_cols = (
                    set(row_candidates[r1])
                    & set(row_candidates[r2])
                    & set(row_candidates[r3])
                )
                if len(common_cols) == 3:
                    for r in range(9):
                        if r not in [r1, r2, r3]:
                            for c in common_cols:
                                if (
                                    digit
                                    in self.__board_metadata_solver[r * 9 + c][
                                        "possibilities"
                                    ]
                                ):
                                    self.__board_metadata_solver[r * 9 + c][
                                        "possibilities"
                                    ].remove(digit)

            # Check columns
            col_candidates = {
                c: [
                    r
                    for r in range(9)
                    if digit in self.__board_metadata_solver[r * 9 + c]["possibilities"]
                ]
                for c in range(9)
            }
            cols_with_candidates = [
                c for c, rows in col_candidates.items() if 2 <= len(rows) <= 3
            ]

            for c1, c2, c3 in [
                (x, y, z)
                for x in cols_with_candidates
                for y in cols_with_candidates
                for z in cols_with_candidates
                if x < y < z
            ]:
                common_rows = (
                    set(col_candidates[c1])
                    & set(col_candidates[c2])
                    & set(col_candidates[c3])
                )
                if len(common_rows) == 3:
                    for c in range(9):
                        if c not in [c1, c2, c3]:
                            for r in common_rows:
                                if (
                                    digit
                                    in self.__board_metadata_solver[r * 9 + c][
                                        "possibilities"
                                    ]
                                ):
                                    self.__board_metadata_solver[r * 9 + c][
                                        "possibilities"
                                    ].remove(digit)

    def __check_new_value(self):
        """Checks for cells with a single possibility and resolves them."""
        progress = False
        for i in range(81):
            if (
                len(self.__board_metadata_solver[i]["possibilities"]) == 1
                and self.__board_metadata_solver[i]["state"] == "empty"
            ):
                value = self.__board_metadata_solver[i]["possibilities"].pop()
                self.__board_metadata_solver[i]["value_new"] = value
                self.__remove_value_from_related_cells(
                    self.__board_metadata_solver[i]["row"],
                    self.__board_metadata_solver[i]["col"],
                    self.__board_metadata_solver[i]["box"],
                    value,
                )
                progress = True
        return not progress

    def __solver(self):
        """Solves the Sudoku puzzle using logical deduction."""
        iterations = 0
        while True:
            self.__process_unique_possibilities_in_box()
            self.__process_unique_possibilities_in_row()
            self.__process_unique_possibilities_in_column()

            self.__process_naked_pairs()
            self.__process_naked_pairs()
            self.__process_swordfish()
            self.__process_x_wing()

            if self.__check_new_value():
                break
            iterations += 1
            if iterations > 50:  # Prevent infinite loops
                break

    def solve_sudoku_board(self, board_list):
        self.__board_metadata_solver = self.__convert_list_to_metadata(board_list)
        Sudoku._update_possibilities(self.__board_metadata_solver)
        self.__solver()

        is_solved = True
        for val in self.__board_metadata_solver.values():
            if val["state"] == "empty" and not val.get("value_new"):
                is_solved = False

        if is_solved:
            board_metadata_solution = copy.deepcopy(self.__board_metadata_solver)
            for val in board_metadata_solution.values():
                if val["state"] == "empty":
                    val["value"] = val["value_new"]
                    val["state"] = "checked"
                    if "value_new" in val:
                        del val["value_new"]
            
            return [cell["value"] for cell in board_metadata_solution.values()]
        else:
            return "This sudoku doesn't have single solution."
