from minesweeper import Minesweeper
import random
import time
from enum import Enum

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

	def start(self):
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

	def start(self):
		num_rows = self.game.get_num_rows()
		num_cols = self.game.get_num_cols()
		random.seed()
		# self.game.uncover_cell(num_rows//2, num_cols//2)
		# self.game.uncover_cell(num_rows-1,0)
		action = random.choice([self._uncover_center_cell, self._uncover_corner_cell])
		action()
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

def main():
	game = Minesweeper(10, 10)
	solver = Solver2(game)
	t1 = time.time()
	solver.start()
	for i in range(99999):
		game = Minesweeper(10, 10)
		solver.set_game(game)
		solver.start()
	t2 = time.time()
	print("Losses: {}, Wins: {} in {} seconds".format(solver._losses, solver._wins, t2 - t1))
