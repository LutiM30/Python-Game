import pygame
import random

##Initializing Fonts Module
pygame.font.init()

# GLOBALS VARS
S_WIDTH = 800
S_HEIGHT = 700
PLAY_WIDTH = 300  # meaning 300 // 10 = 30 width per block
PLAY_HEIGHT = 600  # meaning 600 // 20 = 30 height per block
BLOCK_SIZE = 30

top_left_x = (S_WIDTH - PLAY_WIDTH) // 2
top_left_y = S_HEIGHT - PLAY_HEIGHT


# SHAPE FORMATS

S = [['.....',
    '.....',
    '..00.',
    '.00..',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '...0.',
    '.....']]

Z = [['.....',
    '.....',
    '.00..',
    '..00.',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '.0...',
    '.....']]

I = [['..0..',
    '..0..',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '0000.',
    '.....',
    '.....',
    '.....']]

O = [['.....',
    '.....',
    '.00..',
    '.00..',
    '.....']]

J = [['.....',
    '.0...',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..00.',
    '..0..',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '...0.',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '.00..',
    '.....']]

L = [['.....',
    '...0.',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..0..',
    '..00.',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '.0...',
    '.....'],
    ['.....',
    '.00..',
    '..0..',
    '..0..',
    '.....']]

T = [['.....',
    '..0..',
    '.000.',
    '.....',
    '.....'],
    ['.....',
    '..0..',
    '..00.',
    '..0..',
    '.....'],
    ['.....',
    '.....',
    '.000.',
    '..0..',
    '.....'],
    ['.....',
    '..0..',
    '.00..',
    '..0..',
    '.....']]

##DEFINING SHAPE NAME AND THEIR COLORS
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


##Creating piece
class Piece(object):
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):
        self.x = column
        self.y = row
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3

##Creating Grid
def create_grid(locked_positions={}):

    ##GIVING GRID COLOR
    grid =[[(0,0,0)for x in range(10)]  for x in range(20)]

    ##SETTING UP LOCKED_POSITIONS AS WELL
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_positions:
                c=locked_positions[(j,i)]
                grid[i][j]=c    
    return grid

##SETTING UP PIECE
def convert_shape_format(shape):
    ##PIECE's POSITIONS
    positions = []

    ##SHAPE.SHAPE means Piece's class method 
    ##Getting list of shape
    format = shape.shape[shape.rotation%len(shape.shape)]
    ##neglating '...' in list of piece and postion of piece is updating as piece going downwards
    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0':
                positions.append((shape.x+j,shape.y+i))
    
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2,pos[1]-4)
    
    return positions

## Getting pos of blocks which are not locked 
def valid_space(shape, grid):
    
    ##if color of block is black then it is valid
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0) ]for i in range(20)]
    accepted_pos=[j for sub in accepted_pos for j in sub]


    formatted=convert_shape_format(shape)


    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1]> -1:
                return False
    return True


def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y<1:
            return True
    return False

def get_shape():
    global shapes, shape_colors
    return Piece(5,0,random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('monospace',size,bold=True)
    label=font.render(text,1,color)

    surface.blit(label, (top_left_x + PLAY_WIDTH/2 - (label.get_width() / 2), top_left_y + PLAY_HEIGHT/2 - label.get_height()/2))

   
def draw_grid(surface, grid):
    sx,sy= top_left_x, top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx,sy+i*BLOCK_SIZE),(sx+PLAY_WIDTH,sy+i*BLOCK_SIZE))
        for j in range(len(grid[i])):
            pygame.draw.line(surface,(128,128,128),(sx+j*BLOCK_SIZE,sy),(sx+j*BLOCK_SIZE,sy+PLAY_HEIGHT))

def clear_rows(grid, locked):
    
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('monospace',30)
    label=font.render('Next Shape',1,(255,255,255))

    sx=top_left_x+PLAY_WIDTH+50
    sy=top_left_y+PLAY_HEIGHT/2-100
    format=shape.shape[shape.rotation%len(shape.shape)]

    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column=='0':
                pygame.draw.rect(surface,shape.color,(sx+j*BLOCK_SIZE,sy+i*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),0)

    surface.blit(label,(sx+10,sy-30))

def draw_window(surface,grid,score=0):
    surface.fill((0,0,0))

    pygame.font.init()
    font = pygame.font.SysFont('monospace',60)
    label=font.render('TETRIS', 1,(255,255,255))
    surface.blit(label, (top_left_x + PLAY_WIDTH / 2 - (label.get_width() / 2), 30))
    
    #CURRENT SCORE
    font = pygame.font.SysFont('monospace',30)
    label=font.render('Score: '+str(score),1,(255,255,255))

    sx=top_left_x+PLAY_WIDTH+50
    sy=top_left_y+PLAY_HEIGHT/2-100
    surface.blit(label,(sx+20,sy+160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface,grid[i][j],(top_left_x+j*BLOCK_SIZE,top_left_y+i*BLOCK_SIZE,BLOCK_SIZE,BLOCK_SIZE),0)

    pygame.draw.rect(surface,(255,0,0),(top_left_x,top_left_y,PLAY_WIDTH,PLAY_HEIGHT),5)

def main(win):
    locked_positions={}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    scores = 0

    while run:
        fall_speed = 0.27

        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        # PIECE FALLING CODE
        if fall_time/1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            scores+=clear_rows(grid, locked_positions)*10

        draw_window(win,grid,scores)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 80, (255,255,255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle('Press any key to begin.', 40, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main(win)
    pygame.quit()

win = pygame.display.set_mode((S_WIDTH,S_HEIGHT))
pygame.display.set_caption('Tetris by Mitul')

main_menu()  # start game
