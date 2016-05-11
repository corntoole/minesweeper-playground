import random
from enum import Enum
def get_neighbors(i, j, n):
    def within_bounds(row, col):
        return (row,col) != (i,j) and row >= 0 and row < n and col >= 0 and col < n
    neighbors = []
    for r in range(i-1, i+2, 1):
#         print('r ',r, 'i', i)
        for c in range(j-1, j+2, 1):
#             print('c ', c)
            if within_bounds(r,c):
                neighbors.append((r,c))
    return neighbors

class MinesweeperStates(Enum):
    new_game = 1
    in_progress = 2
    game_lost = 3
    game_won = 4

class Minesweeper(object):
    grid_repr = {'empty': 'X', 'uncovered': '.', 'marked': 'M', 'covered': '_', 'armed': '*'}
    def compute_mine_adjacency(self):
        for mine in self.mines:
            for cell in get_neighbors(mine[0], mine[1], len(self.board)):
                self.board[cell[0]][cell[1]]['adjacent_mines'] = self.board[cell[0]][cell[1]]['adjacent_mines'] + 1

    def __init__(self, dim, number_of_mines):
        self._state = MinesweeperStates.new_game
        print(self._state)
        self.mines = set([])
        self.board = [ [] for d in range(dim)]
        for r in self.board:
            for i in range(dim):
                r.append({'state': 'covered', 'adjacent_mines': 0, 'is_armed': False})
        for m in range(number_of_mines):
            x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
            self.mines.add((x,y))
            # self.board[x][y]['state'] = 'armed'
            self.board[x][y]['is_armed'] = True
        self.flags = []
        self.remaining_flags = number_of_mines
        self.compute_mine_adjacency()

    def _render_cell(self, cell):
        if self._state is MinesweeperStates.new_game:
            return '_'
        elif self._state is MinesweeperStates.in_progress:
            if cell['state'] == 'covered':
                return '_'
            elif cell['state'] == 'uncovered':
                if cell['adjacent_mines'] > 0:
                    return str(cell['adjacent_mines']) # show number of adjacent mines
                else:
                    return 'X'
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
    def is_game_over(self):
        return self._state == MinesweeperStates.game_lost

    def show(self):
        print ("  " + "".join([' {} '.format(i) for i in range(len(self.board))]))

        for row, row_number in zip(self.board, range(len(self.board))):
            print("{} ".format(row_number) + "".join([' {} '.format(self._render_cell(cell)) for cell in row]))

        print (self._state)

        # for row in self.board:
        #     print([item['adjacent_mines'] for item in row])

        # print(self.mines)
    # def update_state(self, operation):
    #     if self._state is MinesweeperStates.new_game:
    #         if operation is 'mark':
    #             self._state = MinesweeperStates.in_progress
    #
    #     elif self._state is MinesweeperStates.in_progress:
    #         pass
    #     elif self._state is MinesweeperStates.game_lost:
    #         pass
    #     else:
    #         pass
    def mark_cell(self, x, y):
        # update cell.state
        self.board[y][x]['state'] = 'marked'
        if self._state is MinesweeperStates.new_game:
            self._state = MinesweeperStates.in_progress
        # update remaining flags
        self.remaining_flags = self.remaining_flags - 1
        self.flags.append((y,x))

    def uncover_cell(self, x, y):
        if self.board[y][x]['is_armed'] == False:
            self.board[y][x]['state'] = 'uncovered'
            self.uncover_empty_neighbors(y,x)
            self._state = MinesweeperStates.in_progress
        else:
            self.board[x][y]['state'] = 'uncovered'
            self._state = MinesweeperStates.game_lost

    def uncover_empty_neighbors(self, i, j):
        for r,c in get_neighbors(i,j, len(self.board)):
            if self.board[r][c]['is_armed'] == False and self.board[r][c]['state'] == 'covered':
                self.board[r][c]['state'] = 'uncovered'
                self.uncover_empty_neighbors(r,c)

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
