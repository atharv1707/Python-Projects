
class Solution:
    def isSafe(self, row, col, board, k):
        # Verifying each step function
        for i in range(9):
            # Checking the row
            if board[row][i] == k:
                return False
            # Checking the column
            if board[i][col] == k:
                return False
            
            if board[3*(row//3) + i//3][3*(col//3) + i%3] == k:
                return False
                # Grid not safe

        # Checking the 3x3 grid inside the Sudoku board

        return True

    def solve(self, board):
        # Solving function
        n = len(board)

        for i in range(n):
            for j in range(n):
                if board[i][j] == '.':
                    for k in map(str, range(1, 10)):
                        if self.isSafe(i, j, board, k):
                            board[i][j] = k

                            if self.solve(board):
                                return True
                            else:
                                # Backtrack because a solution is not possible
                                board[i][j] = '.'

                    return False

        return True

# Example usage:
# Initialize a Sudoku board as a list of lists (9x9 grid) with '.' for empty cells.
sudoku_board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]

solver = Solution()
solver.solve(sudoku_board)

# Print the solved Sudoku board
for row in sudoku_board:
    print(" ".join(row))
