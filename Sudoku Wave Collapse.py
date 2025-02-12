from random import randint
from math import floor

# n by n size
n = 9

board = [[] for y in range(n)]

class pallette:
    def __init__(self, value, options): # Options are stored in nested lists going U-R-D-L
        self.value = value
        self.up_options = options[0]
        self.right_options = options[1]
        self.down_options = options[2]
        self.left_options = options[3]

class tile:
    def __init__(self):
        self.options = {str(x) for x in range(1, n+1)}
        r = 0
        while len(board[r]) == n:
            r += 1

        self.x, self.y = r, len(board[r]) # x is row and y is column - we can find it by board[x][y]
        board[r].append(self)
        

    def collapse(self, choice):

        self.options = {choice}

        for i in range(9):
            if i != self.y and choice in board[self.x][i].options:
                board[self.x][i].options.remove(choice)
                # If collapsed to singular value, then collapse this cell
                if len(board[self.x][i].options) == 1:
                    board[self.x][i].collapse(list(board[self.x][i].options)[0])
            if i != self.x and choice in board[i][self.y].options:
                board[i][self.y].options.remove(choice)
                if len(board[i][self.y].options) == 1:
                    board[i][self.y].collapse(list(board[i][self.y].options)[0])

        chunk_x = floor(self.x / (n**0.5))
        chunk_y = floor(self.y / (n**0.5))
        
        for i in range(int(n**0.5)):
            for j in range(int(n**0.5)):
                if (chunk_x*int(n**0.5) + i != self.x or chunk_y*int(n**0.5) + j != self.y) and choice in board[chunk_x*int(n**0.5) + i][chunk_y*int(n**0.5) + j].options:
                        board[chunk_x*int(n**0.5) + i][chunk_y*int(n**0.5) + j].options.remove(choice)
                        if len(board[chunk_x*int(n**0.5) + i][chunk_y*int(n**0.5) + j].options) == 1:
                            board[chunk_x*int(n**0.5) + i][chunk_y*int(n**0.5) + j].collapse(list(board[chunk_x*int(n**0.5) + i][chunk_y*int(n**0.5) + j].options)[0])





def show_board():
    print('-'*(n*4+1))
    for row in range((n*2-1)):
        if row % 2 == 0:
            for col in range((n*4+1)):
                if col % 4 == 2:
                    print(list(board[row//2][col//4].options)[0], end='')
                elif col % int((n**0.5)*4) == 0:
                    print('|', end='')
                else:
                    print(' ', end='')

            
        elif row % int((n**0.5)*2) == (n**0.5)*2-1:
            for col in range((n*4+1)):
                print('-', end='')

        else:
            print(('|'+' '*int((n**0.5)*4-1))*int(n**0.5)+'|', end='')

        print('\n', end='')

    print('-'*(n*4+1))

def lowest_entropy():
    entropies = []
    for row in board:
        r = []
        for t in row:
            if len(t.options) > 1:
                r.append(len(t.options))
        if len(r) > 0:
            entropies.append(min(r))

    choices = []
    for row in board:
        for t in row:
            if len(t.options) == min(entropies):
                choices.append(t)

    return choices[randint(0, len(choices) - 1)]
    



for i in range(int(n*n)):
    tile()

board[randint(0, 8)][randint(0, 8)].collapse('1')

while True:
    try:
        choice = lowest_entropy()
        choice.collapse(list(choice.options)[randint(0, len(choice.options)-1)])
    except:
        break

show_board()
