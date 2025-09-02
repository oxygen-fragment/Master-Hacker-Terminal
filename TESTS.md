# Terminal Art Testing Plan

## Environment Detection Tests

### 1. Locale Environment Variables
Test UTF-8 environment detection across different setups:

```python
# Test cases for environment detection
test_environments = [
    # UTF-8 environments (should return True)
    {"LC_ALL": "en_US.UTF-8", "expected": True},
    {"LANG": "en_US.utf8", "expected": True}, 
    {"LC_CTYPE": "C.UTF-8", "expected": True},
    
    # Non-UTF-8 environments (should return False)
    {"LC_ALL": "en_US.ISO-8859-1", "expected": False},
    {"LANG": "C", "expected": False},
    {"LC_ALL": "", "LC_CTYPE": "", "LANG": "", "expected": False},
]
```

**Manual test procedure:**
```bash
# Test 1: UTF-8 environment
export LANG=en_US.UTF-8
python3 masterhacker.py --unicode auto

# Test 2: Legacy environment  
export LANG=C
python3 masterhacker.py --unicode auto

# Test 3: Override with explicit flag
python3 masterhacker.py --unicode on
python3 masterhacker.py --unicode off
```

### 2. Terminal Capability Detection
Test TERM variable heuristics:

```python
# Test cases for TERM detection
term_test_cases = [
    # Modern terminals (likely Unicode-capable)
    ("xterm-256color", True),
    ("screen-256color", True),
    ("tmux-256color", True),
    
    # Legacy/basic terminals (questionable Unicode)
    ("xterm", False),
    ("vt100", False),
    ("dumb", False),
    ("", False),  # No TERM set
]
```

### 3. Platform-Specific Tests

**Linux/macOS terminals:**
- gnome-terminal
- xterm
- Terminal.app (macOS)
- iTerm2 (macOS)
- tmux/screen sessions

**Windows terminals:**
- Windows Terminal
- cmd.exe (legacy)
- PowerShell (legacy) 
- PowerShell Core
- WSL bash

## Width Probe Tests

### Minimal Probe Implementation
```python
#!/usr/bin/env python3
"""Minimal Unicode width probe test"""

import sys
import os
import select
import termios
import tty

def simple_width_probe():
    """
    Test Unicode character width without external dependencies
    Returns True if Unicode appears to render with expected width
    """
    if not sys.stdout.isatty():
        return False
        
    try:
        # Save terminal state
        old_attrs = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        
        # Move to known position and test Unicode
        sys.stdout.write('\033[s')  # Save cursor position
        sys.stdout.write('┌─┐')     # 3 Unicode box chars
        sys.stdout.write('\033[6n') # Query cursor position
        sys.stdout.flush()
        
        # Read response with timeout
        if select.select([sys.stdin], [], [], 0.1)[0]:
            response = sys.stdin.read(10)
            # Parse ESC[row;colR format
            # Expected: cursor moved exactly 3 positions
            # Implementation simplified for this test
        
        sys.stdout.write('\033[u')  # Restore cursor
        sys.stdout.write('\033[K')  # Clear line
        return True  # Simplified - assume success
        
    except Exception:
        return False
    finally:
        # Restore terminal
        try:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attrs)
        except:
            pass

if __name__ == "__main__":
    result = simple_width_probe()
    print(f"Unicode width probe: {'PASS' if result else 'FAIL'}")
```

## Art Rendering Tests

### ASCII vs Unicode Comparison
Test both character sets across terminals:

```bash
# Generate test output for visual comparison
python3 -c "
# ASCII version
print('ASCII Frame:')
print('+' + '-'*20 + '+')
print('|' + ' '*20 + '|')
print('+' + '-'*20 + '+')

# Unicode version  
print('\nUnicode Frame:')
print('┌' + '─'*20 + '┐')
print('│' + ' '*20 + '│')
print('└' + '─'*20 + '┘')

# Progress bars
print('\nASCII Progress: [########..........] 40%')
print('Unicode Progress: [████▋░░░░░░░░░] 40%')
"
```

### Layout Integrity Tests
Verify consistent width across different scenarios:

```python
def test_banner_width():
    """Test that banners maintain consistent width"""
    ascii_lines = ASCII_BANNER.strip().split('\n')
    unicode_lines = UNICODE_BANNER.strip().split('\n')  # If implemented
    
    # Check ASCII banner width consistency
    ascii_widths = [len(line) for line in ascii_lines]
    assert all(w <= 60 for w in ascii_widths), "ASCII banner exceeds 60 columns"
    
    # Check Unicode banner width (if enabled)
    # Note: This would require actual width calculation, not len()
```

## Manual Testing Matrix

### Terminal Compatibility Grid

| Terminal | OS | ASCII | Unicode | Notes |
|----------|-------|--------|---------|-------|
| gnome-terminal | Linux | ✓ | ✓ | Excellent support |
| xterm | Linux | ✓ | ? | Font-dependent |
| Terminal.app | macOS | ✓ | ✓ | Good default fonts |
| iTerm2 | macOS | ✓ | ✓ | Excellent support |
| Windows Terminal | Windows | ✓ | ✓ | Modern, full support |
| cmd.exe | Windows | ✓ | ✗ | Legacy, poor Unicode |
| PowerShell 5.1 | Windows | ✓ | ? | Font size dependent |
| PowerShell 7+ | Windows | ✓ | ✓ | Better Unicode support |
| WSL bash | Windows | ✓ | ✓ | Inherits terminal capabilities |

### Test Procedure for Each Terminal

1. **Basic functionality test:**
   ```bash
   python3 masterhacker.py --unicode off
   python3 masterhacker.py --unicode on
   python3 masterhacker.py --unicode auto
   ```

2. **Visual inspection checklist:**
   - [ ] Banners render without broken characters
   - [ ] Box frames have connected corners
   - [ ] Progress bars align properly
   - [ ] Text fits within expected width
   - [ ] No character encoding errors

3. **Edge case testing:**
   ```bash
   # Test with minimal terminal size
   stty cols 60 rows 24
   python3 masterhacker.py
   
   # Test with large terminal
   stty cols 120 rows 40  
   python3 masterhacker.py
   
   # Test without color support
   TERM=dumb python3 masterhacker.py
   ```

## Regression Tests

### Backward Compatibility
Ensure ASCII mode works identically to current implementation:

```python
def test_ascii_backward_compatibility():
    """Ensure ASCII mode matches existing output exactly"""
    # Current ASCII_BANNER should remain unchanged
    # Progress bars should use same characters (#, .)
    # All existing functionality preserved
```

### Performance Tests
```python
import time

def test_unicode_detection_speed():
    """Unicode detection should complete in <50ms"""
    start = time.time()
    # Run detection logic
    elapsed = time.time() - start
    assert elapsed < 0.05, "Unicode detection too slow"
```

## Automation Script

Simple test runner for continuous validation:

```bash
#!/bin/bash
# test_terminals.sh - Automated terminal art testing

echo "Testing Master Hacker Terminal art rendering..."

# Test each mode
for mode in off on auto; do
    echo "Testing --unicode $mode"
    python3 masterhacker.py --unicode $mode --script demo > test_output_$mode.txt
    
    # Basic checks
    if grep -q "Command not recognized" test_output_$mode.txt; then
        echo "ERROR: Broken functionality in $mode mode"
        exit 1
    fi
done

echo "Basic functionality tests passed"

# Width check - ensure no lines exceed 80 characters  
max_width=$(python3 masterhacker.py --unicode on | wc -L)
if [ $max_width -gt 80 ]; then
    echo "WARNING: Output width $max_width exceeds 80 columns"
fi

echo "Terminal art tests complete"
```

## Expected Results

- **ASCII mode**: Should work identically on all tested terminals
- **Unicode mode**: Should gracefully degrade to ASCII on unsupported terminals
- **Auto mode**: Should select appropriate mode based on environment detection
- **Width constraint**: All output should fit comfortably in 80-column terminals
- **Performance**: Mode detection should be imperceptible to users (<50ms)