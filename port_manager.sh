#!/bin/bash

# GET DIRECTORY WHERE THIS SCRIPT IS SAVED
DIR="$(dirname "$(realpath "$0")")"

cd "$DIR"

# ACTIVATE VIRTUAL ENV

source "$DIR/venv/bin/activate"

# RUN SERVER

exec python "$DIR/port_manager.py"
