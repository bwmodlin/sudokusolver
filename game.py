import random

from utilities import generate_sudoku_board, is_possible
import sys, pygame as pg
import time
from simulatedannealing import run_annealing
from backtracking import backtracking_solve


class game:
    def __init__(self, type, board=None):
        pg.init()

        self.screen_size = 750, 750
        self.screen = pg.display.set_mode(self.screen_size)
        self.font = pg.font.SysFont(None, 40)
        self.board = board
        if self.board is None:
            self.board = generate_sudoku_board(9, 60)
        pg.display.flip()

        self.start_game(type)


    def draw_background(self):
        self.screen.fill(pg.Color("white"))
        pg.draw.rect(self.screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
        i = 1
        while (i * 80) < 720:
            line_width = 5 if i % 3 > 0 else 10
            pg.draw.line(self.screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735),
                         line_width)
            pg.draw.line(self.screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15),
                         line_width)
            i += 1

    def draw_numbers(self):
        for row in range(len(self.board)):
            offset = 46
            for column in range(len(self.board[row])):
                output = self.board[row][column]
                n_text = self.font.render(str(output), True, pg.Color('black'))
                self.screen.blit(n_text, pg.Vector2((column * 80) + offset, (row * 80) + offset))

    def color_square(self, r, c):
        for row in range(len(self.board)):
            offset = 46
            for column in range(len(self.board[row])):

                output = self.board[row][column]
                n_text = self.font.render(str(output), True, pg.Color('black'))
                if row == r and column == c:
                    pg.draw.circle(self.screen, pg.Color("orange"), (pg.Vector2((column * 80) + 55, (row * 80) + 55)),
                                   30)
                self.screen.blit(n_text, pg.Vector2((column * 80) + offset, (row * 80) + offset))

    def start_game(self, type):
        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
        if type == "annealing":
            run_annealing(self.board, display=True, game=self)
        else:
            backtracking_solve(self.board, display=True, game=self)

    def new_board(self, row=None, col=None, annealing=False):
        self.draw_background()
        self.draw_numbers()
        # Highlights the current selected cell

        if annealing:
            self.color_square(row[0], col[0])
            self.color_square(row[1], col[1])
        else:
            self.color_square(row, col)

        pg.display.flip()
        time.sleep(0.04)
