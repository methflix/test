#!/bin/sh

echo "Type N if you using a Desktop. Type y if you using a Laptop"
echo "Do you want to proceed? [y/N]"
read confirm

if [ "$confirm" != "y" ]; then
  echo "Aborting..."
  exit 1
fi

sudo pacman -S wmctrl xdotool --noconfirm
sudo gpasswd -a $USER input

echo "Installing libinput-gestures using Paru..."
paru -S libinput-gestures --skipreview --noconfirm
```
