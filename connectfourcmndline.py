import numpy as np

ROW_COUNT = 6
COLOUMN_COUNT = 7
TURN = 0

def create_board():
    board =np.zeros((ROW_COUNT,COLOUMN_COUNT))
    return board

def drop_piece(board,row,col,piece):
    board[row][col] = piece

def is_valid_location(board , col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board ,col):

    for r in range(ROW_COUNT):

        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board,0))

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

board = create_board()
print_board(board)
game_over= False

while not game_over :
    ##ASK PLAYER 1 INPUT
    if TURN == 0:
        
        while True:

            col = input("Player 1 Make Your Selection (0-6): ")
            try:
                col=int(col)
                if col > COLOUMN_COUNT-1:
                    print("INVALID INPUT")
                    continue
                break
            except:
                print('INVALID INPUT')

        if is_valid_location(board,col):
            row=get_next_open_row(board ,col)
            drop_piece(board ,row,col,1)

            if winning_move(board,1):
                print('Player 1 Wins')
                game_over=True
                break

        
         
    ##ASK PLAYER 2 INPUT
    else:
        
        while True:

            col = input("Player 2 Make Your Selection (0-6): ")
            try:
                col=int(col)
                if col > COLOUMN_COUNT-1:
                    print("INVALID INPUT")
                    continue
                break
            except:
                print('INVALID INPUT')

        if is_valid_location(board,col):
            row=get_next_open_row(board ,col)
            drop_piece(board ,row,col,2)

            if winning_move(board,2):
                print('Player 2 Wins')
                game_over=True
                break
    print_board(board)
    TURN +=1
    TURN %= 2 