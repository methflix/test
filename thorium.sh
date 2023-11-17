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

# Done!
