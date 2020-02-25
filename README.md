# Sudoku game generator and solver

![](https://github.com/datahappy1/sudoku/blob/master/docs/img/rating.svg)

[installation and getting started](#installation-and-getting-started)<br>
[running sudoku generator](#running-sudoku-generator)<br>
[running sudoku solver](#running-sudoku-solver)<br>
[solving the worlds hardest sudoku](#solving-the-worlds-hardest-sudoku)<br>


### installation and getting started

1) First, clone this repo `git clone https://github.com/datahappy1/sudoku.git c:\sudoku`
2) Set PYTHONPATH , from Windows CMD for example `set PYTHONPATH=%PYTHONPATH%;C:\sudoku`
3) Pytest can be used to make sure you're working on a healthy codebase.
You can install the `Pytest` package from requirements.txt using the command `pip install -r requirements.txt`
Currently there are 6 functional tests in the repo, all 3 levels of sudoku
generator function calls and all 3 levels of sudoku solvers are getting evaluated.

*It is highly recommended to setup and activate `pipenv` or `virtualenv`

### running sudoku generator
arguments needed:<br>
-a: action (str, required, option:"generate")<br>
-l: level (str, optional, options: {"easy", "medium", "hard"}, default: "easy")<br>
-p: prettify (str, optional, options: {"T","F","True","False","1","0"}, default: 0)<br>
<br>
example:<br>
`CD c:\sudoku`
`python sudoku\sudoku_game.py -a "generate" -l "hard" -p 1`
<br>

### running sudoku solver
arguments needed:<br>
-a: action (str, required, option: "solve")<br>
-f: filepath (str, optional, options: {"easy", "medium", "hard"}, default: "files/sudoku_easy.txt")<br>
-p: prettify (str, optional, options: {"T","F","True","False","1","0"}, default: "0")<br>
<br>
The format of the text file with the sudoku to be solved has to be set like:<br>
000500640<br>
009630018<br>
061409200<br>
000001803<br>
700305001<br>
203900000<br>
002806450<br>
670054300<br>
054003000<br>
( The zeros are the grid members that need to be calculated ) :) <br>
<br>
example:<br>
`CD c:\sudoku`
`python sudoku\sudoku_game.py -a "solve" -f "files/sudoku_hard.txt" -p 1`
<br>

### solving the worlds hardest sudoku
The "worlds hardest sudoku" game is described here:<br>
https://www.conceptispuzzles.com/index.aspx?uri=info%2Farticle%2F424<br>

this is how it looks like:<br>

800000000<br>
003600000<br>
070090200<br>
050007000<br>
000045700<br>
000100030<br>
001000068<br>
008500010<br>
090000400<br>

and the sudoku solver calculated solution (in ~1 minute on a 8GB RAM VMWare virtual machine):

812753649<br>
943682175<br>
675491283<br>
154237896<br>
369845721<br>
287169534<br>
521974368<br>
438526917<br>
796318452<br>
