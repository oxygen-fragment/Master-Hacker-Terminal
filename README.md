# Master Hacker Terminal

**If you want to help me out you can [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I3I5ZJUA3)**

A tongue-in-cheek, movie-hacker terminal simulator that parodies Hollywood's over-the-top hacking scenes.

**Version 2.1.4** - Now with modern Python architecture, comprehensive type safety, and state-of-the-art terminal rendering.

## Requirements

- Python 3.7+
- No dependencies (uses Python standard library only)

## Quick Start

```bash
# Run deterministic demo
python masterhacker.py --script demo

# Show banner and usage examples
python masterhacker.py

# Interactive mode
python masterhacker.py --interactive

# Force specific terminal width
python masterhacker.py --width 80 --script demo
```

## Adaptive Width System

The terminal automatically adapts to your screen with three rendering modes:

- **Compact** (≤62 chars): Minimal ASCII art for narrow terminals
- **Standard** (63-99 chars): Balanced layout with moderate detail
- **Wide** (≥100 chars): Full cinematic experience with professional letterforms

Width is auto-detected or can be manually set with `--width N`.

## Examples

```bash
# Auto-detect terminal width and Unicode support
python masterhacker.py --script demo

# Force specific width for testing
python masterhacker.py --width 50 --unicode off

# Wide terminal with Unicode
python masterhacker.py --width 120 --unicode on

# Single command execution
python masterhacker.py scan
python masterhacker.py infiltrate MAINFRAME-7
```

## CLI Arguments

| Argument | Description |
|----------|-------------|
| `--script demo` | Run deterministic demo sequence |
| `--interactive` | Start interactive session |
| `--unicode auto\|on\|off` | Control Unicode rendering |
| `--width N` | Set terminal width (auto-detected if omitted) |

## Commands

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `scan` | Scan network for targets |
| `decrypt` | Decrypt intercepted data |
| `infiltrate <target>` | Infiltrate specified target |
| `hack` | Execute full hack sequence |
| `trace <target>` | Trace target location |
| `countertrace` / `evade` | Deploy countermeasures |
| `status` | Show system status |
| `clear` | Clear terminal screen |
| `exit` | Exit terminal |

## Visual Modes

**Compact Width (≤62 chars)**:
```
+=======================+
|   *** SCANNING ***    |
+=======================+
Progress: [###...] 50%
```

**Wide Width (≥100 chars)**:
```
╔═══════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                                    *** NETWORK INFILTRATION COMPLETE ***                            ║
╚═══════════════════════════════════════════════════════════════════════════════════════════════════════╝
Progress: [████████████████████████████████████████████████████████████████████████████████████████] 100%
```

## Demo Mode

```bash
python masterhacker.py --script demo
```

Runs a deterministic demonstration sequence with consistent output across all terminal sizes.

## Technical Notes

- **Modern Architecture** - Built with comprehensive type hints and state management patterns
- **Adaptive rendering** - Professional letterforms scale with terminal width
- **Thread-safe design** - Robust state management with validation and error handling
- **Zero dependencies** - Uses only Python standard library  
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Deterministic demo** - Consistent output for reliable demonstrations
- **Auto-detection** - Terminal width and Unicode capability probing
- **Production-ready** - Comprehensive documentation, type safety, and testing
- **For laughs only** - No actual hacking capabilities included

## License

MIT License - Feel free to hack the planet (responsibly).

---

*For entertainment purposes only. No actual hacking capabilities included.*