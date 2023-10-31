import pygame
import sys
import copy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")

# Sudoku puzzle grid (0 represents an empty cell)
sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

# Create a copy of the original board
original_board = copy.deepcopy(sudoku_grid)

# Track the active cell
active_cell = (0, 0)

# Function to draw the Sudoku grid
def draw_grid():
    for i in range(GRID_SIZE + 1):
        line_width = 3 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_width)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_width)

# Function to draw the Sudoku numbers on the grid
def draw_numbers():
    font = pygame.font.Font(None, 36)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if sudoku_grid[i][j] != 0:
                text = font.render(str(sudoku_grid[i][j]), True, BLACK)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

def reset_board():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if original_board[i][j] != 0:
                sudoku_grid[i][j] = original_board[i][j]
            else:
                sudoku_grid[i][j] = 0


# Function to solve the Sudoku puzzle using backtracking
def solve_sudoku():
    def is_valid(num, row, col):
        for i in range(GRID_SIZE):
            if sudoku_grid[row][i] == num or sudoku_grid[i][col] == num:
                return False
        subgrid_row, subgrid_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if sudoku_grid[subgrid_row + i][subgrid_col + j] == num:
                    return False
        return True

    def solve():
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if sudoku_grid[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(num, row, col):
                            sudoku_grid[row][col] = num
                            pygame.event.pump()
                            screen.fill(WHITE)
                            draw_grid()
                            draw_numbers()
                            pygame.draw.rect(screen, GREEN, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
                            pygame.display.flip()
                            pygame.time.delay(100)
                            if solve():
                                return True
                            sudoku_grid[row][col] = 0
                    return False
        return True

    solve()

# Function to handle user input
def handle_input(event):
    if original_board[active_cell[0]][active_cell[1]] == 0 and event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
        num = int(event.unicode)
        sudoku_grid[active_cell[0]][active_cell[1]] = num

# Main loop
running = True
is_solving = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and active_cell[1] > 0:
                active_cell = (active_cell[0], active_cell[1] - 1)
            elif event.key == pygame.K_RIGHT and active_cell[1] < GRID_SIZE - 1:
                active_cell = (active_cell[0], active_cell[1] + 1)
            elif event.key == pygame.K_UP and active_cell[0] > 0:
                active_cell = (active_cell[0] - 1, active_cell[1])
            elif event.key == pygame.K_DOWN and active_cell[0] < GRID_SIZE - 1:
                active_cell = (active_cell[0] + 1, active_cell[1])
            if event.key == pygame.K_s:
                reset_board()
                is_solving = not is_solving
            else:
                handle_input(event)

    screen.fill(WHITE)
    draw_grid()
    draw_numbers()
    pygame.draw.rect(screen, GREEN, (active_cell[1] * CELL_SIZE, active_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)
    pygame.display.flip()

    if is_solving:
        solve_sudoku()

pygame.quit()
sys.exit()
