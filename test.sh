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
