#!/bin/bash

echo "The following commands will be executed:"
echo "sudo pacman -S sudo"
echo "sudo pacman -S wmctrl"
echo "xdotool"
echo "paru -S libinput-gestures"

read -p "Do you want to proceed? [y/N] " choice

if [[ $choice == "y" || $choice == "Y" ]]; then
  sudo pacman -S sudo
  sudo pacman -S wmctrl
  xdotool
  paru -S libinput-gestures
else
  echo "Aborting..."
fi
