#!/bin/bash

# Prompt user to select installation type
echo "Please select the installation type:"
echo "1. Thorium Browser with SSE3 support"
echo "2. Thorium Browser without SSE3 support"
read -p "Enter your choice (1/2): " choice

# Install Thorium Browser with SSE3 support
if [[ $choice -eq 1 ]]; then
  paru -S thorium-browser-sse3-bin --skipreview --noconfirm
elif [[ $choice -eq 2 ]]; then
  paru -S thorium-browser-bin --skipreview --noconfirm
else
  echo "Invalid choice. Exiting script."
  exit 1
fi

echo "Type N if you using a Desktop. Type y if you using a Laptop"
echo "Do you want to proceed? [y/N]"
read confirm

if [ "$confirm" != "y" ]; then
  echo "Aborting..."
  exit 1
fi

echo "This script will install the following packages and add the user to the 'input' group:"
echo "1. wmctrl"
echo "2. xdotool"
echo "3. paru"
echo "4. libinput-gestures"
echo "5. Add user to 'input' group"

read -p "Do you want to continue? (yes/no): " confirmation

if [ "$confirmation" == "yes" ]; then
    sudo pacman -S wmctrl xdotool
    paru -S libinput-gestures
    sudo gpasswd -a $USER input
    echo "Installation completed."
else
    echo "Installation canceled."
fi

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
