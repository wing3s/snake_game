## Installation
```sh
git clone git@github.com:wing3s/snake_game.git
cd snake_game
# Install app required packages
pip install -r requirements.txt
```

#### Note
If you have any issue with matplotlib package installation, please follow below steps.
##### MacOS with virtualenv (pyenv)
```sh
# Install a Python version
PYTHON_CONFIGURE_OPTS="--enable-unicode=ucs2 --enable-framework CC=clang" pyenv install <your_python_version>
pyenv virtualenv <your_python_version> <your_virtualenv_name>
# Install app required packages
git clone git@github.com:wing3s/snake_game.git
cd snake_game
# Install app required packages
pyenv activate <your_virtualenv_name>
pip install -r requirements.txt
# add missing file for matplotlib in Python virtualenv
echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
```
##### Ubuntu with virtualenv (pyenv)
```sh
# Install freestyle, png packages
sudo apt-get install freetype* libpng*
# Install a Python version
PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install <your_python_version>
pyenv virtualenv <your_python_version> <your_virtualenv_name>
# Install app required packages
git clone git@github.com:wing3s/snake_game.git
cd snake_game
# Install app required packages
pyenv activate <your_virtualenv_name>
pip install -r requirements.txt
```

## Play the game
```sh
python terminal.py
```
- 1: snake or wall
- F: target fruit

<img src="assets/terminal_example.png" height="250" width="250" />