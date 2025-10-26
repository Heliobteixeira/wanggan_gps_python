# 🎯 EXPORT TRIGGER DISCOVERED!

## CRITICAL FINDING

**Function `FUN_0000fa58` is the MAIN MENU/MODE DISPATCHER**

This is a state machine that handles different modes/screens of the GPS device.

---

## 🔥 THE EXPORT TRIGGER CODE

```c
puVar3 = DAT_0000fc70;
if ((int)((uint)*DAT_0000fc70 << 0x10) < 0) {
    if (*pbVar2 != 3) {
        bVar1 = *_DAT_0000fc74;
        
        if (bVar1 == 0x7e) {           // ← EXPORT TRIGGER!
            FUN_000060e0();             // ← CALLS EXPORT FUNCTION!
        }
        else if (bVar1 == 0x21) {
            FUN_0000368c(0);
        }
        else if (bVar1 == 0x5e) {
            FUN_0000368c(1);
        }
        // ... more handlers
    }
    *puVar3 = 0;
}
```

---

## 💡 WHAT THIS MEANS

### **The Export is Triggered by Byte Value: `0x7E`**

**ASCII 0x7E = `~` (tilde character)**

When the device receives byte `0x7E` on the serial port (or from a button press that sets this value), it calls `FUN_000060e0()` - our export function!

---

## 🎮 OTHER SPECIAL COMMANDS FOUND

```c
0x7E  (~)  → FUN_000060e0()  // DATA EXPORT
0x21  (!)  → FUN_0000368c(0) // Unknown function
0x5E  (^)  → FUN_0000368c(1) // Unknown function
```

---

## 🔍 HOW IT WORKS

### **Input Detection:**

1. `DAT_0000fc70` appears to be a **button/key press flag**
   - When bit 15 is set (negative when shifted left), a key was pressed

2. `_DAT_0000fc74` contains the **key code or character received**
   - Value `0x7E` triggers export

3. The code checks:
   - Key was pressed: `(int)((uint)*DAT_0000fc70 << 0x10) < 0`
   - Not in mode 3: `*pbVar2 != 3`
   - Key code equals 0x7E: `bVar1 == 0x7e`

### **Likely Sources:**
- **Serial port input** (user sends `~` character)
- **Button press** mapped to 0x7E
- **Menu selection** that sets this value

---

## 🚀 PYTHON TEST SCRIPT

Let's try sending the trigger character:

```python
import serial
import time

# Open COM5
ser = serial.Serial('COM5', 9600, timeout=5)
time.sleep(2)  # Wait for device ready

print("Sending export trigger: 0x7E (~)")
ser.write(b'~')  # Send tilde character
ser.flush()

print("\nWaiting for data...")
time.sleep(1)

# Read response
data = []
start_time = time.time()
while time.time() - start_time < 10:  # 10 second timeout
    if ser.in_waiting:
        line = ser.readline().decode('ascii', errors='ignore')
        print(line, end='')
        data.append(line)
        if 'null!' in line:  # End marker
            break
    time.sleep(0.1)

print(f"\nReceived {len(data)} lines")
ser.close()
```

---

## 🔬 ALTERNATIVE TRIGGERS TO TRY

If `0x7E` doesn't work immediately, try these variations:

### **1. With Line Endings**
```python
ser.write(b'~\r\n')
ser.write(b'~\n')
ser.write(b'~\r')
```

### **2. NMEA-Style Command**
```python
ser.write(b'$WGEXP~*XX\r\n')  # Wanggan Export command
```

### **3. Multiple Attempts**
```python
for i in range(5):
    ser.write(b'~')
    time.sleep(0.5)
```

### **4. With Wake-Up Sequence**
```python
# Wake device first
ser.write(b'\r\n\r\n')
time.sleep(0.5)
# Then trigger export
ser.write(b'~')
```

---

## 📋 COMPLETE TEST PROTOCOL

### **Test Sequence:**

1. **Basic trigger:**
   ```
   Send: 0x7E
   Wait: 10 seconds
   Check: Any response?
   ```

2. **With terminator:**
   ```
   Send: 0x7E 0x0D 0x0A
   Wait: 10 seconds
   Check: Data streaming?
   ```

3. **Repeated trigger:**
   ```
   Send: 0x7E (every 500ms, 10 times)
   Wait: 10 seconds
   Check: Response after N attempts?
   ```

4. **Context-dependent:**
   ```
   Maybe need to be in specific mode first?
   Try navigating menus on device while script runs
   ```

---

## 🎯 NEXT DEBUGGING STEPS

### **If No Response:**

1. **Check `FUN_0000368c` functions** (0x21 and 0x5E commands)
   - These might be initialization/handshake
   - Try sending `!` (0x21) or `^` (0x5E) first

2. **Analyze the mode check:** `*pbVar2 != 3`
   - Device might need to be in specific mode
   - Mode 3 appears to block export
   - Try sending mode change command first

3. **Check button mapping:**
   - Physical button on device might map to 0x7E
   - Look at button handler functions in Ghidra
   - Search for references to `_DAT_0000fc74`

4. **Analyze the input parser:**
   - Find `FUN_00000780(_DAT_0000fc74, ...)`
   - This appears to parse commands
   - Might need specific format

---

## 🔍 ADDITIONAL GHIDRA ANALYSIS NEEDED

### **Find Input Handler:**

1. Search for references to `_DAT_0000fc74`
   - This is where key codes are written
   - Find the UART receive interrupt
   - See how bytes from serial port are processed

2. Analyze `FUN_00000780`:
   ```
   pbVar4 = FUN_00000780(_DAT_0000fc74, (byte *)(s_Mode_0000fc77 + 1));
   ```
   - This looks like a command parser
   - Second parameter points to "Mode" string
   - Might expect specific command format

3. Check mode state machine:
   - `*pbVar2` is current mode (0-0x4A)
   - Mode 0x17 = `FUN_000128dc()` (route display we analyzed earlier)
   - Find what mode allows export

---

## 💾 SAVE THIS FOR TESTING

Create file: `test_export_trigger.py`

```python
import serial
import time
import sys

def test_trigger(port='COM5', baudrate=9600):
    """Test export trigger 0x7E"""
    
    print(f"Opening {port} at {baudrate} baud...")
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)
    
    # Test 1: Simple trigger
    print("\n[TEST 1] Sending: 0x7E (~)")
    ser.write(b'~')
    ser.flush()
    time.sleep(0.5)
    
    # Read response
    response = ser.read(ser.in_waiting)
    if response:
        print(f"Response: {response}")
    else:
        print("No response")
    
    # Test 2: With line ending
    print("\n[TEST 2] Sending: 0x7E + CRLF")
    ser.write(b'~\r\n')
    ser.flush()
    time.sleep(0.5)
    
    response = ser.read(ser.in_waiting)
    if response:
        print(f"Response: {response}")
    else:
        print("No response")
    
    # Test 3: Alternative commands
    for cmd in [b'!', b'^', b'~']:
        print(f"\n[TEST 3] Sending: {cmd}")
        ser.write(cmd + b'\r\n')
        ser.flush()
        time.sleep(0.5)
        
        response = ser.read(ser.in_waiting)
        if response:
            print(f"Response: {response}")
    
    # Test 4: Long read for data dump
    print("\n[TEST 4] Sending 0x7E and listening for 10 seconds...")
    ser.write(b'~')
    ser.flush()
    
    start = time.time()
    all_data = b''
    while time.time() - start < 10:
        if ser.in_waiting:
            chunk = ser.read(ser.in_waiting)
            all_data += chunk
            print(chunk.decode('ascii', errors='ignore'), end='')
        time.sleep(0.1)
    
    print(f"\n\nTotal received: {len(all_data)} bytes")
    
    ser.close()
    
if __name__ == '__main__':
    test_trigger()
```

---

## ✅ VALIDATION CHECKLIST

- [ ] Tried sending `0x7E` alone
- [ ] Tried sending `0x7E\r\n`
- [ ] Tried alternative commands `0x21`, `0x5E`
- [ ] Checked if device needs to be in specific mode
- [ ] Analyzed input handler in Ghidra
- [ ] Checked for initialization sequence
- [ ] Tested with device in different menu states

---

## 🎉 SUMMARY

**We found the trigger: `0x7E` (~)**

**Next action:** Run the Python test script and report results!

If it doesn't work immediately, we'll analyze:
1. The input parser (`FUN_00000780`)
2. The mode requirements
3. Any initialization needed

**We're 99% there!** 🚀
