# Wanggan GPS GUI Interface - User Guide

## Overview

The Wanggan GPS GUI provides a simple, intuitive graphical interface for downloading GPS data from Wanggan handheld devices. It's designed specifically for non-technical users who want to extract GPS tracks, waypoints, and other data without using command-line tools.

## Installation

### Quick Install (with GUI support)

```bash
pip install -e ".[gui]"
```

Or install just the GUI dependency:

```bash
pip install easygui
```

## Launching the GUI

### Windows
Double-click `wanggan_gps_gui.py` or run:
```bash
python wanggan_gps_gui.py
```

### Linux/Mac
```bash
python3 wanggan_gps_gui.py
```

Or use the example script:
```bash
python examples/gui_usage.py
```

## User Interface Walkthrough

### 1. Welcome Screen
- **Purpose**: Introduces the application and confirms device connection
- **Actions**: 
  - Click "Continue" to proceed to connection setup
  - Click "Settings" to adjust advanced options
  - Click "Exit" to close the application

### 2. Connection Setup
- **Purpose**: Connect to your GPS device
- **Steps**:
  1. Select your GPS device's COM port from the dropdown
     - Windows: Usually COM3, COM5, COM7, etc.
     - Linux: Usually /dev/ttyUSB0 or /dev/ttyACM0
     - Mac: Usually /dev/cu.usbserial*
  2. If your port isn't listed, select "Enter manually..."
  3. Click OK to connect
  
- **Troubleshooting**:
  - If connection fails, check that:
    - Device is powered on
    - USB cable is connected
    - No other application is using the port
    - Device drivers are installed

### 3. Download Mode Selection
Choose how to download data from your device:

#### 📋 Full Download with Details (Recommended)
- **Use when**: You want complete GPS records with all metadata
- **Includes**: Timestamps, track IDs, coordinates, and headers
- **Best for**: Most users, complete archival, analysis
- **Output**: Properly formatted tracks with metadata

#### ⚡ Quick Coordinate Download
- **Use when**: You just need GPS coordinates quickly
- **Includes**: Only coordinate data (latitude/longitude)
- **Best for**: Fast exports, simple coordinate lists
- **Output**: Bulk coordinate dump without headers

#### 🔧 Technical/Debug Mode
- **Use when**: Troubleshooting or advanced analysis
- **Includes**: Binary metadata and raw device data
- **Best for**: Developers, debugging communication issues
- **Output**: Binary and metadata files

### 4. Export Format Selection
Select one or more output formats (multiple selections allowed):

#### GPX (GPS Exchange Format)
- ✅ **Use when**: You need compatibility with GPS software
- **Compatible with**: Garmin BaseCamp, QGIS, GPSBabel, etc.
- **Contains**: Waypoints, tracks, routes with timestamps
- **File extension**: .gpx

#### KML (Keyhole Markup Language)
- 🌍 **Use when**: You want to view tracks in Google Earth
- **Compatible with**: Google Earth, Google Maps
- **Contains**: Geographic features with styling
- **File extension**: .kml

#### CSV (Comma-Separated Values)
- 📊 **Use when**: You need to analyze data in Excel
- **Compatible with**: Excel, LibreOffice, data analysis tools
- **Contains**: Tabular data (lat, lon, timestamp, etc.)
- **File extension**: .csv

#### RAW (Original Device Output)
- 📄 **Use when**: You want to preserve original data
- **Contains**: Unprocessed device output
- **Best for**: Archival, debugging, custom parsing
- **File extension**: .txt

### 5. Export Options

#### Split into Separate Files
- **Checked (default)**: Creates one file per track/waypoint
  - Example: `track_n0001.kml`, `track_n0002.kml`, etc.
  - Better for: Individual track management, selective imports
  
- **Unchecked**: Combines all data into a single file
  - Example: `gps_export_combined.kml`
  - Better for: Viewing all tracks together, bulk imports

#### Output Directory
- **Default**: `downloads` folder in application directory
- **Change**: Click "Change output directory" to select a different location
- **Note**: Folder is created automatically if it doesn't exist

### 6. Download Actions

#### ⬇️ Download & Export
- Downloads data from device
- Converts to selected format(s)
- Creates files in output directory
- **Use this** for normal operations

#### 📥 Download Only (RAW)
- Downloads data from device
- Saves only raw output (no conversion)
- Useful for troubleshooting or custom processing

#### ◀️ Back
- Returns to previous screen to change settings

#### ❌ Cancel
- Aborts operation and returns to main menu

### 7. Progress & Results

During download:
- Progress message shows download is in progress
- Wait for completion (may take 10-60 seconds depending on data size)

After completion:
- Success message shows:
  - Number of bytes downloaded
  - Number of files created
  - List of created files (first 10 shown)
- Option to open output folder
- Return to main menu for additional operations

### 8. Main Menu
After successful connection, the main menu allows:
- **📥 Download GPS Data**: Start new download operation
- **⚙️ Settings**: Adjust advanced settings
- **❓ Help**: View usage guide
- **ℹ️ About**: Device compatibility information
- **🔌 Disconnect & Exit**: Close connection and exit

## Advanced Settings

Access via "Settings" button on welcome screen or main menu.

### Baudrate
- **Default**: 115200 (recommended)
- **Change only if**: Device requires different speed
- **Common values**: 9600, 19200, 38400, 57600, 115200

### Timeout
- **Default**: 1.0 seconds
- **Change only if**: Connection is slow/unreliable
- **Range**: 0.5 - 5.0 seconds typical

### Output Directory
- **Default**: "downloads"
- **Change to**: Any folder path on your system
- **Note**: Use full path for non-local directories

### Auto-create Directory
- **Default**: Yes (enabled)
- **Change to No**: If you want to manually create folders
- **Effect**: Automatically creates output folder if missing

## File Naming Convention

### Split by Record (Default)
Files are named based on data type and record ID:
- Tracks: `track_n{ID}_YYYYMMDD_HHMM.{ext}`
  - Example: `track_n0831_20251024_1548.kml`
  
- Waypoints: `waypoint_n{ID}_YYYYMMDD_HHMM.{ext}`
  - Example: `waypoint_n0001_20251025_0039.kml`
  
- Areas: `area_n{ID}_YYYYMMDD_HHMM.{ext}`
  - Example: `area_n0014_20251024_1534.kml`
  
- Distances: `distance_n{ID}_YYYYMMDD_HHMM.{ext}`
  - Example: `distance_n0138_20251024_1603.kml`

### Combined (Single File)
- Format: `gps_export_{mode}_YYYYMMDD_HHMMSS.{ext}`
- Example: `gps_export_tilde_20251026_153045.gpx`

## Common Workflows

### Workflow 1: Download All Tracks for Google Earth
1. Launch GUI → Continue
2. Select COM port → Connect
3. Choose "Full Download with Details"
4. Select "KML" format only
5. Keep "Split into separate files" checked
6. Click "Download & Export"
7. Open output folder
8. Drag KML files into Google Earth

### Workflow 2: Export for GPS Analysis
1. Launch GUI → Continue
2. Select COM port → Connect
3. Choose "Full Download with Details"
4. Select both "GPX" and "CSV" formats
5. Click "Download & Export"
6. Open CSV in Excel for data analysis
7. Import GPX into GPS software

### Workflow 3: Quick Backup
1. Launch GUI → Continue
2. Select COM port → Connect
3. Choose "Quick Coordinate Download"
4. Select "RAW" and "CSV" formats
5. Click "Download & Export"
6. Archive files for backup

### Workflow 4: Troubleshooting Connection Issues
1. Launch GUI → Settings
2. Increase timeout to 3.0 seconds
3. Continue → Select COM port
4. If connection fails:
   - Try different COM port
   - Check Device Manager (Windows)
   - Use Technical/Debug Mode for diagnostics

## Troubleshooting

### "Could not connect to GPS device"
**Causes**:
- Device not powered on
- Wrong COM port selected
- USB cable disconnected
- Another program using the port
- Missing USB drivers

**Solutions**:
1. Check Device Manager (Windows) for COM port number
2. Close other GPS software
3. Try different USB port
4. Restart device and computer
5. Install manufacturer's USB drivers

### "No data received from device"
**Causes**:
- Device has no stored data
- Wrong download mode selected
- Device in wrong mode/menu
- Communication timeout

**Solutions**:
1. Verify device has recorded data
2. Try "Full Download with Details" mode
3. Ensure device is on main/data screen
4. Increase timeout in Settings

### "Could not save files"
**Causes**:
- Output directory doesn't exist
- No write permissions
- Disk full

**Solutions**:
1. Check output directory path
2. Enable "Auto-create directory"
3. Choose different output location
4. Check disk space

### "Import easygui could not be resolved"
**Cause**: EasyGUI library not installed

**Solution**:
```bash
pip install easygui
```

## Tips for Best Results

1. **Use Full Download Mode**: Provides the most complete data
2. **Export Multiple Formats**: Get both GPX and KML for flexibility
3. **Split Files**: Easier to manage individual tracks
4. **Regular Backups**: Download data regularly to prevent loss
5. **Check Device First**: Ensure device has data before downloading
6. **Keep RAW Copy**: Always save raw output for archival

## Keyboard Shortcuts

- **Alt+F4**: Close application (Windows)
- **Ctrl+C**: Cancel operation (in some dialogs)
- **Tab**: Navigate between options
- **Enter**: Confirm/OK
- **Esc**: Cancel (in some dialogs)

## Known Limitations

- Cannot preview data before download
- No real-time progress bar (just start/end messages)
- Cannot edit/filter data within GUI
- Single device connection at a time
- Windows COM ports only auto-detected reliably

## Support

For issues, bugs, or feature requests:
- GitHub: https://github.com/heliobteixeira/wanggan-gps-python
- Check documentation in `docs/` folder
- Review examples in `examples/` folder

## Version History

### Version 1.0.0 (Current)
- Initial GUI release
- Support for all three download modes
- Multiple export format support
- Auto-port detection
- Split/combine file options
- Settings management
- Help system

## Future Enhancements (Planned)

- Real-time progress bars
- Data preview before export
- Batch processing multiple devices
- Custom file naming templates
- Data filtering and selection
- Track preview/map view
- Automatic device detection
- Profile management for different devices
