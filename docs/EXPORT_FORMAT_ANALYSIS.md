"""
Wanggan D6E GPS - Export Format Analysis
========================================

Based on firmware reverse engineering and testing, the device supports three export triggers:

## 1. TILDE (0x7E) - '~' - Full Data Export with Headers
---------------------------------------------------------
**Purpose**: Export complete data records with type-specific headers and DMS coordinates
**Function**: FUN_000060e0() - Full export function
**Data Types**: Track (k,l), Area (m,l), Distance (l,m), Waypoint (p,p)

**Format Structure**:
```
n####,X##########,Y##########;t############,N####
LON_DMS,LAT_DMS,ALT;
LON_DMS,LAT_DMS,ALT;
...
!
n####,X##########,Y##########;t############,N####
LON_DMS,LAT_DMS,ALT;
...
!
```

**Header Formats by Data Type**:

### Area (m,l format):
```
n0014,m0000019335,l0000006404;t202510241534,N0004
│      └─ Latitude  └─ Longitude
```
- Used for polygon/area measurements
- m = latitude (scaled int ÷ 10,000,000)
- l = longitude (scaled int ÷ 10,000,000)

### Distance (l,m format):
```
n0138,l0000001446,m0000000000;t202510241603,N0004
│      └─ Longitude  └─ Latitude
```
- Used for linear distance measurements
- l = longitude (scaled int ÷ 10,000,000)
- m = latitude (scaled int ÷ 10,000,000)
- Note: Order swapped compared to Area

### Waypoint (p,p format):
```
n0001,p0000000000,p0000000000;t202510250039,N0004
│      └─ p-field   └─ p-field
```
- Used for single point markers
- p fields purpose TBD (often zero)
- Usually contains single coordinate

### Track (k,l format):
```
n0831,k0000019806,l0000012137;t202510241548,N0004
│      └─ k-field   └─ Longitude
```
- Used for GPS tracks/routes
- k field purpose TBD (track parameter?)
- l = longitude (scaled int ÷ 10,000,000)

**Common Header Fields**:
- `n####` - Record number (e.g., n0014, n0138, n0001, n0831)
- `t############` - Timestamp YYYYMMDDHHMM (e.g., t202510241534)
- `N####` - Total record count/index

**Coordinate Format** (DMS - Degrees, Minutes, Seconds):
```
-008d35'22.330",+41d06'50.109",01796;
│   │  │       │   │  │       │
│   │  │       │   │  │       └─ Altitude in meters (5 digits)
│   │  │       │   │  └───────── Seconds with decimals
│   │  │       │   └──────────── Minutes (2 digits)
│   │  │       └──────────────── Degrees (2-3 digits, with sign)
│   │  └──────────────────────── Seconds with decimals
│   └─────────────────────────── Minutes (2 digits)
└─────────────────────────────── Degrees (3 digits, with sign)
```

**Example Output with Multiple Data Types**:
```
n0014,m0000019335,l0000006404;t202510241534,N0004
-008d35'22.330",+41d06'50.109",01796;
-008d35'23.035",+41d06'53.830",01737;
!
n0138,l0000001446,m0000000000;t202510241603,N0004
-008d35'22.586",+41d06'51.525",01816;
-008d35'22.591",+41d06'51.508",01815;
!
n0001,p0000000000,p0000000000;t202510250039,N0004
-008d33'52.395",+41d11'19.367",01588;
!
n0831,k0000019806,l0000012137;t202510241548,N0004
-008d35'27.326",+41d06'54.784",01679;
-008d35'22.323",+41d06'50.112",01796;
!
```

**Use Case**: 
- Complete track download with metadata
- Includes track headers for organization
- Best for exporting all data with context


## 2. EXCLAMATION (0x21) - '!' - Raw Track Data (No Headers)
------------------------------------------------------------
**Purpose**: Export all track points without headers (metadata summary mode)
**Function**: FUN_0000368c(param_1=0) - Export with param_1=0

**Format Structure**:
```
LON_DMS,LAT_DMS,ALT;
LON_DMS,LAT_DMS,ALT;
LON_DMS,LAT_DMS,ALT;
...
!
```

**Characteristics**:
- NO track headers (n####,m####,l####;t####,N#### lines)
- ONLY coordinate data in DMS format
- Coordinates from ALL tracks concatenated
- Same DMS coordinate format as tilde export
- Larger output (26,575 bytes vs 3,260 bytes for tilde)
- 618 coordinates vs 81 coordinates in tilde

**Example Output**:
```
-008d35'25.36680",+41d06'55.14420",01702;
-008d35'25.37100",+41d06'55.17720",01700;
-008d35'25.37820",+41d06'55.21260",01699;
-008d35'25.38120",+41d06'55.25280",01698;
!
```

**Use Case**:
- Raw coordinate data extraction
- When you don't need track organization/metadata
- Simpler parsing (no header parsing needed)
- Bulk coordinate export


## 3. CARET (0x5E) - '^' - Detailed Track Metadata
-------------------------------------------------
**Purpose**: Export track metadata with detailed internal data
**Function**: FUN_0000368c(param_1=1) - Export with param_1=1

**Format Structure**:
```
[Binary/hex data with track indices and metadata]
END
```

**Characteristics**:
- Very small output (15 bytes)
- Contains binary/non-ASCII data
- Format string in firmware: `s_%d:_000037cc` (track index format)
- Format string: `s_---%d:_000037d8` (detailed data index)
- Includes flash memory reads from 0x300000 + track_offset
- May include 10-byte data blocks per coordinate
- Ends with "END" marker

**Example Output** (hex view):
```
�ļ���=0�ļ�END
```

**Use Case**:
- Internal debugging/diagnostics
- Binary track metadata
- Flash memory dump
- Advanced analysis of internal storage format


## Summary Comparison
--------------------

| Trigger | Name        | Headers | Coords | Size    | Format      | Use Case                    |
|---------|-------------|---------|--------|---------|-------------|-----------------------------|
| 0x7E ~  | Tilde       | YES     | 81     | 3.2 KB  | DMS + Meta  | Complete organized export   |
| 0x21 !  | Exclamation | NO      | 618    | 26.5 KB | DMS only    | Raw bulk coordinate dump    |
| 0x5E ^  | Caret       | NO      | 0      | 15 B    | Binary      | Debug/internal metadata     |


## Firmware Analysis Notes
--------------------------

From decompiled C code:

**Tilde Function (0x7E)**:
- Reads from flash memory addresses 0xD000 + offsets
- Formats header: `"n%04d,m%010d,l%010d;t%04d%02d%02d%02d%02d,N%04d"`
- Outputs DMS coordinates for each track point
- Iterates through all stored tracks

**Exclamation/Caret Function (0x21/0x5E)**:
```c
void FUN_0000368c(int param_1) {
    // param_1 = 0 for exclamation (!)
    // param_1 = 1 for caret (^)
    
    // Read track count from offset 0x3c
    // Iterate through tracks (0x24 bytes per track metadata)
    
    if (param_1 == 1) {
        // Caret mode: read detailed flash data
        // Read from 0x300000 + track_offset
        // Output track indices and hex data
    }
    
    // Output coordinate data
}
```


## Implementation Notes
-----------------------

**Current Parser Support**:
- ✓ Tilde (0x7E): Fully supported in `parse_gps_export.py`
- ✗ Exclamation (0x21): Not yet supported (no header parsing)
- ✗ Caret (0x5E): Not yet supported (binary format)

**Next Steps**:
1. Update parser to handle headerless exclamation format
2. Investigate caret binary format structure
3. Add format auto-detection to parser
4. Document track metadata structure from headers
