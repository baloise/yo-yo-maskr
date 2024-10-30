#!/bin/sh

# Your entry point logic here
echo "Running entry point script..."

# Execute the command passed to the container
echo "$(cat banner.txt)"
export PATH="$HOME/.local/bin:$PATH"
make run

# Execute the command passed to the container
exec "$@"