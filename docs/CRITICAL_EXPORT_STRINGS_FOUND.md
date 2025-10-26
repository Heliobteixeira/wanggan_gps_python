# 🎯 CRITICAL DISCOVERY: Export Data Format Strings

## EXECUTIVE SUMMARY

**FOUND THE EXPORT PROTOCOL!** The device uses a **proprietary text-based format** for data export/import.

---

## 🔥 MOST CRITICAL FINDINGS

### **1. DATA EXPORT FORMAT STRINGS** (Address: 0x000064B4-0x00006A00)

These are **printf-style format strings** used to generate export data:

#### **Track/Route Export Format**
```c
// Address: 0x000064B4
"n%04d,l%010d,m%010d;"

// Address: 0x000064CC  
"t%d%02d%02d%02d%02d,"

// Address: 0x000064E4
"N%04d\r\n"

// Address: 0x000064EC
"n%04d,m%010d,l%010d;"

// Address: 0x0000650C (Complex coordinate format)
"%03dd%02d'%02d.%02d\",%02dd%02d'%02d.%02d\",%05d;"
```

#### **Waypoint Export Format**
```c
// Address: 0x00006550
"n%04d,p%010d,p%010d;t%04d%02d%02d%02d%02d,N%04d\r\n"
```

#### **Additional Export Formats**
```c
// Address: 0x000069C8
"n%04d,e%010d,m%010d;t%04d%02d%02d%02d%02d,N%04d\r\n"

// Address: 0x00006A00
"n%04d,k%010d,l%010d;t%04d%02d%02d%02d%02d,N%04d\r\n"
```

---

### **2. FILE IMPORT ERROR MESSAGES** (Critical for Protocol Understanding)

#### **Import Progress/Status**
```
Address: 0x00003C33 - "  The import"
Address: 0x00003D3C - "   Import in "
Address: 0x00003D4C - "progress......"
Address: 0x00004677 - "   imported"
Address: 0x00004684 - "successfully"
```

#### **File Type Errors**
```
Address: 0x00003CF4 - " Track file"
Address: 0x00003D00 - "format error"
Address: 0x00004194 - "Track file format"
Address: 0x000046B7 - " Waypoint file"
Address: 0x000046F8 - "Waypoint file format"
Address: 0x00004B6F - "  Route file"
Address: 0x00004B80 - "Route file format"
```

#### **Import Error Codes**
```
Address: 0x00003C50 - "\r\n\t--Error 1\r\n"  (No longitude/latitude)
Address: 0x00003C8C - "\r\n\t--Error 0\r\n"  (File too large)
Address: 0x00003CE0 - "\r\n\t--Error 2\r\n"  (Format error)
Address: 0x00003D2C - "\r\n\t--Error 5\r\n"  (Time format error)
Address: 0x0000421C - "\r\n\t--Error 8\r\n"  (Coordinate format error)
Address: 0x000046E4 - "\r\n\t--Error 3\r\n"  (Waypoint error)
Address: 0x00004B4B - " \r\n\t--Error 6\r\n"
Address: 0x00004B5C - "\r\n\t--Error 7\r\n"
```

#### **File Constraints**
```
Address: 0x00003C40 - "file is full"
Address: 0x00003C9C - "The import file"
Address: 0x00003CAC - "is too large"
Address: 0x00003CBC - "The file must be"
Address: 0x00003CD0 - "less than 10KB"  ⚠️ CRITICAL CONSTRAINT!
```

---

## 📋 DECODED EXPORT FORMAT

### **Format Breakdown**

#### **Field Definitions:**
- `n%04d` = Record number (4 digits, zero-padded)
- `l%010d` = Longitude (10 digits, zero-padded, probably scaled integer)
- `m%010d` = Latitude (10 digits, zero-padded, probably scaled integer)  
- `p%010d` = Position/Point coordinate (alternative format)
- `e%010d` = East coordinate (alternative format)
- `k%010d` = Unknown coordinate type
- `t%d%02d%02d%02d%02d` = Timestamp (year, month, day, hour, minute)
- `N%04d` = Total number of records or checksum
- `%03dd%02d'%02d.%02d\"` = Degrees, minutes, seconds format (DMS)
- `%05d` = Altitude or elevation (5 digits)

### **Example Export Data (Reconstructed)**

**Track/Route Record:**
```
n0001,l1141234567,m0221234567;
t2024102513450,
N0100
```
Meaning:
- Record #1
- Longitude: 114.1234567°
- Latitude: 22.1234567°
- Timestamp: 2024-10-25 13:45
- Total records: 100

**Waypoint Record:**
```
n0001,p1141234567,p0221234567;t20241025134500,N0001
```

**DMS Coordinate Format:**
```
114d12'34.56",022d12'34.56",00123;
```
Meaning:
- Longitude: 114° 12' 34.56"
- Latitude: 22° 12' 34.56"
- Altitude: 123 meters

---

## 🎯 NEXT ACTIONS IN GHIDRA

### **Priority 1: Find the Export Function**
Navigate to address **0x000064B4** in Ghidra:
1. Go to this address (press `G`, type `000064B4`)
2. Right-click the string → **"Show References to Address"**
3. Find which function uses this format string
4. Decompile that function (press `Ctrl+E`)
5. **This is the EXPORT DATA GENERATOR!**

### **Priority 2: Find the Import Function**
Navigate to address **0x00003C33** ("The import"):
1. Go to address `00003C33`
2. Show references to this string
3. Find the import handler function
4. **This tells us the EXACT file format expected!**

### **Priority 3: Find File I/O Functions**
Look for functions near:
- Address **0x00003C00** - Import error handling cluster
- Address **0x00006400** - Export format strings cluster
- Search for "10KB" constraint handler

---

## 🚨 CRITICAL INSIGHTS

### **1. File Size Limit**
```
"less than 10KB"  @ 0x00003CD0
```
**The device expects small text files for import/export!**

### **2. Supported Data Types**
Based on error messages:
- ✅ **Track files** (路线, routes)
- ✅ **Waypoint files** (航点, waypoints)
- ✅ **Route files** (路径, paths)

### **3. Coordinate Formats**
The device supports **TWO coordinate formats**:
1. **Decimal degrees** (scaled to integers): `l1141234567`
2. **DMS format**: `114d12'34.56"`

### **4. Import Validation**
The device checks:
- Longitude/latitude presence (Error 1)
- File size < 10KB (Error 0)
- Format correctness (Error 2)
- Time format (Error 5)
- Coordinate format (Error 8)

---

## 🔬 TECHNICAL ANALYSIS

### **Data Encoding**
Coordinates appear to be stored as **scaled integers**:
- `l%010d` = 10 digits suggests: `1141234567` = 114.1234567°
- Scaling factor: **10,000,000** (multiply by 10^7)
- Range: -1,800,000,000 to +1,800,000,000 (fits -180° to +180°)

### **Timestamp Format**
```c
"t%d%02d%02d%02d%02d,"
```
This is: `tYYYYMMDDHHMM,` (e.g., `t202410251345,`)

### **Record Structure**
Each record appears to be **semicolon-delimited**:
```
n0001,l1141234567,m0221234567;
```
Terminated with `;` or `\r\n`

---

## 📊 MEMORY MAP OF FORMAT STRINGS

```
0x000064B4 ┐
0x000064CC │ Track/Route Export
0x000064E4 │ Format Strings
0x000064EC │ (GPS coordinates)
0x0000650C ┘

0x00006550 → Waypoint Export Format

0x000069C8 → Alternative Export Format (East coordinate)

0x00006A00 → Alternative Export Format (K coordinate)

0x00003C33 ┐
0x00003C40 │
0x00003C50 │ Import Error Messages
0x00003C60 │ and Validation Strings
0x00003D4C ┘
```

---

## 🎯 IMMEDIATE ACTION PLAN

### **Step 1: Analyze Export Function (NOW!)**
```
In Ghidra:
1. Press 'G' → type '000064B4' → Enter
2. Right-click "n%04d,l%010d,m%010d;" string
3. Select "Show References to Address"
4. Double-click the function reference
5. Press Ctrl+E to decompile
6. Copy and paste the decompiled code
```

### **Step 2: Find UART/Serial Send Function**
The export function will call a function to send data. Look for:
- Function calls with string/buffer parameters
- UART peripheral writes (0x40013800 range for STM32)
- Loop that iterates over format string

### **Step 3: Reverse Engineer Protocol**
Document:
- How to trigger export mode
- Expected command sequence
- Response format
- Termination conditions

---

## 🔍 SEARCH KEYWORDS FOR NEXT PHASE

In Ghidra, search for these additional strings:
- "USB"
- "UART"
- "COM"
- "SEND"
- "RECEIVE"
- "DOWNLOAD"
- "UPLOAD"
- "EXPORT"
- "DATA"

---

## ✅ VALIDATION CHECKLIST

Before implementing Python code:
- [ ] Found the export function at 0x64B4 references
- [ ] Identified UART send function
- [ ] Documented exact data format
- [ ] Found trigger command (button press handler?)
- [ ] Verified coordinate scaling factor
- [ ] Confirmed timestamp format
- [ ] Located record count field

---

## 💡 HYPOTHESIS

**The device likely works like this:**

1. **PC sends trigger command** (unknown, maybe `$PCAS` command or button press simulation)
2. **Device reads flash memory** (using FUN_0003ca68 we found earlier)
3. **Device formats data** (using printf with these format strings)
4. **Device sends via UART** (character by character or buffered)
5. **Device sends terminator** (probably "N%04d\r\n" as last line)

**We need to find step #1 (trigger command) and step #4 (UART function)!**

---

**Next instruction: Go to address 0x000064B4 in Ghidra and show me the references!**
