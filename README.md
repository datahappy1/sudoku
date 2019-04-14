# Sudoku game generator and solver

![](https://github.com/datahappy1/sudoku/blob/master/docs/img/rating.svg)

[installation and getting started](#installation-and-getting-started)<br>
[running sudoku generator](#running-sudoku-generator)<br>
[running sudoku solver](#running-sudoku-solver)<br>
[solving the "worlds hardest sudoku"](#solving-the-"worlds-hardest-sudoku")<br>


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
-l: level (str, required, options: {"easy", "medium", "hard"}, default: "easy")<br>
-p: prettify (str, optional, options: {"T","F","True","False","1","0"}, default: 0)<br>
<br>
example:<br>
`python3 sudoku_game.py -a "generate" -l "hard" -p 1`
<br>

### running sudoku solver
arguments needed:<br>
-a: action (str, required, option: "solve")<br>
-f: filepath (str, optional, options: {"easy", "medium", "hard"}, default: "files/sudoku_easy.txt")<br>
-p: prettify (str, required, options: {"T","F","True","False","1","0"}, default: "0")<br>
<br>
The format of the text file with the sudoku to be solved has to be set like:
000500640<br>
009630018<br>
061409200<br>
000001803<br>
700305001<br>
203900000<br>
002806450<br>
670054300<br>
054003000<br>
( The zeros are the grid members that need to be calculated ) :) 
 
<br>
example:<br>
`python3 sudoku_game.py -a "solve" -f "files/sudoku_hard.txt" -p True`
<br>

### solving the "worlds hardest sudoku"
https://www.conceptispuzzles.com/index.aspx?uri=info%2Farticle%2F424

800000000<br>
003600000<br>
070090200<br>
050007000<br>
000045700<br>
000100030<br>
001000068<br>
008500010<br>
090000400<br>

this tool calculated the solution:

812753649<br>
943682175<br>
675491283<br>
154237896<br>
369845721<br>
287169534<br>
521974368<br>
438526917<br>
796318452<br>
