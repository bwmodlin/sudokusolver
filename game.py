from utilities import generate_sudoku_board, is_possible
import sys, pygame as pg
import time

pg.init()
screen_size = 750, 750
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 40)

board = generate_sudoku_board(9, 100)


def draw_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * 80) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735),
                     line_width)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15),
                     line_width)
        i += 1


def draw_numbers():
    for row in range(len(board)):
        offset = 38
        for column in range(len(board[row])):
            # if board[row][column] == 0:
            #     board[row][column] = ""
            output = board[row][column]
            n_text = font.render(str(output), True, pg.Color('black'))
            screen.blit(n_text, pg.Vector2((column * 80) + offset, (row * 80) + offset))


def backtracking_solve(board):
    draw_background()
    draw_numbers()
    pg.display.flip()
    time.sleep(0.1)

    row = None
    col = None

    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                row = r
                col = c

    # If no empty spots were found, we are done and return True:
    if row is None and col is None:
        return True

    for num in range(1, len(board) + 1):

        if is_possible(board, row, col, num):
            board[row][col] = num

            # Recursively call the solve function again

            if backtracking_solve(board):
                return True

            # If returned false, then the choice was wrong, reset
            board[row][col] = 0

    # Backtrack
    return False


def start_game():
    for event in pg.event.get():
        if event.type == pg.QUIT: sys.exit()
    backtracking_solve(board)


while 1:
    start_game()
