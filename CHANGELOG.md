# Changelog

All notable changes to the Wanggan D6E GPS Library project.

## [Unreleased] - gui-development branch

### Added

#### GUI Interface (New)
- **EasyGUI-based graphical interface** (`wanggan_gps_gui.py`)
  - User-friendly interface designed for non-technical users
  - No command-line knowledge required
  - Simple point-and-click operation
  
#### GUI Features
- **Welcome Screen**: Introduction and device compatibility info
- **Connection Setup**: Auto-detection of COM ports with manual entry option
- **Download Mode Selection**: Clear descriptions of three modes:
  - Full Download with Details (Tilde mode)
  - Quick Coordinate Download (Exclamation mode)
  - Technical/Debug Mode (Caret mode)
- **Export Format Selection**: Multi-select checkboxes for GPX, KML, CSV, RAW
- **Export Options**: Split files or combine, custom output directory
- **Progress & Feedback**: Status messages and success/error dialogs
- **Advanced Settings**: Baudrate, timeout, and directory configuration
- **Help System**: Built-in usage guide and about dialog
- **Platform Support**: Works on Windows, Linux, and macOS

#### GUI Workflow
- Guided step-by-step process from connection to export
- Automatic error detection and user-friendly error messages
- Option to open output folder after successful export
- Ability to perform multiple downloads without reconnecting
- Main menu for repeated operations

#### Documentation
- Comprehensive GUI User Guide (`docs/GUI_USER_GUIDE.md`)
- GUI usage example (`examples/gui_usage.py`)
- Updated README with GUI installation instructions
- Launch scripts for Windows (`launch_gui.bat`) and Linux/Mac (`launch_gui.sh`)

#### Installation
- Added easygui as optional dependency in `setup.py`
- Install with: `pip install -e ".[gui]"`

### Changed
- Updated README.md to highlight GUI as recommended option for non-programmers
- Modified setup.py to include GUI extras requirement

### Technical Details
- Uses easygui library for cross-platform GUI dialogs
- Imports and wraps existing WangganGPS class
- No changes to core library functionality
- Handles all exceptions with user-friendly messages
- Auto-detects available serial ports
- Platform-specific folder opening (Windows/Mac/Linux)

## [1.0.0] - 2025-10-26

### Added

#### Core Features
- Three download modes support (Tilde 0x7E, Exclamation 0x21, Caret 0x5E)
- Four data type recognition and parsing:
  - **Track** (k,l header format): GPS tracks and routes
  - **Area** (m,l header format): Polygon/area measurements
  - **Distance** (l,m header format): Linear distance measurements
  - **Waypoint** (p,p header format): Single point markers
- Intelligent header parsing with automatic type detection
- Context manager support for automatic connection handling

#### Export Capabilities
- GPX (GPS Exchange Format) export
- KML (Keyhole Markup Language) export for Google Earth
- CSV (Comma-Separated Values) export
- RAW text export preserving original format
- Smart file naming with data type prefix: `{type}_{id}_{timestamp}.{ext}`
- Split-by-track option for separate files per record

#### Coordinate Processing
- Automatic DMS (Degrees, Minutes, Seconds) to decimal degrees conversion
- Support for both longitude and latitude in various orders
- Altitude preservation in all formats

#### Communication
- Serial connection management at 115200 baud
- Intelligent stream reception with idle timeout detection (3-second default)
- Progress feedback during large downloads
- Automatic buffer management
- Graceful error handling

#### Documentation
- Comprehensive README with quick start guide
- Complete API documentation in docstrings
- Three example scripts (basic, bulk, advanced)
- Export format analysis documentation
- Protocol reverse engineering details from firmware analysis

#### Testing & Examples
- `basic_usage.py`: Simple download and export example
- `bulk_download.py`: Multi-format export demonstration
- `advanced_usage.py`: All modes testing with statistics
- Test parser for validating data type recognition

### Technical Details

#### Protocol Implementation
- Based on Ghidra firmware reverse engineering
- Trigger byte identification: 0x7E (Tilde), 0x21 (Exclamation), 0x5E (Caret)
- Record separator: '!' (0x21) marks end of each data record
- Stream termination: Device stops transmitting when complete
- Command handler function: `FUN_0000fa58()` state machine
- Export functions: `FUN_000060e0()`, `FUN_0000368c(param)`

#### Data Format Analysis
- Header format: `n####,X##########,Y##########;t############,N####`
- Timestamp format: YYYYMMDDHHMM
- Coordinate scaling: Integer ÷ 10,000,000 for lat/lon
- DMS format: `±DDDdMM'SS.SSSSS"`

#### Library Architecture
- Clean enum-based API (DownloadMode, OutputFormat)
- Static parsing methods for reusability
- Separation of concerns: connection, download, parse, export
- Type hints for better IDE support
- Comprehensive error messages

### Fixed
- Stream reception now uses idle timeout instead of relying solely on end marker
- Header parsing handles all four data type formats correctly
- File naming includes data type for better organization
- Progress feedback prevents perceived hangs during large downloads

### Known Limitations
- k-field in Track headers: purpose to be determined
- p-fields in Waypoint headers: purpose to be determined
- Caret mode (0x5E) output is binary metadata, interpretation incomplete

## [Unreleased]

### Planned Features
- GUI application for non-programmers
- Real-time NMEA streaming support
- Batch processing for multiple devices
- Web-based viewer for exported tracks
- Database storage option
- Track editing and merging capabilities

---

## Version Format

This project follows [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: New functionality (backward compatible)
- PATCH: Bug fixes (backward compatible)
