# Changelog

All notable changes to the Wanggan D6E GPS Library project.

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
