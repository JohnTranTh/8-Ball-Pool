# Project Title

8-Ball Game simulator playable through locally hosted webserver.

## Description

This program allows two players to play 8-Ball through a website running on a locally hosted webserver. The game has a simplified
ruleset. There are no penalities for scratching or sinking the cue. Missing all balls incurs no penalty. There are
no calling shots.

## Getting Started

### Dependencies

* Python 3
* Swig
* Make
* Clang

### Executing program

* Python3, Clang, Swig, and Make are required to compile and run the program
* These can all be installed through WSL
* export LD_LIBRARY_PATH=`pwd` must be entered in the command line before running
* To run the webserver, enter "python3 server.py 'portnumber' ", the portnumber can be any number (i.e. 10000)
* While running, go to http://localhost:portnumber/startPage.html, where portnumber is the number entered previously
* To stop the server, enter Ctrl + c on the command line 

## Author Information

Name: John Tran
Email: jtran18@uoguelph.ca

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [simple-readme] (https://gist.githubusercontent.com/DomPizzie/7a5ff55ffa9081f2de27c315f5018afc/raw/d59043abbb123089ad6602aba571121b71d91d7f/README-Template.md)
