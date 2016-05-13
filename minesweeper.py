import random
from enum import Enum
import re
def get_neighbors(i, j, n):
    # def within_bounds(row, col):
    #     return (row,col) != (i,j) and row >= 0 and row < n and col >= 0 and col < n
    neighbors = []
    for row in range(i-1, i+2, 1):
        for col in range(j-1, j+2, 1):
            if (row,col) != (i,j) and row >= 0 and row < n and col >= 0 and col < n:
                neighbors.append((row,col))
    return neighbors

class MinesweeperStates(Enum):
    new_game = 1
    in_progress = 2
    game_lost = 3
    game_won = 4

class Cell(object):
    def __init__(self, x, y, state, n):
        self.x = x
        self.y = y
        self.state = state
        self.num_adjacent_mines = n

    def __repr__(self):
        return "({},{}), state: {}, n: {}".format(self.x,self.y, self.state, self.num_adjacent_mines)

class Minesweeper(object):
    grid_repr = {'empty': '◼', 'uncovered': '.', 'marked': 'M', 'covered': '_', 'armed': '*'}
    def compute_mine_adjacency(self):
        for mine in self.mines:
            for cell in get_neighbors(mine[0], mine[1], len(self.board)):
                self.board[cell[0]][cell[1]]['adjacent_mines'] = self.board[cell[0]][cell[1]]['adjacent_mines'] + 1

    def __init__(self, dim, number_of_mines):
        self.num_rows = dim
        self.num_cols = dim
        self._state = MinesweeperStates.new_game
        # print(self._state)
        self.mines = set([])
        self.board = [ [] for d in range(dim)]
        for r in self.board:
            for i in range(dim):
                r.append({'state': 'covered', 'adjacent_mines': 0, 'is_armed': False})
        self._num_of_mines = number_of_mines
        random.seed()
        for m in range(number_of_mines):
            x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
            while (x,y) in self.mines:
                x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
            self.mines.add((x,y))
            # self.board[x][y]['state'] = 'armed'
            self.board[x][y]['is_armed'] = True
        self.flags = set([])
        self.remaining_flags = number_of_mines
        self._number_of_empty_cells = (dim * dim) - len(self.mines)
        self.compute_mine_adjacency()

    def new_game(self):
        self._state = MinesweeperStates.new_game
        for row in self.board:
            # print (row)
            for cell in row:
                # print(cell)
                cell['state'] = 'covered'
                cell['adjacent_mines'] = 0
                cell['is_armed'] = False
        random.seed()
        self.mines.clear()
        for m in range(self._num_of_mines):
            x,y = (random.randint(0,self.num_rows-1),random.randint(0,self.num_cols-1))
            while (x,y) in self.mines:
                x,y = (random.randint(0,self.num_rows-1),random.randint(0,self.num_cols-1))
            self.mines.add((x,y))
            # self.board[x][y]['state'] = 'armed'
            self.board[x][y]['is_armed'] = True
        self.flags.clear()
        self.remaining_flags = self._num_of_mines
        self._number_of_empty_cells = (self.num_rows * self.num_cols) - len(self.mines)
        self.compute_mine_adjacency()

    def get_num_rows(self):
       return self.num_rows

    def get_num_cols(self):
        return self.num_cols

    def _render_cell(self, cell):
        if self._state is MinesweeperStates.new_game:
            return '◼'
        elif self._state is MinesweeperStates.in_progress:
            if cell['state'] == 'covered':
                return '◼'
            elif cell['state'] == 'uncovered':
                if cell['adjacent_mines'] > 0:
                    return str(cell['adjacent_mines']) # show number of adjacent mines
                else:
                    return '.'
            else: # then cell['state'] == 'marked'
                return 'M'
        elif self._state is MinesweeperStates.game_lost:
            if cell['state'] == 'marked':
                if cell['is_armed'] is False:
                    return '%'
                else:
                    return 'M'
            elif cell['state'] == 'uncovered' and cell['is_armed']:
                return '@'
            elif cell['is_armed'] and cell['state'] == 'covered':
                return '*'
            else:
                if cell['adjacent_mines'] > 0:
                    return str(cell['adjacent_mines']) # show number of adjacent mines
                else:
                    return 'X'
                return 'u'
        else:
            return Minesweeper.grid_repr[cell['state']]
    def is_game_over(self):
        return self._state == MinesweeperStates.game_lost or self._state == MinesweeperStates.game_won

    def show(self):
        print ("  " + "".join([' {} '.format(i) for i in range(len(self.board))]))

        for row, row_number in zip(self.board, range(len(self.board))):
            print("{} ".format(row_number) + "".join([' {} '.format(self._render_cell(cell)) for cell in row]))

        print (self._state, "\nNumber of remaining empty cells: {}\nNumber of remaining flags: {}".format(self._number_of_empty_cells, self.remaining_flags))


    def _are_all_mines_flagged(self):
        return len(self.mines - self.flags) is 0

    def mark_cell(self, x, y):
        # update cell.state
        if self._state is MinesweeperStates.new_game:
            self._state = MinesweeperStates.in_progress

        cell_state = self.board[y][x]['state']
        if cell_state == 'marked':
            self.board[y][x]['state'] = 'covered'
            self.remaining_flags = self.remaining_flags + 1
            self.flags.remove((y,x))
        elif cell_state == 'covered':
            if self.remaining_flags == 0:
                # print('No more flags, unflag some other cell')
                return
            self.board[y][x]['state'] = 'marked'
            # update remaining flags
            self.remaining_flags = self.remaining_flags - 1
            self.flags.add((y,x))
            if self._are_all_mines_flagged():
                self._state = MinesweeperStates.game_won
        else:
            print('Error: cannot mark or unmark an empty cell.')


    def uncover_cell(self, x, y):
        if self._state == MinesweeperStates.new_game:
            self._state = MinesweeperStates.in_progress
        if self.board[y][x]['is_armed'] == False:
            self.board[y][x]['state'] = 'uncovered'
            self._number_of_empty_cells = self._number_of_empty_cells - 1
            self.uncover_empty_neighbors(y,x)
            if self._number_of_empty_cells == 0:
                self._state = MinesweeperStates.game_won
        else:
            self.board[y][x]['state'] = 'uncovered'
            self._state = MinesweeperStates.game_lost

    def uncover_empty_neighbors(self, i, j):
        for r,c in get_neighbors(i,j, len(self.board)):
            if self.board[r][c]['is_armed']:
                return
            if self.board[r][c]['is_armed'] == False and self.board[r][c]['state'] == 'covered':
                self.board[r][c]['state'] = 'uncovered'
                self._number_of_empty_cells = self._number_of_empty_cells - 1
                self.uncover_empty_neighbors(r,c)

    def get_results(self):
        return {'outcome' : self._state.name, 'remaining_flags' : self.remaining_flags, 'number_of_empty_cells' : self._number_of_empty_cells}

    def get_board(self):
        # return [[ (cell['state'], cell['adjacent_mines']) for cell in row] for row in self.board]
        return [[ Cell(x,y,cell['state'], cell['adjacent_mines']) for cell, x in zip(row, range(len(row)))] for row, y in zip(self.board, range(len(self.board)))]

# Trying to verify that adjacent empty cells are being uncovered correctly
class MinesweeperGenerationalUncover(Minesweeper):
    def __init__(self, dim, number_of_mines):
        Minesweeper.__init__(self, dim, number_of_mines)

    def uncover_empty_neighbors(self, i, j, depth=1):
        if depth == 0:
            return
        for r,c in get_neighbors(i,j, len(self.board)):
            if self.board[r][c]['state'] == 'empty':
                self.board[r][c]['state'] = 'uncovered'
                self.uncover_empty_neighbors(r,c, depth-1)

def test1(dim = 7, num_mines = 10):
    preamble ='''-------------------------------------------------------------------------------
|   New Game                                                                   |
-------------------------------------------------------------------------------
'''
    print(preamble)
    mine = Minesweeper(dim, num_mines)
    for i in range(dim*dim):
        x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
        print ("Move #{} at cell({},{})".format(i+1,x,y))
        mine.uncover_cell(y,x)
        mine.show()
        if mine.is_game_over():
            return


def test2(dim = 7, num_mines = 10):
    preamble ='''-------------------------------------------------------------------------------
|   New Game                                                                   |
-------------------------------------------------------------------------------
'''
    print(preamble)
    mine = Minesweeper(dim, num_mines)
    for j in range(num_mines):
        x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
        print ("Mark #{} at cell({},{})".format(j+1,x,y))
        mine.mark_cell(y,x)
        mine.show()
    for i in range(dim*dim):
        x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
        print ("Move #{} at cell({},{})".format(i+1,x,y))
        mine.uncover_cell(y,x)
        mine.show()
        if mine.is_game_over():
            return


def main():
    num_of_mines = 10
    board_dimension = 10
    game = Minesweeper(board_dimension, num_of_mines)
    user_action = None
    two_digit_pattern = re.compile(r'(\d+)\s+(\d+)')
    game.show()
    while not game.is_game_over():
        print("Please enter a column number(x coord) and row number(y coord) for the cell you would like to act upon:")
        cell_str = input()
        cell_input_match = two_digit_pattern.match(cell_str)
        while cell_input_match is None:
            print('Try again: enter a cell coordinate as two integers between 0 and {}:'.format(board_dimension-1))
            cell_str = input()
            cell_input_match = two_digit_pattern.match(cell_str)
        [col_number, row_number] = map(int, cell_input_match.groups())
        print("What action would you like to perform on cell {} , {}? (m)ark or (u)ncover:".format(col_number, row_number))
        action = input()
        if action[0].lower() == 'm':
            game.mark_cell(col_number, row_number)
        else:
            game.uncover_cell(col_number, row_number)
        game.show()


if __name__ == '__main__':
    main()
