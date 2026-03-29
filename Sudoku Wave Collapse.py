import numpy as np
from typing import Tuple

class Grid:
    """
    This class object contains a sudoku board. The board structure is generated using the wave-collapse algorithm.
    """
    def __init__(self, N:int=9):
        """
        This function initiates the class instance, creating a board with all possible values.

        Args:
            N (int): The side length of the board, defaults to 9. 
        """
        self.N = N

        # Creating the board
        self.board = []
        for y in range(N):
            row = []
            for x in range(N):
                # Options for each cell are stored in sets
                row.append({x+1 for x in range(N)})
            self.board.append(row)
            
    def collapse_one(self, x:int, y:int, choice:int):
        """
        This function collapses one specified cell of the board.

        Args:
            x (int): The column index of the cell to collapse.
            y (int): The row index of the cell to collapse.
            choice (int): The value to collapse the cell to.
        """
        self.board[y][x] = {choice}

        # Remove the choice from the corresponding row and column
        for i in range(self.N):
            if i != y and choice in self.board[i][x]:
                self.board[i][x].remove(choice)
                if len(self.board[i][x]) == 1:
                    # If only one choice left, collapse the cell too
                    self.collapse_one(x, i, list(self.board[i][x])[0])
            if i != x and choice in self.board[y][i]:
                self.board[y][i].remove(choice)
                if len(self.board[y][i]) == 1:
                    # If only one choice left, collapse the cell too
                    self.collapse_one(i, y, list(self.board[y][i])[0])

        # Identify which chunk the cell resides in
        rt_N = int(self.N ** 0.5)
        chunk_x = int(np.floor(x / rt_N))
        chunk_y = int(np.floor(y / rt_N))
        
        # Remove the choice from all cells within the chunk
        for i in range(rt_N):
            for j in range(rt_N):
                x_, y_ = chunk_x*rt_N + i, chunk_y*rt_N + j
                if (x_ != x or y_ != y) and choice in self.board[y_][x_]:
                    self.board[y_][x_].remove(choice)
                    if len(self.board[y_][x_]) == 1:
                        # If only one choice left, collapse the cell too
                        self.collapse_one(x_, y_, list(self.board[y_][x_])[0])

    def lowest_entropy(self) -> Tuple[int, int]:
        """
        This function finds the cell with the lowest entropy (least number of options).

        Returns:
            int: The row index of the identified cell.
            int: The column index of the identified cell.
        """
        x_, y_ = -1, -1
        entropy = self.N

        for y in range(self.N):
            for x in range(self.N):
                if len(self.board[y][x]) < entropy and len(self.board[y][x]) > 1:
                    entropy = len(self.board[y][x])
                    x_, y_ = x, y
        
        return x_, y_
    
    def wave_collapse(self):
        """
        This function performs the full wave-collapse algorithm to reduce the options in each cell of the board to one or less.
        """
        # Collapse an initial cell to begin the process
        self.collapse_one(int(np.random.randint(9)), int(np.random.randint(9)), int(np.random.randint(9))+1)

        # Iteratively find the lowest entropy and collapse the cell
        x, y = self.lowest_entropy()
        while x != -1 and y != -1:
            self.collapse_one(x, y, np.random.choice(list(self.board[y][x])))
            x, y = self.lowest_entropy()

        # Save the final solution so that a puzzle board can be created
        self.solution = self.board.copy()

    def remove_some(self, p:float=0.5):
        """
        This function removes a specified portion of the cells to create a puzzle.

        Args:
            p (float): The portion of the board to remove (between 0 and 1).
        """
        for _ in range(int(p*(self.N**2.0))):
            x, y = int(np.random.randint(self.N)), int(np.random.randint(self.N))
            while self.board[y][x] == set({}):
                x, y = int(np.random.randint(self.N)), int(np.random.randint(self.N))
            self.board[y][x] = set({})

    def show_board(self):
        """
        This function displays the board in the terminal.
        """
        print('-'*(self.N*4+1)) # Boarder
        for row in range(self.N*2 - 1):
            # Every other row shall display values
            if row % 2 == 0:
                for col in range(self.N*4 + 1):
                    # Every four columns shall display values
                    if col % 4 == 2:
                        v = list(self.board[row//2][col//4])
                        v = v[0] if len(v) > 0 else ' '
                        print(v, end='')
                    elif col % int((self.N**0.5) * 4) == 0:
                        print('|', end='')
                    else:
                        print(' ', end='')

                
            elif row % int((self.N**0.5) * 2) == (self.N**0.5) * 2-1:
                for col in range((self.N*4+1)):
                    print('-', end='')

            else:
                print(('|'+' '*int((self.N**0.5) * 4-1)) * int(self.N**0.5) + '|', end='')

            print('\n', end='')

        print('-'*(self.N*4+1))

    def any_empties(self):
        """
        This function identifies whether there are any empty cells in the solution board.
        """
        for row in self.solution:
            for v in row:
                if len(v) == 0:
                    # Empty cell found
                    return True
        
        return False





if __name__ == '__main__':
    board = Grid()
    board.wave_collapse()

    # The wave collapse is not always successful, occasionally leading to empty cells
    while board.any_empties():
        board = Grid()
        board.wave_collapse()

    print('## Solution ##')
    board.show_board()
    board.remove_some()
    print('\n## Puzzle ##')
    board.show_board()
