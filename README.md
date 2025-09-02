# Master Hacker Terminal

A tongue-in-cheek, movie-hacker terminal simulator that parodies Hollywood's over-the-top hacking scenes.

## Requirements

- Python 3.8+
- No dependencies (uses Python standard library only)

## Quick Start

```bash
# Run deterministic demo
python masterhacker.py --script demo

# Show banner and usage examples
python masterhacker.py

# Interactive mode
python masterhacker.py --interactive

# Force ASCII mode
python masterhacker.py --unicode off --script demo
```

## Examples

```bash
# Auto-detect Unicode support (default)
python masterhacker.py --unicode auto

# Force Unicode box-drawing characters
python masterhacker.py --unicode on --script demo

# ASCII-only mode for compatibility
python masterhacker.py --unicode off

# Single command execution
python masterhacker.py scan
python masterhacker.py infiltrate MAINFRAME-7
```

## Unicode Mode

The `--unicode` flag controls terminal art rendering:

- **`auto`** (default): Detect Unicode support automatically
- **`on`**: Force Unicode box-drawing characters (╔══╗ style)
- **`off`**: Use ASCII-only characters (+--+ style)

Auto-detection checks environment variables and terminal type for safe Unicode support.

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

## Demo Mode

```bash
python masterhacker.py --script demo
```

Runs a deterministic demonstration sequence:
- Always produces identical output (seeded random generation)
- Showcases all major features and terminal art
- Sequence: scan → infiltrate → hack → trace → countertrace → status → exit
- Perfect for screenshots and presentations

## ASCII vs Unicode Modes

**ASCII Mode** (`--unicode off`):
```
+============================================+
|        *** ACCESS GRANTED ***             |
+============================================+
Progress: [######....] 60%
```

**Unicode Mode** (`--unicode on`):
```
╔════════════════════════════════════════════╗
║        *** ACCESS GRANTED ***             ║
╚════════════════════════════════════════════╝
Progress: [██████░░░░] 60%
```

## Technical Notes

- **Single file implementation** - Everything in `masterhacker.py`
- **Zero dependencies** - Uses only Python standard library  
- **Cross-platform** - Works on Windows, macOS, and Linux
- **Deterministic demo** - Consistent output for reliable demonstrations
- **Auto Unicode detection** - Safe terminal capability probing
- **For laughs only** - No actual hacking capabilities included

## License

MIT License - Feel free to hack the planet (responsibly).

---

*For entertainment purposes only. No actual hacking capabilities included.*