# Pygame template - skeleton for a new pygrame project

import pygame
import constant as c
from game.game import Game

## draw the board
def draw_board():
    global screen
    screen.fill(c.WHITE)
    pygame.draw.rect(screen, c.WOOD, (0,0,c.HEIGHT,c.HEIGHT))
    ## draw horizontal lines
    pos = c.EDGE
    y_start = c.EDGE
    y_end = c.HEIGHT-c.EDGE
    for i in range(c.SIZE):
        pygame.draw.line(screen, c.BLACK, (pos, y_start), (pos, y_end), c.THICK)
        pos += c.SPACE
    ## draw vertical lines
    pos = c.EDGE
    x_start = c.EDGE
    x_end = c.HEIGHT-c.EDGE
    for i in range(c.SIZE):
        pygame.draw.line(screen, c.BLACK, (x_start, pos), (x_end, pos), c.THICK)
        pos += c.SPACE
    ## draw 9 dots
    if c.SIZE == 15:
        start_pos = int(round(c.EDGE + 1*c.SPACE))+c.THICK//2
    elif c.SIZE == 17:
        start_pos = int(round(c.EDGE + 2*c.SPACE))+c.THICK//2
    elif c.SIZE == 19:
        start_pos = int(round(c.EDGE + 3*c.SPACE))+c.THICK//2
    else:
        print("UNSUPPORTED SIZE")
        exit()
    x = start_pos
    for i in range(3):
        y = start_pos
        for j in range(3):
            pygame.draw.circle(screen, c.BLACK, (x, y), c.DOT_SIZE)
            y+= int(round(6*c.SPACE))
        x+= int(round(6*c.SPACE))

def draw_stones():
    global screen, game
    board = game.board
    for i in range(c.SIZE):
        x = int(round(c.EDGE+ i*c.SPACE))+c.THICK//2
        for j in range(c.SIZE):
            y = int(round(c.EDGE+ j*c.SPACE))+c.THICK//2
            if board[i,j] == c.BLACK_P:
                pygame.draw.circle(screen, c.BLACK, (x, y), c.STONE_SIZE)
            elif board[i,j] == c.WHITE_P:
                pygame.draw.circle(screen, c.WHITE, (x, y), c.STONE_SIZE)

## get mouse click on the board
def get_board_pos(x):
    if x < c.HEIGHT:
        x = (x-c.EDGE)/c.SPACE
        if abs(x-round(x)) < c.ROUND_ERR:
            return int(round(x))
    return -1

## show message on screen
def show_msg(text,pos,color):
    global screen
    font = c.FONT
    msg_surf = font.render(text, True, color)
    msg_rect = msg_surf.get_rect()
    msg_rect.center = pos
    screen.blit(msg_surf, msg_rect)

def draw_button():
    global screen, game
    WIDTH, HEIGHT = c.WIDTH, c.HEIGHT
    DIFF = WIDTH-HEIGHT
    msgs = game.get_msg()
    for i,(msg, color) in enumerate(msgs):
        pygame.draw.rect(screen, c.WOOD, (DIFF//4+HEIGHT, (2+i)*HEIGHT//10, DIFF//2, HEIGHT//20))
        show_msg(msg, (DIFF//2+HEIGHT, (2.25+i)*HEIGHT//10), color)

def draw_extra_msg(msg=None):
    global screen, game
    WIDTH, HEIGHT = c.WIDTH, c.HEIGHT
    DIFF = WIDTH-HEIGHT

    if msg is not None:
        show_msg(msg, (DIFF//2+HEIGHT, 6.25*HEIGHT//10), c.GRAY)

    # else show win msg:
    else:
        if game.finish == 1:
            show_msg("BLACK WINS !", (DIFF//2+HEIGHT, 6.25*HEIGHT//10), c.GRAY)
        elif game.finish == -1:
            show_msg("WHITE WINS !", (DIFF//2+HEIGHT, 6.25*HEIGHT//10), c.GRAY)

def get_button(x, y):
    WIDTH, HEIGHT = c.WIDTH, c.HEIGHT
    DIFF = WIDTH-HEIGHT
    if x>(DIFF//4+HEIGHT) and x<(3*DIFF//4+HEIGHT):
        if y>(2*HEIGHT//10) and y<(2.5*HEIGHT//10):
            return 1 # button 1
        elif y>(3*HEIGHT//10) and y<(3.5*HEIGHT//10):
            return 2 # button 2
        elif y>(4*HEIGHT//10) and y<(4.5*HEIGHT//10):
            return 3 # button 3
        elif y>(5*HEIGHT//10) and y<(5.5*HEIGHT//10):
            return 4 # button 4
        else:
            return 0
    else:
        return 0

# initialize the game
pygame.init()
pygame.mixer.init()

# initialize the screen
screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("Five-in-a-Row")

# used to set up frame rate
clock = pygame.time.Clock()

# game loop
running = True
game = Game()
move_illegal = False
while running:
    # process input (events) - nothing but closing window
    for event in pygame.event.get():
        # check for closing window:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            x,y = pygame.mouse.get_pos()
            board_x = get_board_pos(x)
            board_y = get_board_pos(y)
            if board_x!=-1 and board_y!=-1 and game.mode!=0:
                move_illegal = game.move((board_x, board_y))

            # if clicked a button
            button = get_button(x,y)
            game.get_button(button)

    # draw
    draw_board()
    draw_stones()
    draw_button()
    if move_illegal: draw_extra_msg("Illegal Move !")
    else: draw_extra_msg()

    # after drawing everything, flip the display
    pygame.display.flip()

    # set the FPS right
    clock.tick(c.FPS)

pygame.quit()
