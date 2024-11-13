#!/bin/bash

# Execute the command passed to the container
echo "$(cat banner.txt)"

# Define your dictionary as an associative array
declare -A flavor

# Add key-value pairs
flavor["openshift"]="make runos"
flavor["default"]="make run"

if [ -z "$@" ]; then
    export PATH="$HOME/.local/bin:$PATH"
    echo "starting with flavor: $HOST_FLAVOR"
    eval "${flavor[$HOST_FLAVOR]}"
fi

# Execute the command passed to the container
exec "$@"