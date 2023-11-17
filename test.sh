#!/bin/sh

echo "Select N if you using a Desktop. Select y if you using a Laptop"
echo "Do you want to proceed? [y/N]"
read confirm

if [ "$confirm" != "y" ]; then
  echo "Aborting..."
  exit 1
fi

sudo pacman -S wmctrl xdotool
sudo gpasswd -a $USER input

echo "Installing libinput-gestures using Paru..."
paru -S libinput-gestures
```
