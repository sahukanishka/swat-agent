#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Make the swat script executable
chmod +x "$SCRIPT_DIR/swat"

# Create a symbolic link in /usr/local/bin
echo "Creating symbolic link for swat command..."
sudo ln -sf "$SCRIPT_DIR/swat" /usr/local/bin/swat

# Create virtual environment if it doesn't exist
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$SCRIPT_DIR/.venv"
    source "$SCRIPT_DIR/.venv/bin/activate"
    pip install -r "$SCRIPT_DIR/requirements.txt"
fi

echo "Installation complete! You can now use the 'swat' command from anywhere."
echo "Example: swat \"find the port 8080 and kill it\"" 