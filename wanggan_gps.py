"""
Wanggan GPS Device Communication Library

A Python library for interfacing with Wanggan handheld GPS locators.
Supports downloading GPS track data in multiple formats and converting to standard formats.

**Tested Device:** Wanggan D6E GNSS Handheld Navigator
**Compatibility:** Protocol likely compatible with other Wanggan GPS models (untested)

Author: Hélio Teixeira
License: MIT
Repository: https://github.com/yourusername/wanggan-gps-python

Supported Features:
- Three download modes (Tilde, Exclamation, Caret)
- Four data types (Track, Area, Distance, Waypoint)
- Multiple output formats (GPX, KML, CSV, RAW)
- Automatic track splitting by headers
- DMS to decimal degree conversion
- Timestamp parsing and metadata extraction

Requirements:
- pyserial >= 3.5
- Python >= 3.8
"""

import serial
import time
import os
import re
from typing import Optional, List, Tuple, Dict
from enum import Enum
from pathlib import Path
import json


class DownloadMode(Enum):
    """GPS data download modes based on firmware trigger bytes"""
    TILDE = 0x7E        # '~' - Full track export with headers
    EXCLAMATION = 0x21  # '!' - Bulk coordinate dump without headers
    CARET = 0x5E        # '^' - Binary metadata export


class OutputFormat(Enum):
    """Output file formats"""
    GPX = "gpx"
    KML = "kml"
    CSV = "csv"
    RAW = "raw"  # Raw text as received from device


class WangganGPS:
    """
    Communication interface for Wanggan GPS devices.
    
    **Tested on:** Wanggan D6E GNSS Handheld Navigator
    **Compatibility:** Protocol likely compatible with other Wanggan models (untested)
    
    Example usage:
        >>> gps = WangganGPS(port='COM5')
        >>> tracks = gps.download(mode=DownloadMode.TILDE)
        >>> gps.export_tracks(tracks, format=OutputFormat.KML, split_by_track=True)
    """
    
    DEFAULT_BAUDRATE = 115200
    DEFAULT_TIMEOUT = 1.0
    DOWNLOAD_TIMEOUT = 60.0
    END_MARKER = b'!'
    
    def __init__(
        self,
        port: str,
        baudrate: int = DEFAULT_BAUDRATE,
        timeout: float = DEFAULT_TIMEOUT,
        output_dir: str = "downloads",
        auto_create_dir: bool = True
    ):
        """
        Initialize Wanggan GPS device connection.
        
        Tested on: Wanggan D6E GNSS Handheld Navigator
        
        Args:
            port: Serial port name (e.g., 'COM5' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Communication speed (default: 115200)
            timeout: Serial port timeout in seconds
            output_dir: Directory for exported files
            auto_create_dir: Automatically create output directory if it doesn't exist
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.output_dir = Path(output_dir)
        self.serial_conn: Optional[serial.Serial] = None
        
        if auto_create_dir:
            self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def connect(self) -> bool:
        """
        Open serial connection to the GPS device.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.serial_conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            time.sleep(2)  # Wait for port to stabilize
            return True
        except Exception as e:
            print(f"✗ Connection error: {e}")
            return False
    
    def disconnect(self) -> None:
        """Close serial connection."""
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.close()
    
    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
    
    def send_trigger(self, mode: DownloadMode) -> bool:
        """
        Send download trigger byte to device.
        
        Args:
            mode: Download mode (TILDE, EXCLAMATION, or CARET)
        
        Returns:
            True if trigger sent successfully
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            print("✗ Device not connected")
            return False
        
        try:
            self.serial_conn.reset_input_buffer()
            self.serial_conn.write(bytes([mode.value]))
            self.serial_conn.flush()
            return True
        except Exception as e:
            print(f"✗ Error sending trigger: {e}")
            return False
    
    def receive_data(self, timeout: float = DOWNLOAD_TIMEOUT, idle_timeout: float = 3.0) -> Optional[bytes]:
        """
        Receive data from device after trigger.
        Stream ends when device stops sending data (idle_timeout seconds of silence).
        Note: '!' marks end of each track. Device stops when no more tracks exist.
        
        Args:
            timeout: Maximum time to wait for data (seconds)
            idle_timeout: Time to wait with no data before considering stream ended (seconds)
        
        Returns:
            Raw bytes received from device, or None on error
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            print("✗ Device not connected")
            return None
        
        # Give device a moment to start transmitting
        time.sleep(0.2)
        
        start_time = time.time()
        last_data_time = None  # Track when we last received data
        all_data = b''
        chunks_received = 0
        
        while time.time() - start_time < timeout:
            if self.serial_conn.in_waiting:
                chunk = self.serial_conn.read(self.serial_conn.in_waiting)
                all_data += chunk
                chunks_received += 1
                last_data_time = time.time()  # Reset idle timer
                
                # Debug: Show progress for large downloads
                if chunks_received % 10 == 0:
                    print(f"  Received {len(all_data)} bytes so far...", end='\r')
            else:
                # Only check idle timeout if we've actually received data
                if last_data_time and (time.time() - last_data_time) >= idle_timeout:
                    print(f"\n  Stream idle for {idle_timeout}s, ending reception")
                    break
            
            time.sleep(0.05)
        
        if chunks_received > 0:
            print(f"\n  Total: {chunks_received} chunks, {len(all_data)} bytes")
        
        return all_data if all_data else None
    
    def download(
        self,
        mode: DownloadMode = DownloadMode.TILDE,
        save_raw: bool = False,
        raw_filename: Optional[str] = None
    ) -> Optional[bytes]:
        """
        Download GPS data from device.
        
        Args:
            mode: Download mode (default: TILDE for full tracks with headers)
            save_raw: Save raw data to file
            raw_filename: Custom filename for raw data (auto-generated if None)
        
        Returns:
            Raw data bytes, or None on error
        """
        if not self.serial_conn or not self.serial_conn.is_open:
            if not self.connect():
                return None
        
        print(f"📡 Sending {mode.name} trigger (0x{mode.value:02X})...")
        if not self.send_trigger(mode):
            return None
        
        print("📥 Receiving data...")
        data = self.receive_data()
        
        if data:
            print(f"✓ Received {len(data)} bytes")
            
            if save_raw or raw_filename:
                if raw_filename is None:
                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    raw_filename = f"gps_export_{mode.name.lower()}_{timestamp}.txt"
                
                raw_path = self.output_dir / raw_filename
                with open(raw_path, 'wb') as f:
                    f.write(data)
                print(f"✓ Raw data saved: {raw_path}")
        else:
            print("✗ No data received")
        
        return data
    
    @staticmethod
    def parse_dms_coordinate(dms_str: str) -> Optional[float]:
        """
        Parse DMS coordinate to decimal degrees.
        
        Args:
            dms_str: DMS string like "-008d35'28.86540\""
        
        Returns:
            Decimal degrees, or None if parse fails
        """
        match = re.match(r'([+-])(\d+)d(\d+)\'(\d+\.\d+)"', dms_str)
        if not match:
            return None
        
        sign_str, degrees, minutes, seconds = match.groups()
        sign = -1 if sign_str == '-' else 1
        
        decimal = sign * (float(degrees) + float(minutes)/60 + float(seconds)/3600)
        return decimal
    
    @staticmethod
    def parse_track_line(line: str) -> Optional[Tuple[float, float, int]]:
        """
        Parse track coordinate line.
        
        Args:
            line: Line like "-008d35'28.86540\",+41d06'52.58100\",01769;"
        
        Returns:
            Tuple of (longitude, latitude, altitude), or None if parse fails
        """
        match = re.match(r'([+-]\d+d\d+\'\d+\.\d+")\,([+-]\d+d\d+\'\d+\.\d+")\,(\d+);', line)
        if not match:
            return None
        
        lon_str, lat_str, alt_str = match.groups()
        
        lon = WangganGPS.parse_dms_coordinate(lon_str)
        lat = WangganGPS.parse_dms_coordinate(lat_str)
        
        if lon is None or lat is None:
            return None
        
        return (lon, lat, int(alt_str))
    
    @staticmethod
    def parse_header_line(line: str) -> Optional[Dict[str, any]]:
        """
        Parse header line for different data types.
        
        Formats:
        - Area:     n####,m##########,l##########;t############,N####
        - Distance: n####,l##########,m##########;t############,N####
        - Waypoint: n####,p##########,p##########;t############,N####
        - Track:    n####,k##########,l##########;t############,N####
        
        Args:
            line: Header line from device
        
        Returns:
            Dictionary with metadata including 'type', or None if parse fails
        """
        # Pattern: n####,X##########,Y##########;t############,N####
        # where X,Y can be: m/l (Area), l/m (Distance), p/p (Waypoint), k/l (Track)
        match = re.match(r'n(\d+),([a-z])(\d+),([a-z])(\d+);t(\d+),N(\d+)', line)
        if not match:
            return None
        
        record_num, field1, value1, field2, value2, timestamp, total = match.groups()
        
        # Determine data type and extract coordinates
        data_type = None
        latitude = None
        longitude = None
        
        if field1 == 'm' and field2 == 'l':
            data_type = 'Area'
            latitude = int(value1) / 10000000.0
            longitude = int(value2) / 10000000.0
        elif field1 == 'l' and field2 == 'm':
            data_type = 'Distance'
            longitude = int(value1) / 10000000.0
            latitude = int(value2) / 10000000.0
        elif field1 == 'p' and field2 == 'p':
            data_type = 'Waypoint'
            # Waypoints use p fields (purpose unclear, may be zero)
            latitude = int(value1) / 10000000.0
            longitude = int(value2) / 10000000.0
        elif field1 == 'k' and field2 == 'l':
            data_type = 'Track'
            # k field purpose unclear (may be track parameter)
            longitude = int(value2) / 10000000.0
            latitude = 0.0  # Will be determined from actual track points
        else:
            # Unknown format
            data_type = f'Unknown({field1},{field2})'
            latitude = 0.0
            longitude = 0.0
        
        # Parse timestamp: YYYYMMDDHHMM
        year = timestamp[:4]
        month = timestamp[4:6]
        day = timestamp[6:8]
        hour = timestamp[8:10]
        minute = timestamp[10:12]
        
        return {
            'type': data_type,
            'record_num': int(record_num),
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': f'{year}-{month}-{day} {hour}:{minute}',
            'total_records': int(total)
        }
    
    @staticmethod
    def parse_raw_data(data: bytes) -> List[Tuple[Optional[Dict], List[Tuple[float, float, int]]]]:
        """
        Parse raw GPS data into tracks.
        
        Args:
            data: Raw bytes from device
        
        Returns:
            List of (header_dict, points_list) tuples
        """
        text = data.decode('ascii', errors='ignore')
        tracks = []
        current_header = None
        current_points = []
        
        for line in text.split('\n'):
            line = line.strip()
            if not line or line == '!':
                continue
            
            # Try to parse as header
            header = WangganGPS.parse_header_line(line)
            if header:
                # Save previous track
                if current_header is not None or current_points:
                    tracks.append((current_header, current_points))
                # Start new track
                current_header = header
                current_points = []
                continue
            
            # Try to parse as coordinate
            point = WangganGPS.parse_track_line(line)
            if point:
                current_points.append(point)
        
        # Don't forget last track
        if current_header is not None or current_points:
            tracks.append((current_header, current_points))
        
        return tracks
    
    def export_to_kml(
        self,
        points: List[Tuple[float, float, int]],
        output_file: Path,
        track_name: str = "GPS Track",
        timestamp: str = ""
    ) -> None:
        """Export track points to KML format."""
        display_name = f"{track_name} - {timestamp}" if timestamp else track_name
        
        kml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{display_name}</name>
    <Placemark>
      <name>{display_name}</name>'''
        
        if timestamp:
            kml_content += f'''
      <TimeStamp>
        <when>{timestamp.replace(' ', 'T')}:00Z</when>
      </TimeStamp>'''
        
        kml_content += '''
      <LineString>
        <coordinates>
'''
        
        for lon, lat, alt in points:
            kml_content += f'          {lon:.7f},{lat:.7f},{alt}\n'
        
        kml_content += '''        </coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(kml_content)
        
        print(f"✓ KML saved: {output_file}")
    
    def export_to_gpx(
        self,
        points: List[Tuple[float, float, int]],
        output_file: Path,
        track_name: str = "GPS Track"
    ) -> None:
        """Export track points to GPX format."""
        gpx_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Wanggan GPS Python Library"
  xmlns="http://www.topografix.com/GPX/1/1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <trk>
    <name>{track_name}</name>
    <trkseg>
'''
        
        for lon, lat, alt in points:
            gpx_content += f'      <trkpt lat="{lat:.7f}" lon="{lon:.7f}">\n'
            gpx_content += f'        <ele>{alt}</ele>\n'
            gpx_content += f'      </trkpt>\n'
        
        gpx_content += '''    </trkseg>
  </trk>
</gpx>
'''
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(gpx_content)
        
        print(f"✓ GPX saved: {output_file}")
    
    def export_to_csv(
        self,
        points: List[Tuple[float, float, int]],
        output_file: Path
    ) -> None:
        """Export track points to CSV format."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('longitude,latitude,altitude\n')
            for lon, lat, alt in points:
                f.write(f'{lon:.7f},{lat:.7f},{alt}\n')
        
        print(f"✓ CSV saved: {output_file}")
    
    def export_tracks(
        self,
        data: bytes,
        format: OutputFormat = OutputFormat.KML,
        split_by_track: bool = False,
        filename_prefix: str = "track"
    ) -> List[Path]:
        """
        Export GPS data to specified format.
        
        Args:
            data: Raw GPS data bytes
            format: Output format (GPX, KML, CSV, or RAW)
            split_by_track: Create separate files for each track (only for TILDE mode)
            filename_prefix: Prefix for output filenames
        
        Returns:
            List of created file paths
        """
        if format == OutputFormat.RAW:
            raw_path = self.output_dir / f"{filename_prefix}.txt"
            with open(raw_path, 'wb') as f:
                f.write(data)
            print(f"✓ Raw data saved: {raw_path}")
            return [raw_path]
        
        tracks = self.parse_raw_data(data)
        created_files = []
        
        if split_by_track and any(h is not None for h, p in tracks):
            # Create separate file for each track
            for idx, (header, points) in enumerate(tracks):
                if not points:
                    continue
                
                if header:
                    # Include data type in filename
                    data_type = header.get('type', 'Unknown').lower()
                    track_id = f"n{header['record_num']:04d}"
                    timestamp = header['timestamp'].replace('-', '').replace(' ', '_').replace(':', '')
                    file_base = f"{data_type}_{track_id}_{timestamp}"
                    track_name = f"{header.get('type', 'Track')} {header['record_num']}"
                    track_timestamp = header['timestamp']
                else:
                    file_base = f"{filename_prefix}_{idx+1:04d}"
                    track_name = f"Track {idx+1}"
                    track_timestamp = ""
                
                output_file = self.output_dir / f"{file_base}.{format.value}"
                
                if format == OutputFormat.KML:
                    self.export_to_kml(points, output_file, track_name, track_timestamp)
                elif format == OutputFormat.GPX:
                    self.export_to_gpx(points, output_file, track_name)
                elif format == OutputFormat.CSV:
                    self.export_to_csv(points, output_file)
                
                created_files.append(output_file)
        else:
            # Single file with all tracks
            all_points = []
            for header, points in tracks:
                all_points.extend(points)
            
            output_file = self.output_dir / f"{filename_prefix}.{format.value}"
            
            if format == OutputFormat.KML:
                self.export_to_kml(all_points, output_file)
            elif format == OutputFormat.GPX:
                self.export_to_gpx(all_points, output_file)
            elif format == OutputFormat.CSV:
                self.export_to_csv(all_points, output_file)
            
            created_files.append(output_file)
        
        return created_files
    
    def download_and_export(
        self,
        mode: DownloadMode = DownloadMode.TILDE,
        format: OutputFormat = OutputFormat.KML,
        split_by_track: bool = False,
        save_raw: bool = False
    ) -> List[Path]:
        """
        Convenience method to download and export in one call.
        
        Args:
            mode: Download mode
            format: Output format
            split_by_track: Create separate files per track
            save_raw: Also save raw data
        
        Returns:
            List of created file paths
        """
        data = self.download(mode=mode, save_raw=save_raw)
        if not data:
            return []
        
        return self.export_tracks(data, format=format, split_by_track=split_by_track)


if __name__ == "__main__":
    # Example usage
    print("Wanggan GPS Python Library - Example Usage\n")
    
    # Example 1: Download with context manager
    with WangganGPS(port='COM5', output_dir='downloads') as gps:
        # Download full tracks (TILDE mode) and export to KML
        data = gps.download(mode=DownloadMode.TILDE, save_raw=True)
        if data:
            gps.export_tracks(data, format=OutputFormat.KML, split_by_track=True)
    
    # Example 2: Download bulk coordinates (EXCLAMATION mode)
    gps = WangganGPS(port='COM5')
    if gps.connect():
        files = gps.download_and_export(
            mode=DownloadMode.EXCLAMATION,
            format=OutputFormat.CSV,
            save_raw=True
        )
        print(f"Created {len(files)} file(s)")
        gps.disconnect()


# Backwards compatibility alias
WangganD6E = WangganGPS
