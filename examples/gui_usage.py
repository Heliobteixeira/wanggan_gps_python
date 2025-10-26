"""
Example: Launch the Wanggan GPS GUI Interface

This script demonstrates how to launch the graphical user interface
for non-technical users to easily download GPS data.

Usage:
    python gui_usage.py

Or simply run the GUI directly:
    python wanggan_gps_gui.py
"""

import sys
from pathlib import Path

# Add parent directory to path to import wanggan_gps_gui
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

# Import and run the GUI
from wanggan_gps_gui import main

if __name__ == "__main__":
    print("Starting Wanggan GPS GUI...")
    print("Please use the graphical interface that appears.")
    main()
