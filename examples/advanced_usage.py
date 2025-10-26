"""
Advanced Usage Example - Wanggan GPS Python Library

This script demonstrates advanced features:
- Testing different download modes
- Custom parsing
- Error handling
- Progress monitoring

Tested on: Wanggan D6E GNSS Handheld Navigator
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from wanggan_gps import WangganGPS, DownloadMode, OutputFormat


def analyze_track_data(data: bytes) -> dict:
    """Analyze downloaded track data."""
    
    text = data.decode('utf-8', errors='ignore')
    
    # Count elements
    headers = text.count('n')  # Track headers start with 'n'
    coordinates = text.count(';')
    
    # Extract track IDs
    track_ids = []
    for line in text.split('\n'):
        if line.startswith('n'):
            try:
                track_id = line.split(',')[0][1:]  # Remove 'n' prefix
                track_ids.append(int(track_id))
            except:
                pass
    
    return {
        'size_bytes': len(data),
        'headers': headers,
        'coordinates': coordinates,
        'track_ids': track_ids,
        'track_count': len(track_ids)
    }


def test_all_modes(gps: WangganGPS):
    """Test all three download modes."""
    
    modes = [
        (DownloadMode.TILDE, "Track headers + coordinates"),
        (DownloadMode.EXCLAMATION, "All coordinates (no headers)"),
        (DownloadMode.CARET, "Binary metadata"),
    ]
    
    print("\n" + "=" * 60)
    print("TESTING ALL DOWNLOAD MODES")
    print("=" * 60)
    
    for mode, description in modes:
        print(f"\n{mode.name} Mode (0x{mode.value:02X})")
        print(f"  Purpose: {description}")
        print(f"  Downloading...", end='', flush=True)
        
        data = gps.download(mode=mode)
        
        if not data:
            print(" No data received")
            continue
        
        print(f" {len(data)} bytes")
        
        if mode == DownloadMode.CARET:
            # Binary mode - show hex dump
            hex_data = ' '.join(f'{b:02X}' for b in data[:20])
            print(f"  Data (first 20 bytes): {hex_data}")
        else:
            # Text mode - analyze
            stats = analyze_track_data(data)
            print(f"  Tracks: {stats['track_count']}")
            print(f"  Coordinates: {stats['coordinates']}")
            if stats['track_ids']:
                print(f"  Track IDs: {stats['track_ids']}")


def main():
    """Advanced example with multiple download modes and analysis."""
    
    # Configuration
    port = 'COM5'  # Change to your serial port
    output_dir = 'advanced_output'
    
    print("Wanggan GPS Advanced Usage")
    print(f"Port: {port}")
    print(f"Output: {output_dir}/")
    
    # Create GPS interface with custom timeout
    gps = WangganGPS(
        port=port,
        baudrate=115200,
        timeout=2.0,  # Longer timeout for large downloads
        output_dir=output_dir
    )
    
    # Connect with error handling
    try:
        if not gps.connect():
            print("ERROR: Failed to connect")
            return
        
        print(f"Connected successfully\n")
        
        # Test all download modes
        test_all_modes(gps)
        
        # Download and analyze primary mode
        print("\n" + "=" * 60)
        print("PRIMARY EXPORT (Tilde Mode)")
        print("=" * 60)
        
        data = gps.download(mode=DownloadMode.TILDE, save_raw=True)
        
        if data:
            stats = analyze_track_data(data)
            print(f"\nDownload Statistics:")
            print(f"  Size: {stats['size_bytes']:,} bytes")
            print(f"  Tracks: {stats['track_count']}")
            print(f"  Coordinates: {stats['coordinates']}")
            print(f"  Avg coords/track: {stats['coordinates'] / max(stats['track_count'], 1):.1f}")
            
            # Export with split tracks
            print(f"\nExporting tracks...")
            files = gps.export_tracks(
                data=data,
                format=OutputFormat.KML,
                split_by_track=True
            )
            
            print(f"Created {len(files)} file(s):")
            for i, file in enumerate(files, 1):
                file_path = Path(file)
                size = file_path.stat().st_size if file_path.exists() else 0
                print(f"  {i}. {file_path.name} ({size:,} bytes)")
        
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Always disconnect
        if gps.serial and gps.serial.is_open:
            gps.disconnect()
            print("\nDisconnected")


if __name__ == "__main__":
    main()
