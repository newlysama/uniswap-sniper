#!/bin/bash

if [[ "$1" == "-D" ]] || [[ "$1" == "--debug" ]]; then
    python3.10 -m src.Program --debug
elif [[ -z "$1" ]]; then
    python3.10 -m src.Program
else
    echo "Invalid arg: $1, please use --debug or -D for debug mode, and no option for main program."
    exit 1
fi