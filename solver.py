from minesweeper import Minesweeper
import random
import time

class Solver(object):
	def __init__(self, game):
		self.game = game
		self._wins = 0
		self._losses = 0

	def set_game(self, game):
		self.game = game

	def start(self):
		num_rows = self.game.get_num_rows()
		num_cols = self.game.get_num_cols()
		random.seed()
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
	solver = Solver(None)
	t1 = time.time()
	for i in range(100000):
		game = Minesweeper(10, 10)
		solver.set_game(game)
		solver.start()
	t2 = time.time()
	print("Losses: {}, Wins: {} in {} seconds".format(solver._losses, solver._wins, t2 - t1))
