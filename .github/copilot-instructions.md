# Copilot Coding Agent Instructions: Wanggan GPS Python Library

## Repository Overview

Python library for Wanggan handheld GPS locators - downloads GPS track data via serial connection and exports to GPX/KML/CSV. Protocol reverse-engineered from firmware, tested on **Wanggan D6E GNSS Handheld Navigator**.

**Type:** Python library + GUI | **Size:** ~1,400 LOC | **Languages:** Python 3.8+ | **Dependencies:** pyserial, easygui (GUI) | **Platforms:** Windows/macOS/Linux | **Status:** v1.0.0 production

## Project Structure

```
wanggan_gps_python/
├── .github/                 # GitHub metadata (you are adding to this)
├── docs/                    # Protocol documentation and user guides
│   ├── WANGGAN_D6E_PROTOCOL.md      # Reverse-engineered protocol details
│   ├── GUI_USER_GUIDE.md            # End-user GUI documentation
│   └── [other analysis docs]        # Firmware analysis and research
├── examples/                # Usage examples
│   ├── basic_usage.py       # Simple download and export
│   ├── bulk_download.py     # Multi-format export
│   ├── advanced_usage.py    # All modes testing
│   └── gui_usage.py         # GUI example
├── firmware/                # Firmware binaries and decompiled code
│   ├── D6E.bin              # Device firmware binary
│   ├── D6E.hex              # Hex format firmware
│   └── decompiled/          # Ghidra analysis output
├── wanggan_gps.py          # **MAIN MODULE** - Core library (622 lines)
├── wanggan_gps_gui.py      # GUI interface (768 lines)
├── setup.py                # Package configuration
├── launch_gui.sh           # Linux/Mac GUI launcher script
├── launch_gui.bat          # Windows GUI launcher script
├── README.md               # User documentation
├── CHANGELOG.md            # Version history
├── DEVELOPMENT_ROADMAP.md  # Future development plans
└── LICENSE                 # MIT license
```

### Key Files & Architecture

**Files:** `wanggan_gps.py` (core, 622 lines), `wanggan_gps_gui.py` (GUI, 768 lines), `setup.py` (packaging), `.gitignore` (excludes *.gpx, *.kml, output/, downloads/)

**Components:** Serial communication (WangganGPS class) → Protocol (3 modes: 0x7E/Tilde, 0x21/Exclamation, 0x5E/Caret) → Parser (4 types: Track/Area/Distance/Waypoint) → Exporters (GPX/KML/CSV/RAW) → GUI (optional)

**CI/CD:** None - no GitHub Actions, no automated tests, no linting enforcement.

## Installation & Environment

**Always use virtual environment first:**
```bash
python3 -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .  # Installs pyserial>=3.5 + wanggan_gps module (~10-15 sec)
```

**GUI support (may timeout on network issues):**
```bash
pip install -e ".[gui]"  # Adds easygui>=0.98.0, OR install separately: pip install easygui
```

**Dev tools (optional, no tests exist yet):**
```bash
pip install -e ".[dev]"  # OR individually: pip install black flake8 pytest
```

## Testing & Validation

**No build step** - Pure Python, runs directly after install. **No formal tests exist** (no tests/ dir, no pytest files).

**Manual validation:**
```bash
python -c "import wanggan_gps; print('Success')"  # Test import
python -m py_compile wanggan_gps.py  # Syntax check
flake8 wanggan_gps.py --select=E9,F63,F7,F82  # Critical errors only
```

**Hardware required** for full testing: Wanggan D6E GPS via USB serial. Examples won't work without device.

**Current linting state:** ~130 flake8 issues (E501 line length, W293 whitespace). **Don't fix unrelated issues.**

## Development Workflow

**Making Changes:**
1. Activate venv: `source venv/bin/activate`
2. Edit files: Core → `wanggan_gps.py`, GUI → `wanggan_gps_gui.py`, Package → `setup.py`
3. Test: `python -c "import wanggan_gps"` and `python -m py_compile wanggan_gps.py`
4. Lint (optional): `flake8 wanggan_gps.py --select=E9,F63,F7,F82`

**Common Issues:**
- Import errors → Activate venv
- Module not found → Reinstall: `pip install -e .`
- GUI won't start → Install: `pip install easygui`
- Serial access denied (Linux) → Add to dialout: `sudo usermod -a -G dialout $USER` (logout required)

## Critical Technical Details

**Serial:** 115200 baud (NEVER change), 1s connection timeout, 60s download timeout, end marker `0x21` ('!'), 3s idle = complete  
**Data:** Header `n####,X##########,Y##########;t############,N####`, types Track(k,l)/Area(m,l)/Distance(l,m)/Waypoint(p,p), coords DMS `±DDDdMM'SS.SSSSS"`, scaling ÷10,000,000, timestamp YYYYMMDDHHMM  
**Performance:** Downloads 10-15s (~15KB, 350pts), parsing <100ms, exports instant  
**Code:** Trigger commands in `DownloadMode` enum (lines 37-41), parsing in `parse_header_line()` / `parse_track_line()` static methods

## Documentation

**User:** README.md (quick start), docs/GUI_USER_GUIDE.md (GUI walkthrough), CHANGELOG.md (features)  
**Technical:** docs/WANGGAN_D6E_PROTOCOL.md (protocol spec), docs/EXPORT_FUNCTION_ANALYSIS.md (firmware), DEVELOPMENT_ROADMAP.md (future plans)

## Agent Guidelines

**Always:**
- Use venv before pip installs
- Install editable mode: `pip install -e .`
- Test imports: `python -c "import wanggan_gps"`
- Respect existing code style (lines >79 chars OK, whitespace in blank lines OK)
- Check protocol docs (docs/WANGGAN_D6E_PROTOCOL.md) for protocol questions

**Never:**
- Fix unrelated linting (focus on your changes only)
- Add tests unless asked (no infrastructure)
- Change 115200 baud rate (hardcoded requirement)
- Modify .gitignore carelessly (excludes important generated files)
- Assume hardware available (validate without GPS)

**Search only if** these instructions are incomplete/incorrect. Don't search for structure, install steps, or file locations - they're documented here.
