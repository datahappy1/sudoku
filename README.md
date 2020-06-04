# Sudoku game generator and solver
 ![](https://github.com/datahappy1/sudoku/blob/master/docs/img/rating.svg)

- [installation and getting started](#installation-and-getting-started)
- [running sudoku generator](#running-sudoku-generator)
- [running sudoku solver](#running-sudoku-solver)
- [solving the worlds hardest sudoku](#solving-the-worlds-hardest-sudoku)


### installation and getting started
 - First, clone this repo `git clone https://github.com/datahappy1/sudoku.git c:\sudoku`
 - Second, set PYTHONPATH
   - from Windows CMD for example `set PYTHONPATH=%PYTHONPATH%;C:\sudoku`
   - from Linux CMD for example `export PYTHONPATH=${PYTHONPATH}:${HOME}/sudoku`
- Pytest can be used to make sure you're working on a healthy codebase.
You can install the `Pytest` package from requirements.txt using the command `pip install -r requirements.txt` . There are functional tests in the `/tests` folder, that can be used for running sudoku solver on 10 sudoku puzzles of all complexity levels and a sudoku generator generating easy, medium and hard level puzzles. 
> It is highly recommended to setup and activate `virtualenv` or use
> `pipenv`

  ### running sudoku generator 
arguments needed:
- `-a` action (str, required, option:"generate")
- `-l:` level (str, optional, options: {"easy", "medium", "hard"}, default: "easy")
- `-p:` prettify (str, optional, options: {"T","F","True","False","1","0"}, default: 0)

example:
```
CD c:\sudoku
python sudoku\sudoku_game.py -a "generate" -l "hard" -p 1
```

  ### running sudoku solver 
arguments needed:
- `-a` action (str, required, option: "solve")
- `-f` filepath (str, optional, options: {"easy", "medium", "hard"}, default: "files/sudoku_easy.txt")
- `-p` prettify (str, optional, options: {"T","F","True","False","1","0"}, default: "0")

The format of the text file with the sudoku to be solved has to be set like:
```  
000500640
009630018
061409200
000001803
700305001
203900000
002806450
670054300
054003000
```  

> The zeros are the grid members that need to be calculated  

example:
```
CD c:\sudoku
python sudoku\sudoku_game.py -a "solve" -f "files/sudoku_hard.txt" -p 1
```

### solving the worlds hardest sudoku 
The "worlds hardest sudoku" game is described [here](https://www.conceptispuzzles.com/index.aspx?uri=info/article/424)
and this is how the puzzle looks like:
```
800000000
003600000
070090200
050007000
000045700
000100030
001000068
008500010
090000400 
```
and this is the sudoku solver calculated solution:
```
812753649
943682175
675491283
154237896
369845721
287169534
521974368
438526917
796318452
```
