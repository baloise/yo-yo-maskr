#!/bin/sh

# Execute the command passed to the container
echo "$(cat banner.txt)"

if [ -z "$@" ]; then
    export PATH="$HOME/.local/bin:$PATH"
    make run
fi

# Execute the command passed to the container
exec "$@"