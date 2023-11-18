#!/bin/bash

echo "Choose a Thorium Browser package to install:"
echo "1. thorium-browser-sse3-bin"
echo "2. thorium-browser-bin"
echo "3. Cancel installation"

read -p "Enter your choice (1, 2, or 3): " choice

case $choice in
    1)
        paru -S thorium-browser-sse3-bin
        ;;
    2)
        paru -S thorium-browser-bin
        ;;
    3)
        echo "Installation canceled."
        ;;
    *)
        echo "Invalid choice. Installation canceled."
        ;;
esac

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

logo "Installing Themes"				 
git clone https://github.com/Fausto-Korpsvart/Tokyo-Night-GTK-Theme.git
cd Tokyo-Night-GTK-Theme/
sudo cp -r themes/Tokyonight-Dark-BL-LB /usr/share/themes/
cd
printf "%s%sDone!!%s\n" "${BLD}" "${CGR}" "${CNC}"
sleep 2	  
clear

logo "Setup TimeZone Asia/Manila.."
sudo timedatectl set-timezone Asia/Manila >/dev/null 2>&1
printf "%s%sSuccesfully!%s\n" "${BLD}" "${CGR}" "${CNC}"
sleep 2
clear
