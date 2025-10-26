"""
Basic Usage Example - Wanggan GPS Python Library

This script demonstrates the simplest way to download and export GPS tracks.
Tested on: Wanggan D6E GNSS Handheld Navigator
"""

import sys
from pathlib import Path

# Add parent directory to path (for development/testing)
sys.path.insert(0, str(Path(__file__).parent.parent))

from wanggan_gps import WangganGPS, DownloadMode, OutputFormat


def main():
    """Basic example: Download tracks with headers and export to KML."""
    
    # Configuration
    port = 'COM5'  # Change to your serial port
    output_dir = 'output'
    
    # Create GPS interface
    gps = WangganGPS(port=port, output_dir=output_dir)
    
    # Connect to device
    if not gps.connect():
        print("Failed to connect to GPS device")
        return
    
    print(f"Connected to {port}")
    
    # Download data with track headers
    print("Downloading tracks...")
    data = gps.download(mode=DownloadMode.TILDE, save_raw=True)
    
    if not data:
        print("No data received")
        gps.disconnect()
        return
    
    print(f"Downloaded {len(data)} bytes")
    
    # Export to KML (separate file per track)
    print("Exporting to KML...")
    files = gps.export_tracks(
        data=data,
        format=OutputFormat.KML,
        split_by_track=True
    )
    
    print(f"\nCreated {len(files)} file(s):")
    for file in files:
        print(f"  - {file}")
    
    # Clean disconnect
    gps.disconnect()
    print("\nDisconnected")


if __name__ == "__main__":
    main()
