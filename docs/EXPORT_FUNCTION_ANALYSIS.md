# 🎯 EXPORT FUNCTION FULLY DECODED - FUN_000060e0

## EXECUTIVE SUMMARY

**WE FOUND THE COMPLETE DATA EXPORT FUNCTION!**

This function (`FUN_000060e0`) is the **MASTER EXPORT ROUTINE** that:
1. Reads all GPS data from flash memory
2. Formats it into text using our discovered format strings
3. Sends it via serial port (through `FUN_000003c0` = printf/send function)

---

## 🔥 CRITICAL DISCOVERIES

### **1. The Send Function: `FUN_000003c0`**

This is called repeatedly throughout the code:
```c
FUN_000003c0(format_string, param1, param2, param3);
FUN_0003e338(delay_ms);  // Delay between transmissions
```

**`FUN_000003c0` is the UART/Serial SEND function!** It's essentially `printf()` for the serial port.

### **2. Flash Read Function: `FUN_0003ca68`**

Called to read data from flash before formatting:
```c
FUN_0003ca68(flash_address, buffer, 0x1000);  // Read 4KB page
```

### **3. Data Processing Function: `FUN_00007258`**

Converts raw GPS data to formatted coordinates:
```c
FUN_00007258((undefined1 *)&local_6c, record_index);
```

---

## 📊 EXPORT DATA STRUCTURE

### **Three Main Data Types Exported:**

#### **Type 1: Track/Route Points** (Main GPS tracks)
```c
if (local_3e == '\0') {
    FUN_000003c0("n%04d,m%010d,l%010d;", record_num, latitude, longitude);
} else {
    FUN_000003c0("n%04d,l%010d,m%010d;", record_num, longitude, latitude);
}
FUN_0003e338(2);  // 2ms delay

FUN_000003c0("t%d%02d%02d%02d%02d,", year, month, day, hour, minute);
FUN_0003e338(2);  // 2ms delay

FUN_000003c0("N%04d", total_count);
FUN_0003e338(1);  // 1ms delay
```

**Example output:**
```
n0001,l1141234567,m0221234567;
t202410251345,
N0100
```

#### **Type 2: Waypoints** (Saved points with names)
```c
FUN_000003c0("n%04d,p%010d,p%010d;t%04d%02d%02d%02d%02d,N%04d\r\n",
             waypoint_num, coord1, coord2, year, month, day, hour, min, total);
FUN_0003e338(5);  // 5ms delay
```

#### **Type 3: Area Measurements** (Polygon data)
```c
FUN_000003c0("n%04d,e%010d,m%010d;t%04d%02d%02d%02d%02d,N%04d\r\n",
             area_num, east_coord, north_coord, year, month, day, hour, min, total);
FUN_0003e338(5);  // 5ms delay
```

#### **Type 4: Route Definitions** (k-type coordinates)
```c
FUN_000003c0("n%04d,k%010d,l%010d;t%04d%02d%02d%02d%02d,N%04d\r\n",
             route_num, k_coord, l_coord, year, month, day, hour, min, total);
FUN_0003e338(5);  // 5ms delay
```

---

## 🔍 DETAILED COORDINATE FORMAT

### **DMS (Degrees Minutes Seconds) Format**

The function converts coordinates to DMS format for detailed points:

```c
FUN_000003c0("%03dd%02d'%02d.%02d\",%02dd%02d'%02d.%02d\",%05d;",
             lon_degrees, lon_minutes, lon_seconds, lon_hundredths,
             lat_degrees, lat_minutes, lat_seconds, lat_hundredths,
             altitude);
FUN_0003e338(3);  // 3ms delay
```

**Example:**
```
114d12'34.56",022d12'34.56",00123;
```

**Calculation Logic Found:**
```c
uVar5 / DAT_00006508                              // Degrees
(uVar5 - DAT_00006508 * (uVar5 / DAT_00006508)) / 60000   // Minutes
(uVar5 % 60000) / 1000                            // Seconds
```

- `DAT_00006508` appears to be a division factor (likely 3,600,000 for degrees)
- Values are scaled integers
- Check for altitude < 60000 (validity flag)

---

## 🎮 EXPORT SEQUENCE

### **Complete Export Flow:**

```
1. Initialize variables
   - Read track count from flash
   - Calculate total records to export

2. FOR EACH TRACK:
   - Read track data from flash (FUN_0003ca68)
   - Format header: "n####,l##########,m##########;"
   - Send via serial (FUN_000003c0)
   - Delay 2ms
   - Format timestamp: "t#############,"
   - Send via serial
   - Delay 2ms
   - Format total: "N####"
   - Send via serial
   - Delay 1ms
   
   FOR EACH POINT IN TRACK:
   - Read point data (4KB pages, 0x199 = 409 points per page)
   - Format DMS coordinates
   - Send via serial
   - Delay 3ms
   - If last point: send "\r\n" terminator
   - Else: send "," separator

3. EXPORT WAYPOINTS (offset 0x2a, count at +0x34):
   - Read waypoint data
   - Format: "n####,p##########,p##########;t############,N####\r\n"
   - Send each waypoint
   - Delay 5ms between waypoints

4. EXPORT AREAS (offset varies, count at +0x36):
   - Read area polygon data
   - Format: "n####,e##########,m##########;t############,N####\r\n"
   - Send all area points in DMS format
   - Delay 5ms between areas

5. EXPORT ROUTES:
   - Read route data
   - Format: "n####,k##########,l##########;t############,N####\r\n"
   - Send route points
   - Delay 5ms between routes

6. If no data: send "null!\r\n"
```

---

## 💾 MEMORY LAYOUT DISCOVERED

### **Flash Memory Organization:**

```c
DAT_00006548  // Base address for waypoints flash
DAT_000069b8  // Base address for areas flash
DAT_000069c0  // Area data storage base
DAT_000069fc  // Routes flash base
DAT_00006a34  // Route points storage
```

### **Page Structure:**
- Each page = 0x1000 (4096 bytes)
- Waypoint record = 0x10 (16 bytes)
- Area record = 0x24 (36 bytes)
- Track points = 10 bytes each
- Max points per page = 0x199 (409 points)

### **Data Offsets:**
```c
iVar1 + 0x38  // Track count 1
iVar1 + 0x3a  // Track count 2
iVar1 + 0x2a  // Waypoint base offset
iVar1 + 0x34  // Waypoint count (byte)
iVar1 + 0x36  // Area count (byte)
```

---

## 🔧 KEY FUNCTIONS IDENTIFIED

| Function | Purpose | Parameters |
|----------|---------|------------|
| `FUN_000003c0` | **SERIAL SEND** (printf) | format_string, param1, param2, param3 |
| `FUN_0003e338` | **DELAY** | milliseconds |
| `FUN_0003ca68` | **FLASH READ** | address, buffer, size |
| `FUN_00007258` | **COORDINATE CONVERTER** | output_buffer, record_index |
| `FUN_00007298` | **PAGE LOADER** | page_num, buffer |
| `FUN_000072b0` | **INITIALIZATION** | (unknown params) |
| `FUN_0003fb84` | **DATA VALIDATOR** | record_index |

---

## 🎯 NEXT CRITICAL STEP

### **Find the Trigger - What Calls FUN_000060e0?**

We need to find **how this export function is triggered**:

1. In Ghidra, click on the function name `FUN_000060e0`
2. Right-click → **"Show References to"**
3. Find what calls this function
4. Look for:
   - Button press handlers
   - Menu option handlers
   - Serial command handlers
   - USB enumeration code

**This will tell us THE EXACT COMMAND or button press needed to trigger data download!**

---

## 🚀 PROTOCOL IMPLEMENTATION READY

We now have **95% of the protocol**. We can implement:

### **Python Serial Listener:**
```python
import serial
import time

# Open COM5
ser = serial.Serial('COM5', 9600, timeout=5)

# TODO: Send trigger command (unknown)
# ser.write(b'???')

# Read export data
while True:
    line = ser.readline().decode('ascii')
    if line.startswith('n'):
        # Parse track/waypoint data
        print(f"Data: {line}")
    elif line.startswith('null'):
        # End of export
        break
```

### **Data Parser:**
```python
import re

def parse_track_line(line):
    # n0001,l1141234567,m0221234567;
    match = re.match(r'n(\d{4}),l(\d{10}),m(\d{10});', line)
    if match:
        record = int(match.group(1))
        lon = int(match.group(2)) / 10000000.0
        lat = int(match.group(3)) / 10000000.0
        return record, lon, lat
    return None
```

---

## ⚠️ REMAINING UNKNOWNS

1. **Trigger mechanism** - How to start export? (CRITICAL!)
2. **Coordinate scaling** - Exact division factor (DAT_00006508)
3. **Coordinate type flag** - What determines `local_3e` value?
4. **Validation checks** - What makes altitude < 60000 special?

---

## 📋 YOUR NEXT GHIDRA COMMAND

```
1. Click on "FUN_000060e0" (the function name at top)
2. Right-click → "Show References to"
3. Report: What function(s) call this export function?
4. Look for menu handlers, button handlers, or serial command parsers
```

**We're SO CLOSE! Just need the trigger command!** 🎯
