import pygame

# define display constants
WIDTH = 1000
HEIGHT = 800
FPS = 20

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (128,128,128)
RED = (255,0,0)
GREEN = (0,255,0)
WOOD = (193,154,107)

# define board
SIZE = 17
EDGE = 0.03 * HEIGHT
SPACE = (HEIGHT - 2*EDGE)/(SIZE-1)
THICK = 2
DOT_SIZE = 5
STONE_SIZE = 15

# define mouse click
ROUND_ERR = 0.25

# define text size
pygame.font.init()
FONT = pygame.font.Font('freesansbold.ttf', HEIGHT//40)

# define game constants
BLACK_P = 1
WHITE_P = -1
