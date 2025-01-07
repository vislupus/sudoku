# Sudoku Solver and Generator

This project is a Python implementation of a Sudoku generator and solver. It provides functionality to create complete Sudoku boards, generate puzzles with gaps, and visualize the solutions and possible values for cells.

## Features

- Sudoku Board Generation: Generates a complete, valid Sudoku board using recursive backtracking.

- Puzzle Generation: Creates a Sudoku puzzle with a specified number of gaps.

- Possibilities Display: Displays the possible values for empty cells based on Sudoku rules.

- Customizable Board Visualization: Supports printing the board in different modes (e.g., solution, gaps, or possibilities).

- Custom Board Solving: Allows solving puzzles provided as a 1D list of 81 elements.

## Installation

1. Clone this repository:
```
git clone https://github.com/vislupus/sudoku.git
```
2. Navigate to the project directory:
```
cd sudoku
```
3. Ensure you have Python 3.7+ installed.

## Usage

### Import the Class
```python
from sudoku import Sudoku
```
### Generate a Sudoku Puzzle
```python
# Create a Sudoku instance with 30 gaps
sudoku = Sudoku(gaps=30)

# Print the board with gaps
sudoku.print_board(mode="gaps")

# Print the complete solution
sudoku.print_board(mode="solution")

# Print the possibilities for each cell
sudoku.print_board(mode="possibilities")
```
### Retrieve the Board as a List
```python
# Get the board with gaps as a 1D list
board_gaps = sudoku.get_board_gaps(dimension="one")

# Get the complete solution as a 2D list
board_solution = sudoku.get_board_solution(dimension="two")
```
### Solving Sudoku Puzzle
```python
# Example puzzle with empty cells as 'X'
puzzle = [
    5, 3, 'X', 'X', 7, 'X', 'X', 'X', 'X',
    6, 'X', 'X', 1, 9, 5, 'X', 'X', 'X',
    'X', 9, 8, 'X', 'X', 'X', 'X', 6, 'X',
    8, 'X', 'X', 'X', 6, 'X', 'X', 'X', 3,
    4, 'X', 'X', 8, 'X', 3, 'X', 'X', 1,
    7, 'X', 'X', 'X', 2, 'X', 'X', 'X', 6,
    'X', 6, 'X', 'X', 'X', 'X', 2, 8, 'X',
    'X', 'X', 'X', 4, 1, 9, 'X', 'X', 5,
    'X', 'X', 'X', 'X', 8, 'X', 'X', 7, 9,
]

solver = SudokuSolver()

# Solve the puzzle
solution = solver.solve_sudoku_board(puzzle)
```

### Clear the Console
```python
Sudoku.clear_screen()
```

## Class Methods

### Initialization

- `Sudoku(gaps: int)`: Creates a Sudoku instance with a specified number of gaps.

- `SudokuSolver()`: Creates a SudokuSolver instance.

### Board Display

- `print_board(mode: str)`: Prints the Sudoku board. Modes:

    - `"gaps"`: Displays the puzzle with gaps.

    - `"solution"`: Displays the complete solution.

    - `"possibilities"`: Displays the possible values for each empty cell.

### Board Retrieval

- `get_board_gaps(dimension="one")`: Returns the puzzle with gaps as a list.

    - `dimension="one"`: 1D list.

    - `dimension="two"`: 2D list.

- `get_board_solution(dimension="one")`: Returns the complete solution as a list.

    - `dimension="one"`: 1D list.

    - `dimension="two"`: 2D list.
  
### Solving Board

- `solve_sudoku_board(puzzle)`: 
  - **Input**: Accepts a 1D list of 81 elements, where numbers represent filled cells and 'X'  represent empty cells.
  - **Output**: Returns the complete solution as a 1D list if the puzzle is solvable. If the puzzle doesn't have a unique solution, returns a message indicating this.


### Utility

- `clear_screen()`: Clears the console screen.

## License

This project is licensed under the MIT License.