# importing the required libraries
from Board import Board
import pygame as pg
import sys
sys.path.append(".")
pg.font.init()

WHITE = (255, 255, 255)


def redraw_window(win, board):
    win.fill(WHITE)
    board.draw(win)


def main():
    win = pg.display.set_mode((540, 540))
    pg.display.set_caption("TicTacToe")
    board = Board(3, 3, 540, 540)
    key = "X"
    run = True
    XO = "X"

    while run:

        for event in pg.event.get():

            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != None:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Fail")

                        if board.has_won():
                            print(key + " Wins!")
                            run = False

                        if board.is_finished():
                            print("Game Over")
                            run = False
                if XO == "X":
                    XO = "O"
                    key = "O"
                else:
                    XO = "X"
                    key = "X"

            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board)
        pg.display.update()


main()
pg.quit()
