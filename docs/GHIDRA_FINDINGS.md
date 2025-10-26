# Ghidra Firmware Analysis - Key Findings

## Function: FUN_000128dc (Route Manager)

**Address:** 0x000128dc  
**Purpose:** Main route/track display and management function  
**Status:** ✅ FULLY ANALYZED

---

## Critical Data Structures

### Route Record Format (32 bytes each)
```
Offset | Size | Description
-------|------|------------
0x00   | 2    | Route ID/Number (big endian if < 0x30, else +0x700)
0x02   | 1    | Unknown byte
0x03   | 1    | Unknown byte  
0x04   | 1    | Unknown byte
0x05   | 1    | Unknown byte
0x06   | 4    | Distance (meters, big endian)
0x0A   | 4    | Area (square meters, big endian)
0x0E   | 2    | Unknown
0x10+  | ?    | Additional data
```

### Storage Layout
- **Data buffer:** `_DAT_00012ce8` (base address for route data)
- **Records per page:** 7 routes (when > 7 total)
- **Flash storage:** 0x1000 (4KB) pages
- **Max routes:** ~512 (based on 0x200 checks in code)

---

## State Machine (9 modes)

| State | Name | Description |
|-------|------|-------------|
| 0x01 | Route List | Display 7 routes per page |
| 0x02 | Route Details | Show selected route info (area, distance, map) |
| 0x03 | Navigation | Start navigation to route |
| 0x04 | Delete Confirm | "Determine delete" prompt |
| 0x05 | Delete Execute | Perform deletion, compact data |
| 0x06 | Browse Mode | Scroll through routes |
| 0x08 | Signal Error | "Poor signal, unable to navigate" |

---

## UI Strings Found

### Display Labels
- `"Route"` @ multiple locations
- `"Record"` @ 0x00012d0f
- `"No data record"` @ 0x00012ceb

### User Prompts  
- `"Press[_]to_navigation"` @ 0x0001320c
- `"Press[_]to_delete"` @ 0x00013228
- `"Start"` @ 0x00013240
- `"Delete"` @ 0x00013248

### Confirmations
- `"Determine delete"` @ 0x00013253
- `"Successfully delete"` @ 0x00013273

### Errors
- `"Poor signal"` @ 0x0001328b
- `"Unable to navigate"` @ 0x00013298

---

## Area Unit Modes

The device supports 5 different area measurement units:

```c
Mode 0: Custom calculation (÷ stored multiplier)
Mode 1: Chinese Mu (亩) - "Area: %.2fmu"
Mode 2: Large Mu - "Area: %.2flarge mu"  
Mode 3: Acres - "Area: %.2facre"
Mode 4: Hectares - "Area: %.2fhectare"
```

Format strings stored at:
- Mode 1: 0x00013194
- Mode 2: 0x000131a4
- Mode 3: 0x000131b8
- Mode 4: 0x000131c8

---

## Distance Display Logic

```c
if (distance_meters < 10000) {
    display_format = "Distance: %.1fm";
} else {
    display_format = "Distance: %.3fkm";
}
```

- Meters format: `"$@Distance: %.1fm"` @ 0x000131f6
- Kilometers format: `"@Distance: %.3fkm"` @ 0x000131df

---

## Key Functions Called

### Display Functions
- `FUN_0003451c()` - Draw text string
- `FUN_000342a4()` - Draw number
- `FUN_00029434()` - Draw data field
- `FUN_00033ef0()` - Draw UI element
- `FUN_000336a0()` - Draw filled rectangle

### Data Access
- `FUN_0003ca68()` - **READ FROM FLASH** (critical!)
- `FUN_0003cbe0()` - Erase flash page
- `FUN_0003cc1c()` - **WRITE TO FLASH** (critical!)

### Navigation
- `FUN_0002d34c()` - Start navigation to route
- `FUN_000073e0()` - Save/update data

---

## 🎯 NEXT TARGETS FOR ANALYSIS

### Priority 1: Data Export Functions
These flash I/O functions likely handle USB/serial export:
- ✅ `FUN_0003ca68()` - Flash READ - **ANALYZE THIS**
- ✅ `FUN_0003cc1c()` - Flash WRITE - **ANALYZE THIS**

### Priority 2: Search for Export Strings
Look for these in Ghidra string search:
- "DOWNLOAD"
- "EXPORT" 
- "SEND"
- "TRANSFER"
- "PC"
- "USB"
- "UART"
- "SERIAL"
- "DATA"
- "TRACK"

### Priority 3: Find Data Format Functions
The route data must be converted to export format:
- Look for NMEA sentence builders
- Find CSV/text formatters
- Locate binary protocol handlers

---

## Analysis Commands Used

### Ghidra Steps Taken
1. ✅ Imported D6E.bin (ARM:LE:32:Cortex, base 0x08000000)
2. ✅ Auto-analysis completed
3. ✅ Found $PCAS strings (0x7668, 0x7690, 0x76a4)
4. ✅ Traced references to FUN_000128dc
5. ✅ Decompiled and analyzed function

### Next Ghidra Actions
1. Right-click `FUN_0003ca68` → "Show References to" → find callers
2. Search strings for "EXPORT", "DOWNLOAD", "USB"
3. Look at functions around 0x0003ca68 (I/O cluster)
4. Find UART/USB initialization code

---

## 🚨 CRITICAL OBSERVATION

**This function handles ON-SCREEN display only!**

The USB/serial export protocol is likely in a **completely different function** that:
1. Reads route data from flash (using `FUN_0003ca68`)
2. Formats it for transmission (NMEA? Binary? CSV?)
3. Sends via UART/USB

**We need to find the EXPORT/DOWNLOAD command handler next!**
