#!/bin/bash
export PATH="$HOME/.local/bin:$PATH"
pipx install poetry
pipx ensurepath
. ~/.bashrc
make install
if [ "$LOAD_NER_MODELS" == "True" ]; then
    echo "Loading NER models"
    make loadModels
fi