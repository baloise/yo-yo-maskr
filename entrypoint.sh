#!/bin/bash

#set -x
echo "$(cat banner.txt)"
export PATH="/root/.local/bin:$PATH"
make run