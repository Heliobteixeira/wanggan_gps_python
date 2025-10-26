"""
Bulk Download Example - Wanggan D6E GPS Library

This script demonstrates downloading all stored coordinates without headers
and exporting to multiple formats.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wanggan_gps import WangganGPS, DownloadMode, OutputFormat


def main():
    """Download all coordinates in bulk mode and export to all formats."""
    
    # Configuration
    port = 'COM5'  # Change to your serial port
    output_dir = 'bulk_export'
    
    print(f"Wanggan GPS Bulk Download")
    print(f"Port: {port}")
    print(f"Output: {output_dir}/")
    print("-" * 50)
    
    # Using context manager (automatic connect/disconnect)
    with WangganGPS(port=port, output_dir=output_dir) as gps:
        
        # Download all coordinates (no headers)
        print("\nDownloading all coordinates...")
        data = gps.download(
            mode=DownloadMode.EXCLAMATION,
            save_raw=True,
            raw_filename='bulk_raw.txt'
        )
        
        if not data:
            print("No data received")
            return
        
        # Count coordinates
        coords = data.decode('utf-8', errors='ignore').count(';')
        print(f"Downloaded {len(data)} bytes ({coords} coordinates)")
        
        # Export to KML
        print("\nExporting to KML...")
        kml_files = gps.export_tracks(data, OutputFormat.KML)
        print(f"  Created: {kml_files[0] if kml_files else 'None'}")
        
        # Export to GPX
        print("Exporting to GPX...")
        gpx_files = gps.export_tracks(data, OutputFormat.GPX)
        print(f"  Created: {gpx_files[0] if gpx_files else 'None'}")
        
        # Export to CSV
        print("Exporting to CSV...")
        csv_files = gps.export_tracks(data, OutputFormat.CSV)
        print(f"  Created: {csv_files[0] if csv_files else 'None'}")
        
        print(f"\nAll files saved to: {output_dir}/")


if __name__ == "__main__":
    main()
