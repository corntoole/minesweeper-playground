# Minesweeper
## a Minesweeper game

## Instructions

### Requirements

  * python 3.x
	* to run the game and solver: no dependencies
  * to run the iPython Notebook:
	* ```pip install -r requirements.txt```

### To Play Minesweeper game

```python minesweeper.py```


### To Run the solver
```python solver.py``` for default runtime arguments

```python solver.py -h``` for usage information

#### Solver Usage

			Usage: solver.py [options]

			Options:
			-h, --help            show this help message and exit
			-s SOLVER, --solver=SOLVER
												which solver: random or basic [default: basic]
			-j N_JOBS, --num-jobs=N_JOBS
												how many processes to run [default: 1]
			-n NUM_RUNS, --num-games=NUM_RUNS
												how many games to play [default: 1000]
