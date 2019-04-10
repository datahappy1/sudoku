# Sudoku game generator and solver


[installation and getting started](#installation-and-getting-started)<br>
[running sudoku generator](#running-sudoku-generator)<br>
[running sudoku solver](#running-sudoku-solver)<br>
[worlds hardest sudoku](#worlds-hardest-sudoku)<br>


### installation and getting started

1) First, clone this repo locally. `https://github.com/datahappy1/sudoku.git __your_local_sudoku_folder__`
2) To install this game, you need to install all the packages
from dependencies.txt, so change directory to `cd __your_local_sudoku_folder__`
and install using the command `pip install -r requirements.txt`

3) Set your PYTHONPATH variable ( on Windows, for example like ) :
`set PYTHONPATH=%PYTHONPATH%;C:\__your_local_sudoku_folder__\`
4) Pytest can be used to make sure you're working on a healthy codebase.
To run the tests, run the command `pytest`.
Currently there is 6 functional tests in the repo, all 3 levels of sudoku
generator function calls and all 3 levels of sudoku solvers get evaluated. 

*This is just a quick guide, however I strongly suggest to use a virtual environment like pipenv or poetry

### running sudoku generator
arguments needed:<br>
-a: action (str, required, option:"generate")<br>
-l: level (str, optional, options: {"easy", "medium", "hard"}, default: "easy")<br>
-p: prettify (bool, optional, options: {"T","F","True","False",1,0}, default: 0)<br>
<br>
example:<br>
`python3 sudoku_game.py -a "generate" -l "hard" -p 1`
<br>

### running sudoku solver
arguments needed:<br>
-a: action (str, required, option: "solve")<br>
-f: filepath (str, optional, options: {"easy", "medium", "hard"}, default: "files/sudoku_easy.txt")<br>
-p: prettify (bool, optional, options: {"T","F","True","False",1,0}, default: 0)<br>
<br>
example:<br>
`python3 sudoku_game.py -a "solve" -f "files/sudoku_hard.txt" -p True`
<br>

### worlds hardest sudoku
https://www.conceptispuzzles.com/index.aspx?uri=info%2Farticle%2F424

8 0 0 0 0 0 0 0 0<br>
0 0 3 6 0 0 0 0 0<br>
0 7 0 0 9 0 2 0 0<br>
0 5 0 0 0 7 0 0 0<br>
0 0 0 0 4 5 7 0 0<br>
0 0 0 1 0 0 0 3 0<br>
0 0 1 0 0 0 0 6 8<br>
0 0 8 5 0 0 0 1 0<br>
0 9 0 0 0 0 4 0 0<br>

this tool calculated the solution:

8 1 2 7 5 3 6 4 9<br>
9 4 3 6 8 2 1 7 5<br>
6 7 5 4 9 1 2 8 3<br>
1 5 4 2 3 7 8 9 6<br>
3 6 9 8 4 5 7 2 1<br>
2 8 7 1 6 9 5 3 4<br>
5 2 1 9 7 4 3 6 8<br>
4 3 8 5 2 6 9 1 7<br>
7 9 6 3 1 8 4 5 2<br>
