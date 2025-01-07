# Sudoku Solver and Generator

This project is a Python implementation of a Sudoku generator and solver. It provides functionality to create complete Sudoku boards, generate puzzles with gaps, and visualize the solutions and possible values for cells.

## Features

- Sudoku Board Generation: Generates a complete, valid Sudoku board using recursive backtracking.

- Puzzle Generation: Creates a Sudoku puzzle with a specified number of gaps.

- Possibilities Display: Displays the possible values for empty cells based on Sudoku rules.

- Customizable Board Visualization: Supports printing the board in different modes (e.g., solution, gaps, or possibilities).

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
### Generate and Solve a Sudoku Puzzle
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
### Clear the Console
```python
Sudoku.clear_screen()
```
## Class Methods

### Initialization

- `Sudoku(gaps: int)`: Creates a Sudoku instance with a specified number of gaps.

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

### Utility

- `clear_screen()`: Clears the console screen.

## Requirements

Python 3.7+

## Example Output

### Puzzle with Gaps

 X   X   X  |  6   5   1  |  X   X   X    
 7   X   X  |  X   X   8  |  X   X   X    
 X   9   6  |  X   2   4  |  X   X   X    
— — — — — — + — — — — — — + — — — — — —    
 9   X   X  |  4   7   X  |  X   X   6    
 6   X   X  |  9   1   X  |  X   X   X    
 X   7   4  |  X   X   5  |  X   X   X    
— — — — — — + — — — — — — + — — — — — —    
 X   3   X  |  5   X   X  |  6   X   X    
 X   6   7  |  X   8   9  |  X   3   4    
 X   8   X  |  1   X   6  |  X   X   X    

### Complete Solution

 8   2   3  |  6   5   1  |  7   4   9    
 7   4   1  |  3   9   8  |  2   6   5    
 5   9   6  |  7   2   4  |  3   1   8    
— — — — — — + — — — — — — + — — — — — —    
 9   1   2  |  4   7   3  |  8   5   6    
 6   5   8  |  9   1   2  |  4   7   3    
 3   7   4  |  8   6   5  |  1   9   2    
— — — — — — + — — — — — — + — — — — — —    
 2   3   9  |  5   4   7  |  6   8   1    
 1   6   7  |  2   8   9  |  5   3   4    
 4   8   5  |  1   3   6  |  9   2   7    

## License

This project is licensed under the MIT License.