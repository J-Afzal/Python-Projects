# Project List
Using Pygame:
* Chess
* Snake

Using Tkinter
* Currency Converter
* Calculator

# Chess
<h3 align="center"> Main Menu (left) and Game Window (right) </h3>
<p align="center"> <img src="chess/screenshots/main menu.png" width=400> <img src="chess/screenshots/game window.png" width=400> </p>
<h3 align="center"> Game Window During Pawn Promotion (left) and Game Over (right) </h3>
<p align="center"> <img src="chess/screenshots/game window pawn promotion.png" width=400> <img src="chess/screenshots/game over.png" width=400> </p>
<h3 align="center"> Info Window </h3>
<p align="center"> <img src="chess/screenshots/info window.png" width=400> </p>

# Snake
<h3 align="center"> Main Menu (left) amd Game Window (right) </h3>
<p align="center"> <img src="snake/screenshots/main menu.png" width=400> <img src="snake/screenshots/game window.png" width=400> </p>
<h3 align="center"> Game Over (left) and Info Window (right) </h3>
<p align="center"> <img src="snake/screenshots/game over.png" width=400> <img src="snake/screenshots/info window.png" width=400> </p>

# Currency Converter
<h3 align="center"> Main Window (top) Info Window (middle) and Update Window (bottom) </h3>
<p align="center"> <img src="currency converter/screenshots/main window.png"> </p>
<p align="center"> <img src="currency converter/screenshots/info window.png"> </p>
<p align="center"> <img src="currency converter/screenshots/update window.png"> </p>

# Calculator
<h3 align="center"> Main Window (left) and Info Window (right) </h3>
<p align="center"> <img src="calculator/screenshots/main window.png" height=500> <img src="calculator/screenshots/info window.png" height=500> </p>

# About
An assortment of projects that I undertook in order to learn Python

# Building [![PyInstaller](https://github.com/J-Afzal/Python-Projects/workflows/PyInstaller/badge.svg)](https://github.com/J-Afzal/Python-Projects/actions/workflows/pyinstaller.yml)
To install all the dependencies use the following command in the root directory:
```commandline
pip install -r requirements.txt
```
To compile each project in to a single .exe file using the following command in the ```.pyinstaller``` directory:
```commandline
pyinstaller build.spec
```
The .exe files should be located in ```.pyinstaller/dist/```
