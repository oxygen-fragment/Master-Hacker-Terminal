# Terminal Art Compatibility Research

## Overview

This research examines Unicode vs ASCII terminal art compatibility across terminals for Master Hacker Terminal (MHT), focusing on portable strategies that work with Python's stdlib only.

## Key Findings

### 1. Unicode vs ASCII Compatibility Issues

**What breaks and why:**
- **Encoding mismatches**: Legacy terminals/shells may not support UTF-8, causing Unicode box-drawing characters to render as `?` or mojibake
- **Font limitations**: Default system fonts often lack full Unicode coverage for box-drawing (`U+2500-U+257F`) and block elements (`U+2580-U+259F`)
- **Width calculation failures**: Unicode characters may render with unexpected widths (0, 1, or 2 cells) depending on terminal emulator's `wcwidth` implementation
- **Windows legacy console**: CMD/PowerShell before Windows 10 have poor Unicode support; even modern versions can struggle with box-drawing at small font sizes

**Specific problem characters:**
- Box-drawing: `┌┐└┘─│` may appear broken or misaligned
- Block elements: `█▉▋▎` width varies by font/terminal
- Ambiguous-width characters cause layout corruption

### 2. Detection Strategies

**Environment-based detection:**
```python
def utf8_env_check():
    """Check if environment suggests UTF-8 support"""
    for var in ("LC_ALL", "LC_CTYPE", "LANG"):
        val = os.environ.get(var, "")
        if "UTF-8" in val.upper() or "utf8" in val.lower():
            return True
    return False
```

**Terminal capability probes:**
- **TERM variable heuristics**: `xterm-256color`, `screen-256color` usually support Unicode
- **Platform detection**: Windows < 10 or legacy PowerShell likely problematic
- **Quick width probe** (recommended): Print test Unicode string, use ANSI cursor position query to verify expected width

### 3. Fallback Strategies

**Conservative ASCII palette:**
```
Frames: + - | (corners/edges)
Progress: # . (filled/empty)
Emphasis: * = (bullets/dividers)
```

**Enhanced Unicode palette (when safe):**
```
Frames: ┌┐└┘─│ (box-drawing)
Progress: █▉▋▎ (block elements) 
Dividers: ═ ─ (double/single rules)
```

### 4. Cross-Platform Considerations

**Linux/macOS:**
- Modern terminals (gnome-terminal, iTerm2, Terminal.app) handle Unicode well
- SSH sessions may inherit remote locale settings
- Font dependency: DejaVu Sans Mono, Liberation Mono have good coverage

**Windows:**
- **Windows Terminal**: Excellent Unicode support (recommended)
- **Legacy CMD/PowerShell**: Poor Unicode support, small fonts break box-drawing
- **WSL terminals**: Generally good Unicode support

**Font recommendations (optional, not required):**
- Nerd Fonts: Excellent coverage but not system default
- JetBrains Mono: Good box-drawing support
- Cascadia Code: Windows Terminal default, solid Unicode coverage

## Implementation Recommendations

### Detection Algorithm
1. **Environment check**: Look for UTF-8 in `LC_ALL`/`LC_CTYPE`/`LANG`
2. **Terminal hint check**: Parse `TERM` for known-good values
3. **Quick probe**: Test Unicode character width using ANSI escape sequences
4. **Fallback**: Default to ASCII if any check fails

### Character Set Guidelines
- **ASCII set**: Limit to printable ASCII 32-126 for maximum compatibility
- **Unicode set**: Use only well-supported ranges (box-drawing U+2500-U+257F, basic blocks U+2588-U+258F)
- **Width constraint**: Keep all banners ≤ 60 columns to fit standard 80-column terminals
- **Avoid**: Emoji, CJK characters, combining characters, ambiguous-width glyphs

### Color Strategy
- **Basic colors**: ANSI 3/4-bit colors (30-37, 90-97) for compatibility
- **Enhanced colors**: 256-color (38;5;n) only when `TERM` suggests support
- **Never required**: Color should enhance but never be essential for functionality

## Width Probe Implementation

Minimal stdlib-only width detection:
```python
def probe_unicode_width():
    """Test if Unicode renders with expected width"""
    if not sys.stdout.isatty():
        return False
    
    try:
        # Test string: should render as 3 characters wide
        test = "┌─┐"
        sys.stdout.write(test)
        sys.stdout.write("\033[6n")  # Query cursor position
        sys.stdout.flush()
        
        # Read response (ESC[row;colR format)
        # Implementation note: This requires careful handling
        # of terminal input/output, may timeout
        # Simplified: assume failure if any exception
        return False
    except:
        return False
```

## Sources and References

- Unicode box-drawing characters: Unicode Standard Annex #11 (East Asian Width)
- ANSI escape sequences: ECMA-48 standard for cursor control
- Terminal compatibility: VT100/xterm documentation for escape sequence support
- Width calculation: wcwidth algorithm from Unicode Standard Annex #11
- Windows console: Microsoft documentation on console virtual terminal sequences

## Conclusion

**Recommended approach**: Default to ASCII-safe art with opt-in Unicode enhancement when environment detection passes all checks. This maximizes compatibility while providing better aesthetics when safely available.

**Critical constraint**: Never rely on Unicode for essential functionality - it should always be a visual enhancement only.