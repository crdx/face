# face

**face** is a modular IRC bot.

It's simply a glorified module loader that loads modules in the `modules` directory and passes IRC events on to them.

## Installation

Install virtualenv if you don't have it.

    sudo pip install virtualenv

Create the environment.

    virtualenv -p /usr/bin/python3 py3env
    source py3env/bin/activate

Install the required packages.

    pip install irc pyinotify

## Usage

    source py3env/bin/activate
    python face.py

## Bugs or contributions

Open an [issue](https://github.com/crdx/face/issues) or send a [pull request](https://github.com/crdx/face/pulls).

## Licence

[MIT](LICENCE.md).
