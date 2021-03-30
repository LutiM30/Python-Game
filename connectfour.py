##IMPORTING NECCESARRAY Libraries
import numpy as np
import pygame as pg
import sys,math
##Initializing PyGame and Giving Name to WINDOW
pg.init()
pg.display.set_caption('Connect 4 by Mitul')
##DEFINING GLOBAL VARIABLES
ROW_COUNT = 6
COLOUMN_COUNT = 7
TURN = 0
BLUE=(0,0,255)
BLACK=(0,0,0)
RED=(255,0,0)
YELLOW=(255,255,0)
SQUARE=100
RADIUS= int(SQUARE/2 - 5)
WIDTH = COLOUMN_COUNT*SQUARE
HEIGHT = (ROW_COUNT+1)*SQUARE

size = (WIDTH,HEIGHT)

##creating screen as per size
screen = pg.display.set_mode(size)

##creating numerical board
def create_board():
    board =np.zeros((ROW_COUNT,COLOUMN_COUNT))
    return board

##In which row,coloumn the next input will be
def drop_piece(board,row,col,piece):
    board[row][col] = piece

## CHECKING IF THE ROW IS FILLEDUP OR NOT
def is_valid_location(board , col):
    return board[ROW_COUNT-1][col] == 0

#Getting Next Open Row which have Zero
def get_next_open_row(board ,col):

    for r in range(ROW_COUNT):

        if board[r][col] == 0:
            return r

##INITIALLY X AXIS AND Y AXIX ARE TOP DOWN WITH NUMPY FLIP I FLIPPED THAT
def print_board(board):
    print(np.flip(board,0))

## CHECKING FOR 4
def winning_move(board,piece):
    ##Check Horizontal Location For Win
    for c in range(COLOUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    ##Check Vertical Location For Win

    for c in range(COLOUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    ##Check Positively Sloped Diagonal
    for c in range(COLOUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
         
    ##Check Negatively Sloped Diagonal
    for c in range(COLOUMN_COUNT-3):
        for r in range(3,ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

##FILLING SCREEN WITH COLORS
def draw_board(board):
    
    ##CANVAS
    for c in range(COLOUMN_COUNT):
        
        for r in range(ROW_COUNT):
            
            #BLUE Rectangle WITH BLACK HOLES
            pg.draw.rect(screen,BLUE,(c*SQUARE,r*SQUARE+SQUARE,SQUARE,SQUARE))
            pg.draw.circle(screen,BLACK,(int(c*SQUARE+SQUARE/2),int(r*SQUARE+SQUARE+SQUARE/2)),RADIUS)
    
    ## PLAYER 1 and 2's DIFFERENT CIRCLES
    for c in range(COLOUMN_COUNT):
    
        for r in range(ROW_COUNT):
    
            if board[r][c] ==1:
                pg.draw.circle(screen,RED,(int(c*SQUARE+SQUARE/2),HEIGHT-int(r*SQUARE+SQUARE/2)),RADIUS)
    
            elif board[r][c] ==2:
                pg.draw.circle(screen,YELLOW,(int(c*SQUARE+SQUARE/2),HEIGHT-int(r*SQUARE+SQUARE/2)),RADIUS)
    
    #UPDATING SCREEN
    pg.display.update()

        
#NUMERICAL MATRIX
board = create_board()
draw_board(board)

#UPDATING DISPLAY 1st TIME
pg.display.update()

#PRINTing MATRIX for 1st TIME which have all ZEROES
print_board(board)
game_over= False
myfont = pg.font.SysFont('monospace',75)

#MAIN GAME LOGIC
while not game_over :
    ##ASK PLAYER 1 INPUT

    for event in pg.event.get():
        #WHEN the moving circle on top black bar it creates white rectangle as circle moves over
        pg.draw.rect(screen,BLACK,(0,0,WIDTH,SQUARE))
        
        ##WHEN SOMEONE CLOSES THE WINDOW It exits SAFELY
        if event.type == pg.QUIT:
            sys.exit()
        
        ##Circle on top moves as mouse pointer goes using X axis motion
        if event.type == pg.MOUSEMOTION:
            posx  = event.pos[0]
        
        ##CHANGING The COLOR OF CIRCLE as per Player's TURN
            if TURN == 0:
                pg.draw.circle(screen,RED,(posx,int(SQUARE/2)),RADIUS)
        
            else:
                pg.draw.circle(screen,YELLOW,(posx,int(SQUARE/2)),RADIUS)
        
        ##UPDATING SCREEN
        pg.display.update()
        
        ##GETTING INPUT AND DRAWING BLACK RECTANGLE ON DISPLAY BOARD
        if event.type == pg.MOUSEBUTTONDOWN:
            pg.draw.rect(screen,BLACK,(0,0,WIDTH,SQUARE))
            
            ## ASK PLAYER 1 INPUT
            if TURN == 0:
                
                #GETTING CURRENT MOUSE Location AND EVENT AND PUTTING CIRCLES ACCORDING TO IT
                posx  = event.pos[0]
                col = int(math.floor(posx/SQUARE))
                
                # FIRST CHECKING IF ROW IS FULL OR NOT IF IT IS FULL IT WILL NOT DO OTHER OPERATIONS
                if is_valid_location(board,col):
                    ## GETTING THE LAST POSITION OF PARTICULAR COLUMN
                    row=get_next_open_row(board ,col)
                    drop_piece(board ,row,col,1)
                    ## PRINTING MESSAGE AS PER PLAYER WIN
                    if winning_move(board,1):
                        print('Player 1 Wins')
                        label=myfont.render('Player 1 Wins!',1,RED)
                        screen.blit(label,(40,10))
                        game_over=True
                        
            ##ASK PLAYER 2 INPUT
            else:
                
                posx  = event.pos[0]
                col = int(math.floor(posx/SQUARE))
                
                if is_valid_location(board,col):
                    row=get_next_open_row(board ,col)
                    drop_piece(board ,row,col,2)

                    if winning_move(board,2):
                        print('Player 2 Wins')
                    
                        label=myfont.render('Player 2 Wins!',1,YELLOW)
                        screen.blit(label,(40,10))
                        game_over=True
                        game_over=True
                        
            #PRINTING THE LAST BOARD AND GENERATING NEW BOARD AS PER LATEST INPUT
            print_board(board)
            draw_board(board)
            ##CHANGING TURN B/W PLAYER ONE AND TWO
            TURN +=1
            ##WHEN TURN OF PLAYER TWO COMPLETES TURN WILL BE 3 AND REMAINDER OF TURN DIVIDED BY 2 WILL BE 1 SO TURN WILL BE 1 AGAIN
            TURN %= 2

            #AFTER GAME OVER WINDOW WILL CLOSE AFTER 3 SECs OF DELAY
            if game_over==True:
                pg.time.wait(3000)