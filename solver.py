from minesweeper import Minesweeper, get_neighbors
import random
import time
from enum import Enum
import sys
from optparse import OptionParser

class Solver(object):
	def __init__(self, game):
		self.game = game
		self._wins = 0
		self._losses = 0
		try:
			self.num_rows = self.game.get_num_rows()
			self.num_cols = self.game.get_num_cols()
			self.top_left  =    (0, 0)
			self.top_right =    (0, self.num_cols - 1)
			self.bottom_right = (self.num_rows - 1, self.num_cols - 1)
			self.bottom_left  = (self.num_rows - 1, 0)
		except Exception as e:
			print("Error {}".format(e))
			raise

	def set_game(self, game):
		self.game = game
		self.top_left  =    (0, 0)
		self.top_right =    (0, self.num_cols - 1)
		self.bottom_right = (self.num_rows - 1, self.num_cols - 1)
		self.bottom_left  = (self.num_rows - 1, 0)

	def new_game(self):
		self.game.new_game()

	def solve(self):
		num_rows = self.game.get_num_rows()
		num_cols = self.game.get_num_cols()
		random.seed()
		# self.game.uncover_cell(num_rows//2, num_cols//2)
		# self.game.uncover_cell(num_rows-1,0)
		while not self.game.is_game_over():
			col = random.randint(0, num_cols - 1)
			row = random.randint(0, num_rows - 1)
			self.game.uncover_cell(col, row)
		# self.game.show()
		results = self.game.get_results()
		if results['outcome'] == 'game_won':
			self._wins = self._wins + 1
		else:
			self._losses = self._losses + 1

class Corner(Enum):
	top_left = 1
	top_right = 2
	bottom_right = 3
	bottom_left = 4


class Solver2(Solver):

	def __init__(self, game):
		Solver.__init__(self, game)
		self.corner_dict = {}
		self.corner_dict[Corner.top_left] = self.top_left
		self.corner_dict[Corner.top_right] = self.top_right
		self.corner_dict[Corner.bottom_right] = self.bottom_right
		self.corner_dict[Corner.bottom_left] = self.bottom_left

	def _uncover_center_cell(self):
		self.game.uncover_cell(self.num_rows//2, self.num_cols//2)

	def _uncover_corner_cell(self, corner=None):
		if corner is None or corner not in Corner:
			corner = random.choice(list(Corner))
		(x,y) = self.corner_dict[corner]
		self.game.uncover_cell(x,y)

	def _uncover_random_cell(self):
		# board = self.game.get_board()
		# covered_cells = [cell for row in board for cell in row if cell.state is 'covered']
		# cell = random.choice(covered_cells)
		# self.game.uncover_cell(cell.x, cell.y)
		col = random.randint(0, self.num_cols - 1)
		row = random.randint(0, self.num_rows - 1)
		self.game.uncover_cell(col, row)

	def _strategy_1_(self):
		board = self.game.get_board()
		dim = len(board)
		uncovered_cells = set([])
		empty_cells = set([])
		marked_cells = set([])
		covered_cells = set([])
		covered_cells_surrounded_by_numbers = set([])
		cells_w_basic_num_pattern = set([])
		# empty_cells_touching_mines = [[cell for cell in row if cell[0] is 'uncovered' and cell[1] > 0] for row in board]
		for row in board:
			for cell in row:
				if cell.state is 'uncovered':
					uncovered_cells.add(cell)
					if cell.num_adjacent_mines > 0:
						neighbors = get_neighbors(cell.y, cell.x, dim)
						matching = [board[coord[0]][coord[1]] for coord in neighbors if board[coord[0]][coord[1]].state == 'covered' ]
						if cell.num_adjacent_mines == len(matching):
							for m in matching:
								cells_w_basic_num_pattern.add(m)
				elif cell.state is 'marked':
					marked_cells.add(cell)
				else:
					covered_cells.add(cell)
					#find cells surrounded by numbers
					neighbors = get_neighbors(cell.y, cell.x, dim)
					cells_w_numbers = [board[coord[0]][coord[1]] for coord in neighbors if board[coord[0]][coord[1]].num_adjacent_mines > 0 and board[coord[0]][coord[1]].state is 'uncovered']
					if len(neighbors) == len(cells_w_numbers):
						covered_cells_surrounded_by_numbers.add(cell)
		# print("empty cell: {}\nmarked cells: {}\ncovered cells: {}\ncovered cells surrouded by numbers: {}".format(empty_cells, marked_cells, covered_cells, covered_cells_surrounded_by_numbers))
		for cell in covered_cells_surrounded_by_numbers:
			self.game.mark_cell(cell.x, cell.y)
		for cell in cells_w_basic_num_pattern:
			self.game.mark_cell(cell.x, cell.y)


	def solve(self):
		num_rows = self.game.get_num_rows()
		num_cols = self.game.get_num_cols()
		random.seed()
		# self.game.uncover_cell(num_rows//2, num_cols//2)
		# self.game.uncover_cell(num_rows-1,0)
		action = random.choice([self._uncover_center_cell, self._uncover_corner_cell])
		action()
		self._strategy_1_()
		while not self.game.is_game_over():
			self._uncover_random_cell()
			self._strategy_1_()
		results = self.game.get_results()
		if results['outcome'] == 'game_won':
			self._wins = self._wins + 1
		else:
			self._losses = self._losses + 1

def main(num_runs=1000):
	game = Minesweeper(10, 10)
	solver = Solver2(game)
	t1 = time.time()
	solver.solve()
	for i in range(num_runs-1):
		game = Minesweeper(10, 10)
		solver.set_game(game)
		solver.solve()
	t2 = time.time()
	print("Losses: {}, Wins: {} in {} seconds".format(solver._losses, solver._wins, t2 - t1))
	return "Losses: {}, Wins: {} in {} seconds".format(solver._losses, solver._wins, t2 - t1)


def parallel(n_jobs=2, num_runs=1000):
	from multiprocessing import Pool
	p = Pool(n_jobs)

	p.map(main, [num_runs//n_jobs for i in range(n_jobs)])



if __name__ == '__main__':

	usage = "usage: %prog [options]"
	parser = OptionParser()
	parser.add_option("-s", "--solver", dest="solver",
						help="which solver: random or basic [default: basic]", default="basic")
	parser.add_option("-j", "--num-jobs", type="int", dest="n_jobs", help="how many processes to run [default: 1]", default=1)
	parser.add_option("-n", "--num-games", type="int", dest="num_runs", help="how many games to play [default: 1000]", default=1000)

	(options, args) = parser.parse_args()

	_opts = options.__dict__

	# if len(sys.argv) > 1:
	n_jobs = _opts['n_jobs']
	num_runs = _opts['num_runs']
	solver_type = _opts['solver']

	def f(n, which_solver=solver_type):
		gm = Minesweeper(10, 10)
		if which_solver is 'basic':
			s = Solver2(gm)
		else:
			s = Solver(gm)
		for i in range(n):
			s.solve()
			s.new_game()
		return {'wins': s._wins, 'losses': s._losses}

	from multiprocessing import Pool
	from functools import reduce
	p = Pool(n_jobs)

	t1 = time.time()
	results = p.map(f, [num_runs//n_jobs for i in range(n_jobs)])
	t2 = time.time()
	aggregate_results = reduce(lambda x,y: {'wins': x['wins']+y['wins'], 'losses': x['losses']+y['losses']}, results, {'wins': 0, 'losses': 0})
	print("Wins: {}, Losses: {}, in {} seconds".format(aggregate_results['wins'], aggregate_results['losses'], t2 - t1))
