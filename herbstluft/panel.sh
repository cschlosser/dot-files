#!/bin/bash
PATH=$HOME/.local/bin:$PATH
for m in $(polybar --list-monitors | cut -d":" -f1); do
    MONITOR=$m polybar -c $HOME/.config/polybar/config herbstluft &
done
