import pygame as pg
import time
pg.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Board:
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.selected = None
        self.cubes = [[Cube(self.board[i][j], i, j, width, height)
                       for j in range(cols)] for i in range(rows)]
        self.model = None

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == None:
            self.cubes[row][col].set(val)
            self.update_model()
            return True
        return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        gap = self.width / 3
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(win, BLACK, (0, i*gap), (self.width, i*gap), thick)
            pg.draw.line(win, BLACK, (i*gap, 0), (i*gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 3
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == None:
                    return False
        return True

    def has_won(self):
        return isWinner(self.model)


class Cube:
    rows = 3
    cols = 3

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = None
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pg.font.SysFont("comicsans", 40)
        gap = self.width / 3
        x = self.col * gap
        y = self.row * gap

        if not(self.value == None):
            text = fnt.render(str(self.value), 1, BLACK)
            win.blit(text, (x + (gap/2 - text.get_width()/2),
                            y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pg.draw.rect(win, RED, (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def isWinner(bo):
    # Winning Column
    for i in range(len(bo)):
        if ((bo[0][i] == bo[1][i] == bo[2][i]) and (bo[0][i] is not None)):
            return True
    # Winning Row
    for i in range(len(bo)):
        if((bo[i][0] == bo[i][1] == bo[i][2]) and (bo[i][0] is not None)):
            return True
    # Diagonal Wins
    if (bo[0][0] == bo[1][1] == bo[2][2] and (bo[0][0] is not None)):
        return True

    if (bo[0][2] == bo[1][1] == bo[2][0]) and (bo[0][2] is not None):
        return True

    return False


def redraw_window(win, board):
    win.fill(WHITE)
    board.draw(win)
