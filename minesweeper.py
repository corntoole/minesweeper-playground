import random
class Minesweeper(object):
    grid_repr = {'empty': 'X', 'uncovered': '.', 'marked': 'M', 'armed': '*'}
    def compute_mine_adjacency(self):
        for mine in self.mines:
            for cell in get_neighbors(mine[0], mine[1], len(self.board)):
                self.board[cell[0]][cell[1]]['adjacent_mines'] = self.board[cell[0]][cell[1]]['adjacent_mines'] + 1

    def __init__(self, dim, number_of_mines):
        self.mines = []
        self.board = [ [] for d in range(dim)]
        for r in self.board:
            for i in range(dim):
                r.append({'state': 'empty', 'adjacent_mines': 0})
        for m in range(number_of_mines):
            x,y = (random.randint(0,dim-1),random.randint(0,dim-1))
            self.mines.append((x,y))
            self.board[x][y]['state'] = 'armed'
        self.compute_mine_adjacency()

    def show(self):
        for row in self.board:
            print([Minesweeper.grid_repr[item['state']] for item in row])

        for row in self.board:
            print([item['adjacent_mines'] for item in row])

        print(self.mines)

    def uncover_cell(self, x, y):
        if self.board[y][x]['state'] == 'empty':
            self.board[y][x]['state'] = 'uncovered'
            self.uncover_empty_neighbors(y,x)

    def uncover_empty_neighbors(self, i, j):
        for r,c in get_neighbors(i,j, len(self.board)):
            if self.board[r][c]['state'] == 'empty':
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
            else:
                pass
