# yo-yo-maskᴙ
A reversible anonymisation service for us all

## Build status
[![Docker](https://github.com/baloise/yo-yo-maskr/actions/workflows/docker-publish.yml/badge.svg?branch=release)](https://github.com/baloise/yo-yo-maskr/actions/workflows/docker-publish.yml)

## Setup development environment

```
python3 -m pip install pipx
pipx install poetry
pipx ensurepath
make install
```
## Run

```
make run
```
## Trouble shooting

```
echo -n 'db' | gnome-keyring-daemon --unlock
```