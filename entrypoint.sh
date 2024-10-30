#!/bin/sh

# Execute the command passed to the container
echo "$(cat banner.txt)"
export PATH="$HOME/.local/bin:$PATH"
make run

# Execute the command passed to the container
exec "$@"