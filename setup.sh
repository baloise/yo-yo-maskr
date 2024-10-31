#!/bin/sh
export PATH="$HOME/.local/bin:$PATH"
pipx install poetry
pipx ensurepath
. ~/.bashrc
make install