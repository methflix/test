#!/bin/bash

echo "This script can install Thorium Browser (SSE3 and regular), Firefox, and Brave Browser."
echo "1. Thorium Browser (SSE3)"
echo "2. Thorium Browser (regular)"
echo "3. Firefox"
echo "4. Brave Browser"
echo "5. Do not install any packages"

read -p "Do you want to continue with the installation? (yes/no): " confirmation

if [ "$confirmation" == "yes" ]; then
    echo "Choose the packages to install:"
    echo "1. Thorium Browser (SSE3)"
    echo "2. Thorium Browser (regular)"
    echo "3. Firefox"
    echo "4. Brave Browser"

    read -p "Enter your choice(s) separated by spaces (1 2 3 4): " choices

    for choice in $choices; do
        case $choice in
            1)
                paru -S thorium-browser-sse3-bin
                ;;
            2)
                paru -S thorium-browser-bin
                ;;
            3)
                sudo pacman -S firefox
                ;;
            4)
                paru -S brave-bin
                ;;
            *)
                echo "Invalid choice. Skipping."
                ;;
        esac
    done

    echo "Installation completed."
else
    echo "Installation canceled. No packages were installed."
fi

echo "This script will install touchpad gestures if you using a desktop type no:"
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
