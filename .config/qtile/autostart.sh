#!/usr/bin/env bash 

picom --daemon --config ~/.config/picom/picom.conf --log-file ~/.local/share/picom/picom.log --log-level WARN --experimental-backends
clight &
