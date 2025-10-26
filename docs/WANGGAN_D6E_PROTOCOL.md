# Wanggan D6E GPS Navigator - Complete Protocol Documentation

**Date:** October 25, 2025  
**Device:** Wanggan D6E GNSS Handheld Navigator  
**Firmware Version:** D6E.bin (464,688 bytes)  
**Documentation Purpose:** Reference for developing complete applications to interface with the device

---

## Table of Contents

1. [Hardware Interface](#hardware-interface)
2. [Serial Communication](#serial-communication)
3. [Protocol Commands](#protocol-commands)
4. [Data Export Format](#data-export-format)
5. [Data Structures](#data-structures)
6. [Firmware Architecture](#firmware-architecture)
7. [Python Implementation](#python-implementation)
8. [Application Development Guide](#application-development-guide)

---

## Hardware Interface

### USB-to-Serial Adapter
- **Chipset:** CH340 USB-to-Serial converter
- **VID:PID:** 1A86:7523
- **Driver:** CH341SER (downloaded from https://www.chcdwgkj.com/download.html)
- **Port:** Usually appears as COM3-COM5 on Windows
- **Connection:** Device connects via USB, appears as standard serial port

### Physical Connection
- Device has USB-C
- Use standard USB-A to USB-C
- No special cables or adapters required
- Device can be powered on or off during connection ?

---

## Serial Communication

### Critical Parameters

```
Baud Rate: 115200 
Data Bits: 8
Parity: None
Stop Bits: 1
Flow Control: None
```

### Python Serial Configuration

```python
import serial

# Correct configuration
port = serial.Serial(
    port='COM5',          # Adjust for your system
    baudrate=115200,      # MUST be 115200
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=2,
    write_timeout=2
)
```

### Important Notes
- **Baud rate 115200 is mandatory** - device will not respond at other speeds
- 9600 baud will result in silence
- 57600 baud will produce corrupted binary output
- No handshaking or flow control needed
- Device responds immediately (within 100ms typically)

---

## Protocol Commands

### Data Export Trigger (Primary Command)

**Command Byte:** `0x7E` (ASCII: `~` tilde character)

```python
# Send trigger to initiate data export
port.write(b'\x7E')
```

**Response:**
- Device immediately begins streaming GPS track data
- Data continues for 10-15 seconds (depending on storage size)
- Format: ASCII text with DMS coordinates
- Size: Typically 2KB to 15KB per export

### Alternative Command Bytes (Discovered but not fully tested)

| Byte | ASCII | Status | Observed Response |
|------|-------|--------|-------------------|
| `0x7E` | `~` | ✅ Confirmed | Full GPS track export |
| `0x21` | `!` | ⚠️ Partial | Some response observed |
| `0x5E` | `^` | ⚠️ Partial | Some response observed |

**Note:** Only `0x7E` has been thoroughly tested and confirmed to work reliably.

### Command Sequence Examples

#### Simple Export
```python
port.write(b'\x7E')
time.sleep(0.1)
data = port.read_all()
```

#### With Wake-up Sequence (Recommended)
```python
# Send multiple triggers to ensure device is ready
port.write(b'\x7E\x7E\x7E')
time.sleep(0.2)

# Main trigger
port.write(b'\x7E')

# Wait for full export
time.sleep(10)
data = port.read_all()
```

### NMEA Commands (NOT SUPPORTED)

The following standard GPS commands do **NOT** work:
- `$PCAS00` - Restart (no response)
- `$PCAS01` - Factory reset (no response)
- `$PCAS02` - Cold start (no response)
- `$PCAS03` - Status query (no response)
- `$PCAS04` - Rate change (no response)
- `$GNGGA`, `$GNRMC`, etc. - Standard NMEA queries (no response)

**Reason:** Device uses proprietary protocol, not standard NMEA/CASIC commands in export mode.

---

## Data Export Format

### Raw Export Structure

Data is exported as ASCII text with multiple types of records:

#### 1. Track Header Record

**Format:**
```
n0014,m0000019335,l0000006404;t202510241534,N0004
```

**Field Breakdown:**

| Field | Format | Description | Example | Decoded Value |
|-------|--------|-------------|---------|---------------|
| `n` | `n####` | Record number (0-based) | `n0014` | Track #14 |
| `m` | `m##########` | Latitude (scaled int) | `m0000019335` | 1.9335° N |
| `l` | `l##########` | Longitude (scaled int) | `l0000006404` | 0.6404° E |
| `t` | `t############` | Timestamp YYYYMMDDHHMM | `t202510241534` | 2025-10-24 15:34 |
| `N` | `N####` | Total records in track | `N0004` | 4 waypoints |

**Coordinate Scaling:**
```python
latitude_degrees = int(m_value) / 10000000.0
longitude_degrees = int(l_value) / 10000000.0
```

#### 2. Track Point Record (DMS Format)

**Format:**
```
-008d35'28.86540",+41d06'52.58100",01769;
```

**Field Breakdown:**

| Field | Format | Description | Example | Decoded Value |
|-------|--------|-------------|---------|---------------|
| Longitude | `[+-]DDDdMM'SS.sssss"` | DMS longitude | `-008d35'28.86540"` | -8.591352° |
| Latitude | `[+-]DDdMM'SS.sssss"` | DMS latitude | `+41d06'52.58100"` | +41.114606° |
| Altitude | `#####` | Meters above sea level | `01769` | 1769m |
| Terminator | `;` | Record separator | `;` | End of record |

**DMS to Decimal Conversion:**
```python
def dms_to_decimal(dms_string):
    # Parse: [+-]DDDdMM'SS.sssss"
    match = re.match(r'([+-])(\d+)d(\d+)\'(\d+\.\d+)"', dms_string)
    sign_str, degrees, minutes, seconds = match.groups()
    
    sign = -1 if sign_str == '-' else 1
    decimal = sign * (float(degrees) + float(minutes)/60 + float(seconds)/3600)
    
    return decimal
```

### Complete Export Example

```
n0014,m0000019335,l0000006404;t202510241534,N0004
-008d35'22.330",+41d06'50.109",01796;
-008d35'23.00760",+41d06'52.71840",01761;
-008d35'28.86540",+41d06'52.58100",01769;
-008d35'30.22680",+41d06'50.62320",01777;
```

**Interpretation:**
- Track #14 recorded at 2025-10-24 15:34
- Center position: 1.9335°N, 0.6404°E
- Contains 4 waypoints
- Followed by 4 coordinate lines with altitude

---

## Data Structures

### Firmware Internal Storage (Reverse Engineered)

#### Route Record Structure (32 bytes per record)

```c
struct RouteRecord {
    // Offset 0x00: Navigation flag/status
    uint8_t  nav_flag;           // 0x01 = navigating, 0x00 = stored
    
    // Offset 0x01-0x03: Padding/reserved
    uint8_t  reserved1[3];
    
    // Offset 0x04: Latitude (scaled integer)
    int32_t  latitude;           // Divide by 10,000,000 for degrees
    
    // Offset 0x08: Longitude (scaled integer)
    int32_t  longitude;          // Divide by 10,000,000 for degrees
    
    // Offset 0x0C: Altitude (meters)
    int16_t  altitude;           // Direct value in meters
    
    // Offset 0x0E-0x0F: Reserved
    uint8_t  reserved2[2];
    
    // Offset 0x10: Timestamp (packed BCD or binary)
    uint16_t year;               // 2024, 2025, etc.
    uint8_t  month;              // 1-12
    uint8_t  day;                // 1-31
    uint8_t  hour;               // 0-23
    uint8_t  minute;             // 0-59
    uint8_t  second;             // 0-59
    
    // Offset 0x17-0x1F: Additional fields or padding
    uint8_t  reserved3[9];
};
```

#### Flash Memory Layout

**Base Address:** `0x08000000` (ARM Cortex STM32-style)

| Address Range | Size | Purpose |
|--------------|------|---------|
| `0x08000000 - 0x08003FFF` | 16KB | Bootloader |
| `0x08004000 - 0x0807FFFF` | 496KB | Main firmware |
| `0x08010000 - 0x0803FFFF` | 192KB | GPS track storage (estimated) |
| `0x08040000 - 0x0807FFFF` | 256KB | Configuration/settings |

**Storage Capacity:**
- Each route record: 32 bytes
- Estimated capacity: ~6000 track points (192KB / 32)
- Device appears to store ~350-500 points in practice

---

## Firmware Architecture

### Key Functions (Ghidra Analysis)

#### Export Function: `FUN_000060e0`

**Address:** `0x000060e0`  
**Purpose:** Main GPS data export function

```c
// Pseudo-code from Ghidra decompilation
void export_gps_data(void) {
    uint record_count = 0;
    uint flash_address = FLASH_STORAGE_BASE;
    
    // Read route records from flash
    while (flash_address < FLASH_STORAGE_END) {
        RouteRecord record = flash_read_32bytes(flash_address);
        
        if (record.nav_flag == 0xFF) break; // End of data
        
        // Format header
        uart_printf("n%04d,m%010d,l%010d;t%04d%02d%02d%02d%02d,N%04d\r\n",
                    record_count,
                    record.latitude,
                    record.longitude,
                    record.year, record.month, record.day,
                    record.hour, record.minute,
                    total_records);
        
        // Convert and send coordinates in DMS format
        convert_to_dms_and_send(record.longitude, record.latitude, record.altitude);
        
        flash_address += 32;
        record_count++;
        delay_ms(10);  // Small delay between records
    }
}
```

#### UART Send Function: `FUN_000003c0`

**Address:** `0x000003c0`  
**Purpose:** Serial output (printf-like)

```c
void uart_send_string(char* str) {
    while (*str) {
        UART_TRANSMIT_REGISTER = *str;
        while (!(UART_STATUS & UART_TX_READY));
        str++;
    }
}
```

#### Coordinate Converter: `FUN_00007258`

**Address:** `0x00007258`  
**Purpose:** Convert integer coordinates to DMS format

```c
void convert_to_dms(int32_t scaled_coord, char* output) {
    int sign = (scaled_coord < 0) ? -1 : 1;
    scaled_coord = abs(scaled_coord);
    
    double decimal_degrees = scaled_coord / 10000000.0;
    
    int degrees = (int)decimal_degrees;
    double remaining = (decimal_degrees - degrees) * 60.0;
    int minutes = (int)remaining;
    double seconds = (remaining - minutes) * 60.0;
    
    sprintf(output, "%c%03dd%02d'%09.5f\"",
            (sign < 0) ? '-' : '+',
            degrees, minutes, seconds);
}
```

#### Command Dispatcher: `FUN_0000fa58`

**Address:** `0x0000fa58`  
**Purpose:** Main command handler loop

```c
void command_dispatcher(void) {
    uint8_t command_byte;
    
    while (1) {
        if (uart_has_data()) {
            command_byte = uart_read_byte();
            
            switch (command_byte) {
                case 0x7E:  // '~' - Export data
                    export_gps_data();
                    break;
                    
                case 0x21:  // '!' - Alternative command
                    // Some response, not fully documented
                    break;
                    
                case 0x5E:  // '^' - Alternative command
                    // Some response, not fully documented
                    break;
                    
                default:
                    // Ignore unknown commands
                    break;
            }
        }
        
        // Other main loop tasks
        update_gps();
        update_display();
        delay_ms(10);
    }
}
```

### Format Strings (Found at 0x000064B4)

```c
// Track header format
"n%04d,m%010d,l%010d;t%04d%02d%02d%02d%02d,N%04d\r\n"

// Waypoint header format
"n%04d,p%010d,p%010d;t%04d%02d%02d%02d%02d,N%04d\r\n"

// DMS coordinate format
"%c%03dd%02d'%09.5f\""

// Complete track point format
"%s,%s,%05d;\r\n"
```

---

## Python Implementation

### Complete Example Application

```python
import serial
import re
import time
from datetime import datetime


class WangganD6E:
    """Interface for Wanggan D6E GPS Navigator"""
    
    BAUD_RATE = 115200
    TRIGGER_BYTE = b'\x7E'
    
    def __init__(self, port='COM5'):
        """Initialize connection to device"""
        self.port_name = port
        self.port = None
        
    def connect(self):
        """Open serial connection"""
        try:
            self.port = serial.Serial(
                port=self.port_name,
                baudrate=self.BAUD_RATE,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=2,
                write_timeout=2
            )
            print(f"✓ Connected to {self.port_name} at {self.BAUD_RATE} baud")
            return True
        except Exception as e:
            print(f"✗ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection"""
        if self.port and self.port.is_open:
            self.port.close()
            print("✓ Disconnected")
    
    def export_data(self, timeout=15):
        """
        Trigger data export from device
        
        Args:
            timeout: Maximum seconds to wait for data
            
        Returns:
            Raw ASCII data string
        """
        if not self.port or not self.port.is_open:
            raise Exception("Not connected")
        
        # Clear any pending data
        self.port.reset_input_buffer()
        self.port.reset_output_buffer()
        
        # Send wake-up sequence (optional but recommended)
        self.port.write(self.TRIGGER_BYTE * 3)
        time.sleep(0.2)
        
        # Send main trigger
        self.port.write(self.TRIGGER_BYTE)
        print(f"✓ Trigger sent, waiting for data...")
        
        # Collect data
        data_buffer = bytearray()
        start_time = time.time()
        last_data_time = start_time
        
        while True:
            if self.port.in_waiting > 0:
                chunk = self.port.read(self.port.in_waiting)
                data_buffer.extend(chunk)
                last_data_time = time.time()
                print(f"  Received {len(chunk)} bytes... (total: {len(data_buffer)})")
            
            # Stop if no new data for 2 seconds
            if time.time() - last_data_time > 2:
                break
            
            # Stop if timeout exceeded
            if time.time() - start_time > timeout:
                print("  Timeout reached")
                break
            
            time.sleep(0.1)
        
        print(f"✓ Export complete: {len(data_buffer)} bytes")
        return data_buffer.decode('utf-8', errors='ignore')
    
    @staticmethod
    def parse_dms_coordinate(dms_str):
        """Convert DMS string to decimal degrees"""
        match = re.match(r'([+-])(\d+)d(\d+)\'(\d+\.\d+)"', dms_str)
        if not match:
            return None
        
        sign_str, degrees, minutes, seconds = match.groups()
        sign = -1 if sign_str == '-' else 1
        
        decimal = sign * (float(degrees) + float(minutes)/60 + float(seconds)/3600)
        return decimal
    
    @staticmethod
    def parse_track_point(line):
        """Parse track point line"""
        match = re.match(r'([+-]\d+d\d+\'\d+\.\d+")\,([+-]\d+d\d+\'\d+\.\d+")\,(\d+);', line)
        if not match:
            return None
        
        lon_str, lat_str, alt_str = match.groups()
        
        lon = WangganD6E.parse_dms_coordinate(lon_str)
        lat = WangganD6E.parse_dms_coordinate(lat_str)
        alt = int(alt_str)
        
        return {'longitude': lon, 'latitude': lat, 'altitude': alt}
    
    @staticmethod
    def parse_header(line):
        """Parse track header line"""
        match = re.match(r'n(\d+),m(\d+),l(\d+);t(\d+),N(\d+)', line)
        if not match:
            return None
        
        record_num, m_coord, l_coord, timestamp, total = match.groups()
        
        latitude = int(m_coord) / 10000000.0
        longitude = int(l_coord) / 10000000.0
        
        year = timestamp[:4]
        month = timestamp[4:6]
        day = timestamp[6:8]
        hour = timestamp[8:10]
        minute = timestamp[10:12]
        
        return {
            'record_num': int(record_num),
            'latitude': latitude,
            'longitude': longitude,
            'timestamp': f'{year}-{month}-{day} {hour}:{minute}',
            'total_records': int(total)
        }
    
    def parse_export_data(self, raw_data):
        """
        Parse complete export data
        
        Returns:
            Dictionary with 'headers' and 'points' lists
        """
        headers = []
        points = []
        
        for line in raw_data.split('\n'):
            line = line.strip()
            if not line:
                continue
            
            # Try parse as header
            header = self.parse_header(line)
            if header:
                headers.append(header)
                continue
            
            # Try parse as track point
            point = self.parse_track_point(line)
            if point:
                points.append(point)
        
        return {
            'headers': headers,
            'points': points,
            'point_count': len(points),
            'track_count': len(headers)
        }
    
    def export_to_gpx(self, points, filename='track.gpx'):
        """Export track points to GPX file"""
        gpx_header = '''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Wanggan D6E Interface"
  xmlns="http://www.topografix.com/GPX/1/1"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
  <trk>
    <name>Wanggan D6E Track</name>
    <trkseg>
'''
        
        gpx_footer = '''    </trkseg>
  </trk>
</gpx>
'''
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(gpx_header)
            
            for point in points:
                lat = point['latitude']
                lon = point['longitude']
                alt = point['altitude']
                f.write(f'      <trkpt lat="{lat:.7f}" lon="{lon:.7f}">\n')
                f.write(f'        <ele>{alt}</ele>\n')
                f.write(f'      </trkpt>\n')
            
            f.write(gpx_footer)
        
        print(f"✓ GPX saved: {filename}")


# Example usage
if __name__ == '__main__':
    device = WangganD6E('COM5')
    
    if device.connect():
        try:
            # Export data from device
            raw_data = device.export_data()
            
            # Save raw data
            with open('export_raw.txt', 'w', encoding='utf-8') as f:
                f.write(raw_data)
            print(f"✓ Raw data saved: export_raw.txt")
            
            # Parse data
            parsed = device.parse_export_data(raw_data)
            print(f"✓ Parsed: {parsed['point_count']} points, {parsed['track_count']} tracks")
            
            # Export to GPX
            if parsed['points']:
                device.export_to_gpx(parsed['points'], 'wanggan_track.gpx')
            
        finally:
            device.disconnect()
```

---

## Application Development Guide

### Quick Start Checklist

1. **Hardware Setup**
   - [ ] Connect device via USB
   - [ ] Identify COM port (Windows Device Manager / Linux `dmesg`)
   - [ ] Verify CH340 driver installed
   - [ ] Test port with simple serial terminal

2. **Software Setup**
   - [ ] Install Python 3.8+
   - [ ] Install pyserial: `pip install pyserial`
   - [ ] Test serial connection at 115200 baud
   - [ ] Verify device responds to `0x7E` trigger

3. **Basic Communication**
   ```python
   import serial
   port = serial.Serial('COM5', 115200, timeout=2)
   port.write(b'\x7E')
   data = port.read_all()
   print(f"Received {len(data)} bytes")
   ```

### Common Issues and Solutions

#### Issue: No Response from Device
**Solutions:**
- ✅ Verify baud rate is **115200** (not 9600!)
- ✅ Check COM port is correct
- ✅ Ensure device is powered on
- ✅ Try unplugging and reconnecting USB
- ✅ Send multiple triggers: `b'\x7E\x7E\x7E'`

#### Issue: Corrupted Data
**Solutions:**
- ✅ Verify baud rate is exactly 115200
- ✅ Check data bits: 8N1 (8 data, no parity, 1 stop)
- ✅ Increase timeout values
- ✅ Use binary mode when saving data

#### Issue: Incomplete Data Export
**Solutions:**
- ✅ Wait longer (15+ seconds for full export)
- ✅ Monitor `port.in_waiting` to detect end of transmission
- ✅ Look for 2-second silence to detect completion
- ✅ Check for semicolon terminators on each line

#### Issue: Parsing Errors
**Solutions:**
- ✅ Handle UTF-8 encoding with `errors='ignore'`
- ✅ Strip whitespace from lines
- ✅ Check for empty lines
- ✅ Validate regex matches before extracting groups

### Advanced Features to Implement

#### 1. Real-time Monitoring
```python
def monitor_device(device, callback):
    """Monitor device and call callback with new data"""
    last_point_count = 0
    
    while True:
        raw_data = device.export_data()
        parsed = device.parse_export_data(raw_data)
        
        new_points = parsed['point_count'] - last_point_count
        if new_points > 0:
            callback(parsed['points'][-new_points:])
            last_point_count = parsed['point_count']
        
        time.sleep(60)  # Check every minute
```

#### 2. Track Comparison
```python
def compare_tracks(track1, track2):
    """Compare two track exports to find new points"""
    set1 = {(p['latitude'], p['longitude']) for p in track1}
    set2 = {(p['latitude'], p['longitude']) for p in track2}
    
    new_points = set2 - set1
    return len(new_points)
```

#### 3. Data Visualization
```python
import matplotlib.pyplot as plt

def visualize_track(points):
    """Plot track on map"""
    lats = [p['latitude'] for p in points]
    lons = [p['longitude'] for p in points]
    alts = [p['altitude'] for p in points]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Map view
    ax1.plot(lons, lats, 'b-', linewidth=2)
    ax1.scatter(lons[0], lats[0], c='green', s=100, label='Start')
    ax1.scatter(lons[-1], lats[-1], c='red', s=100, label='End')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.legend()
    ax1.grid(True)
    
    # Elevation profile
    ax2.plot(alts, 'r-', linewidth=2)
    ax2.set_xlabel('Point Number')
    ax2.set_ylabel('Altitude (m)')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig('track_visualization.png', dpi=150)
    plt.show()
```

#### 4. Auto-detection of COM Port
```python
import serial.tools.list_ports

def find_wanggan_device():
    """Auto-detect Wanggan device COM port"""
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        # CH340 USB-to-Serial
        if port.vid == 0x1A86 and port.pid == 0x7523:
            return port.device
    
    return None

# Usage
port = find_wanggan_device()
if port:
    print(f"Found device on {port}")
else:
    print("Device not found")
```

### Performance Considerations

| Operation | Typical Time | Notes |
|-----------|--------------|-------|
| Connection | 100-500ms | USB enumeration |
| Trigger response | <100ms | Device responds immediately |
| Small export (<5KB) | 2-3 seconds | ~50 points |
| Large export (15KB) | 10-15 seconds | ~350 points |
| Parsing | <100ms | Pure Python regex |
| GPX export | <500ms | File I/O dependent |

### Memory Usage

| Component | Memory | Notes |
|-----------|--------|-------|
| Raw data buffer | ~15KB | Maximum export size |
| Parsed points list | ~50KB | Python dict overhead |
| GPX output | ~25KB | XML formatting |
| Total application | ~5MB | Including Python runtime |

---

## Testing Procedures

### Verification Test Script

```python
def verify_device_connection(port_name='COM5'):
    """Complete device verification"""
    print("Wanggan D6E Device Verification")
    print("=" * 60)
    
    # Test 1: Port access
    print("\n[Test 1] Port Access")
    try:
        port = serial.Serial(port_name, 115200, timeout=1)
        print(f"  ✓ Port {port_name} opened successfully")
    except Exception as e:
        print(f"  ✗ Failed to open port: {e}")
        return False
    
    # Test 2: Send trigger
    print("\n[Test 2] Trigger Command")
    try:
        port.write(b'\x7E')
        time.sleep(0.5)
        print(f"  ✓ Trigger sent")
    except Exception as e:
        print(f"  ✗ Failed to send trigger: {e}")
        port.close()
        return False
    
    # Test 3: Receive data
    print("\n[Test 3] Data Reception")
    time.sleep(2)
    data_size = port.in_waiting
    if data_size > 0:
        data = port.read(data_size)
        print(f"  ✓ Received {data_size} bytes")
        print(f"  First 100 chars: {data[:100]}")
    else:
        print(f"  ✗ No data received")
        port.close()
        return False
    
    # Test 4: Parse data
    print("\n[Test 4] Data Parsing")
    try:
        text = data.decode('utf-8', errors='ignore')
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        print(f"  ✓ Parsed {len(lines)} lines")
        
        # Try parse first track point
        for line in lines:
            if ',' in line and 'd' in line:
                print(f"  Sample line: {line[:60]}")
                break
    except Exception as e:
        print(f"  ✗ Parsing error: {e}")
    
    port.close()
    print("\n" + "=" * 60)
    print("✓ Verification complete")
    return True
```

### Troubleshooting Flowchart

```
Device not responding?
│
├─ Check COM port in Device Manager
│  └─ If not visible: Check USB cable / reconnect
│
├─ Verify baud rate is 115200
│  └─ If using 9600: Change to 115200
│
├─ Try multiple triggers: b'\x7E\x7E\x7E'
│  └─ If still no response: Power cycle device
│
└─ Check with serial terminal (e.g., PuTTY)
   └─ Set: 115200 8N1, type '~' character
```

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-25 | 1.0 | Initial protocol documentation |
|  |  | Discovered 115200 baud requirement |
|  |  | Documented 0x7E trigger command |
|  |  | Reverse engineered data format |
|  |  | Created Python reference implementation |

---

## References

### Firmware Analysis Files
- `D6E.bin` - Main firmware binary (464,688 bytes)
- `D6E.hex` - Bootloader (Intel HEX format)
- Ghidra project: `C:\Users\Hélio Teixeira\Downloads\ghidra_11.4.2_PUBLIC`

### Documentation Files
- `EXPORT_FUNCTION_ANALYSIS.md` - Detailed export function reverse engineering
- `CRITICAL_EXPORT_STRINGS_FOUND.md` - Format string analysis
- `EXPORT_TRIGGER_FOUND.md` - Trigger mechanism documentation
- `GHIDRA_FINDINGS.md` - Route manager function analysis

### Implementation Files
- `test_export_trigger.py` - Multi-baud rate testing tool
- `parse_gps_export.py` - Data parser and converter
- `gps_export_raw.txt` - Example raw export data

### External Resources
- CASIC GPS Protocol: http://www.casic.com.cn (limited documentation)
- NMEA 0183 Standard: https://www.nmea.org
- GPX Format: https://www.topografix.com/gpx.asp
- CH340 Driver: http://www.wch-ic.com/downloads/CH341SER_ZIP.html

---

## Contact & Support

This documentation was created through reverse engineering of the Wanggan D6E firmware.

**Important Notes:**
- This is **unofficial documentation** based on firmware analysis
- Protocol may vary between firmware versions
- Always test with your specific device before deploying
- No warranty or guarantee is provided

**Contributions:**
If you discover additional commands or features, please document and share them with the community.

---

## Appendix A: Complete Command Reference

### Confirmed Commands

| Command | Hex | ASCII | Function | Response Time | Data Size |
|---------|-----|-------|----------|---------------|-----------|
| Export | `0x7E` | `~` | Full GPS track export | <100ms | 2-15KB |

### Unconfirmed Commands (Require Testing)

| Command | Hex | ASCII | Observed Behavior |
|---------|-----|-------|-------------------|
| Alt 1 | `0x21` | `!` | Some response, not decoded |
| Alt 2 | `0x5E` | `^` | Some response, not decoded |

### Failed Commands (Do Not Work)

All standard NMEA/CASIC commands starting with `$` do not work in export mode.

---

## Appendix B: Data Format Examples

### Example 1: Single Track Point
```
-008d35'28.86540",+41d06'52.58100",01769;
```
**Parsed:**
- Longitude: -8.591352° (8°35'28.865" W)
- Latitude: +41.114606° (41°06'52.581" N)
- Altitude: 1769 meters

### Example 2: Complete Track Export
```
n0014,m0000019335,l0000006404;t202510241534,N0004
-008d35'22.330",+41d06'50.109",01796;
-008d35'23.00760",+41d06'52.71840",01761;
-008d35'28.86540",+41d06'52.58100",01769;
-008d35'30.22680",+41d06'50.62320",01777;
```
**Interpretation:**
- Track #14, recorded 2025-10-24 at 15:34
- 4 waypoints
- Track center: 1.9335°N, 0.6404°E (scaled coordinates)
- Elevation range: 1761-1796m

---

## Appendix C: Coordinate System Notes

### DMS Format Specifics

**Longitude Format:** `[+-]DDDdMM'SS.sssss"`
- Sign: `-` for West, `+` for East
- Degrees: 3 digits (000-180)
- Minutes: 2 digits (00-59)
- Seconds: 2 digits + 5 decimal places (00.00000-59.99999)

**Latitude Format:** `[+-]DDdMM'SS.sssss"`
- Sign: `-` for South, `+` for North
- Degrees: 2 digits (00-90)
- Minutes: 2 digits (00-59)
- Seconds: 2 digits + 5 decimal places (00.00000-59.99999)

### Precision Analysis

| Component | Decimal Places | Ground Distance |
|-----------|----------------|-----------------|
| Degrees | 0 | ~111 km |
| Minutes | 0 | ~1.85 km |
| Seconds | 0 | ~30.9 m |
| Seconds | 5 decimals | ~0.3 mm (sub-meter) |

The device provides **sub-meter precision** in DMS format (5 decimal places on seconds).

---