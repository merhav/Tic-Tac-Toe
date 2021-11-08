import pygame as pg, sys
from pygame.locals import *
import time

XO = 'x'
winner = None
draw = False
fps = 30
windth = 400
height = 400
white = (255,255,255)
line_color = (10,10,10)

TTT = [[None]*3,[None]*3,[None]*3]

# init the pygame window
pg.init()
Clock = pg.time.Clock()
screen = pg.display.set_mode((windth,height+100),0,32)
pg.display.set_caption("Tic Tac Toe")

# loading the image
opening = pg.image.load('images/marble-tic-tac-toe-set.jpg')
x_image = pg.image.load('images/X.png')
o_image = pg.image.load('images/O.png')

# resizing
opening = pg.transform.scale(opening, (windth,height+100))
x_image = pg.transform.scale(x_image, (80,80))
o_image = pg.transform.scale(o_image, (80,80))


def draw_status():
    global draw
    if winner is None:
        message = XO.upper() + "'s Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = 'Game end in Draw'

    font = pg.font.Font(None,30)
    text = font.render(message,1,(255,255,255))

    screen.fill((0, 0, 0), (0, 400, 500, 100))
    text_rect = text.get_rect(center=(windth/2,450))
    screen.blit(text,text_rect)
    pg.display.update()


def game_opening():
    screen.blit(opening,(0,0))
    pg.display.update()
    time.sleep(1)
    screen.fill(white)

    #draw vertical line
    pg.draw.line(screen, line_color, (windth/3,0), (windth/3,height),7)
    pg.draw.line(screen, line_color, (windth/3*2, 0), (windth/3*2, height), 7)
    # draw horizontal line
    pg.draw.line(screen, line_color, (0,windth / 3), (height,windth / 3), 7)
    pg.draw.line(screen, line_color, (0,windth / 3 * 2), (height,windth / 3 * 2), 7)
    # pg.display.update()
    draw_status()


def drawXO(row, col):
    global TTT,XO
    if row==1:
        posx = 30
    if row==2:
        posx = windth/3 +30
    if row ==3:
        posx = windth/3*2 +30

    if col==1:
        posy = 30
    if col==2:
        posy= height/3+30
    if col==3:
        posy = height/3*2+30

    TTT[row-1][col-1] = XO
    if(XO =='x'):
        screen.blit(x_image, (posy,posx))
        XO = 'o'
    else:
        screen.blit(o_image, (posy, posx))
        XO = 'x'
    pg.display.update()


def check_win():
    global TTT, winner, draw
    #check the rows
    for row in range(0,3):
        if(( TTT[row][0] == TTT[row][1] == TTT[row][2]) and( TTT[row][0] is not None)):
            winner = TTT[row][0]
            pg.draw.line(screen, (250,0,0), (0,(row+1)*height/3 - height/6), (windth, (row + 1)*height/3 - height/6 ), 4)
            break
    # check the cols
    for col in range(0,3):
        if ((TTT[0][col] == TTT[1][col] == TTT[2][col]) and (TTT[0][col] is not None)):
            winner = TTT[0][col]
            pg.draw.line(screen, (250, 0, 0), ((col + 1) * windth / 3 - windth / 6,0),
                         ((col + 1) * windth / 3 - windth / 6,height), 4)
            break

    #check diaganols
    if((TTT[0][0] == TTT[1][1] == TTT[2][2] and TTT[0][0] is not None)):
        winner = TTT[0][0]
        pg.draw.line(screen, (250, 70  , 70), (50, 50),
                     (350, 350), 4)
    if ((TTT[0][2] == TTT[1][1] == TTT[2][0] and TTT[0][2] is not None)):
        winner = TTT[0][2]
        pg.draw.line(screen, (250, 70, 70), (350, 50),
                     (50, 350), 4)
    if(all([all(row) for row in TTT]) and winner is None):
        draw=True
    draw_status()


def userClick():
    # get cordinates
    x,y = pg.mouse.get_pos()

    # get col
    if x<windth/3:
        col=1;
    elif x<windth/3*2:
        col=2
    elif x<windth:
        col=3
    else:
        col=None

#     get row
    if y<height/3:
        row=1
    elif y<height/3*2:
        row=2
    elif y<height:
        row=3
    else:
        row=None

    if (row and col and TTT[row - 1][col - 1] is None):
        global XO
        # draw the x or o on screen
        drawXO(row, col)
        check_win()


def reset_game():
    global TTT, winner, XO, draw
    time.sleep(3)
    XO= 'x'
    draw = False
    game_opening()
    winner = None
    TTT = [[None]*3,[None]*3,[None]*3]

game_opening()

while(True):
    for event in pg.event.get():
        if event.type ==QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            userClick()
            if winner or draw:
                reset_game()
                draw_status()

    pg.display.update()
    Clock.tick(fps)

