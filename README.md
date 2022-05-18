<p align="center"> <img src="screenshots/chess.gif" height=400> <img src="screenshots/snake.gif" height=400> </p>
<p align="center"> <img src="screenshots/currency_converter.gif"> </p>
<p align="center"> <img src="screenshots/calculator.gif" width=400> </p>

# About
An assortment of projects that I undertook in order to learn Python:

Using Pygame:
* Chess
* Snake

Using Tkinter
* Currency Converter
* Calculator

# Building [![PyInstaller](https://github.com/J-Afzal/Python-Projects/workflows/PyInstaller/badge.svg)](https://github.com/J-Afzal/Python-Projects/actions/workflows/pyinstaller.yml)
To install all the dependencies use the following command in the root directory:
```commandline
pip install -r requirements.txt
```
To compile each project into a single .exe file using the following command in the `.pyinstaller` directory:
```commandline
pyinstaller build.spec
```
The .exe files should be located in `.pyinstaller/dist/`
