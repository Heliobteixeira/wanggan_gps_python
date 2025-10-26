#!/bin/bash
# Wanggan GPS GUI Launcher for Linux/Mac
# Make executable with: chmod +x launch_gui.sh
# Then run with: ./launch_gui.sh

echo ""
echo "========================================"
echo "  Wanggan GPS Data Downloader"
echo "========================================"
echo ""
echo "Starting GUI interface..."
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if easygui is installed
if ! python3 -c "import easygui" &> /dev/null; then
    echo "Installing required GUI library..."
    pip3 install easygui
    echo ""
fi

# Launch the GUI
python3 wanggan_gps_gui.py

if [ $? -ne 0 ]; then
    echo ""
    echo "An error occurred while running the GUI."
    echo ""
    read -p "Press Enter to exit..."
fi
