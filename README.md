# Wanggan GPS Python Library

[![Status](https://img.shields.io/badge/status-production-brightgreen)]()
[![Protocol](https://img.shields.io/badge/protocol-reverse%20engineered-blue)]()
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

A Python library for interfacing with Wanggan handheld GPS locators. Download GPS track data, parse coordinates, and export to standard formats (GPX, KML, CSV).

**Tested on:** Wanggan D6E GNSS Handheld Navigator
**⚠️ Note:** Protocol likely compatible with other Wanggan GPS models, but untested

## ⚡ Quick Start

### Two Ways to Use

**🖱️ Graphical Interface (Recommended for Non-Programmers)**

```bash
# Install with GUI support
pip install -e "[gui]"

# Launch the GUI
python wanggan_gps_gui.py
```

See [GUI User Guide](docs/GUI_USER_GUIDE.md) for detailed instructions.

### Installation

#### Option 1: Install from Source (Recommended)

```bash
# Clone the repository
git clone https://github.com/heliobteixeira/wanggan-gps-python.git
cd wanggan-gps-python

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the library with dependencies
pip install -e .

# Or install with GUI support
pip install -e "[gui]"
```

---

## GUI Instructions

### For Windows Users

Double-click the GUI script to start:

```bash
python wanggan_gps_gui.py
```

### For macOS and Linux Users

Run the following command:

```bash
python wanggan_gps_gui.py
```
