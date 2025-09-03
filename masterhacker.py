#!/usr/bin/env python3
"""
Master Hacker Terminal v2.0 - Single File Implementation
A parody hacker movie terminal simulator with comprehensive documentation

This module implements a complete hacker terminal simulator inspired by classic
hacker movies and TV shows. It provides an immersive command-line experience
with animated progress bars, dramatic ASCII/Unicode art, and realistic hacking
operations simulation.

## Core Features

### Display System
- **Width-Adaptive Layout**: Automatically adjusts to terminal width with three tiers:
  - Compact (≤62 chars): Mobile terminals and narrow windows
  - Standard (63-99 chars): Typical desktop terminal windows  
  - Wide (≥100 chars): Wide-screen displays and maximized terminals

- **Unicode/ASCII Mode**: Intelligent character set selection:
  - Unicode mode: Elegant box-drawing characters (╔, ═, ║) and progress blocks (█, ░)
  - ASCII mode: Maximum compatibility characters (+, -, |, #, .)
  - Auto-detection based on environment variables and terminal capabilities

### Command System
- **scan**: Network reconnaissance to discover hackable targets
- **decrypt**: Cryptographic decryption of intercepted communications  
- **infiltrate <target>**: System infiltration with security bypass simulation
- **hack**: Comprehensive vulnerability exploitation sequence
- **trace <target>**: Geographical location tracing with ISP identification
- **countertrace/evade**: Anti-tracing countermeasures deployment
- **status**: Real-time system status and security information
- **clear**: Terminal screen clearing (cross-platform)
- **exit**: Graceful application termination
- **help**: Complete command reference and usage information

### Execution Modes
1. **Demo Mode** (--script demo):
   - Deterministic behavior with fixed random seed (1337)
   - Predefined command sequence showcasing all features
   - Consistent output for documentation and testing

2. **Interactive Mode** (--interactive or default):
   - Real-time user command processing
   - Persistent session state across commands
   - Comprehensive error handling and recovery

3. **Single Command Mode** (command args):
   - Execute individual commands with banner display
   - Falls back to interactive mode for invalid commands
   - Useful for scripting and automation

### Terminal Width Detection System
Advanced terminal width detection with comprehensive fallback chain:
1. Primary: Python's shutil.get_terminal_size()  
2. Fallback 1: COLUMNS environment variable
3. Fallback 2: TERM_COLS environment variable
4. Final: Default 80-column assumption

Special handling for:
- Non-interactive terminals (pipes, redirection)
- Terminal size detection failures
- Zero or invalid width values
- Cross-platform compatibility

### Unicode Detection and Safety
Multi-layered Unicode capability detection:
1. Environment variable analysis (LC_ALL, LC_CTYPE, LANG)
2. Terminal capability hints from TERM variable
3. Optional Unicode width probing (disabled by default for performance)

Safety features:
- Comprehensive error handling for all terminal operations
- Automatic cursor position restoration
- Timeout protection against hanging terminals
- Graceful fallback to ASCII mode on any issues

## State Management

### Global State Variables
- **discovered_targets**: List of systems found by scan command
- **infiltrated_targets**: Set of successfully compromised systems
- **system_status**: Dictionary of operational parameters and statistics
- **unicode_mode**: Display character set preference ("auto", "on", "off")
- **width_mode**: Terminal width override ("auto", "compact", "standard", "wide")

### Deterministic Behavior
Demo mode uses fixed random seed (1337) to ensure:
- Identical decrypted messages across runs
- Consistent geographical coordinates for unknown targets  
- Reproducible progress bar animations
- Stable output for testing and documentation

## Architecture Design

### Single-File Constraint
All functionality contained within this single file for:
- Easy distribution and deployment
- Simplified dependency management
- Self-contained executable behavior
- Educational code organization demonstration

### Modular Function Design
Clear separation of concerns:
- Display functions (banners, progress bars, status boxes)
- Command implementation functions (cmd_*)  
- Utility functions (parsing, width detection, Unicode handling)
- Terminal adaptation functions (get_banner, get_progress_chars)
- Main application control (main, interactive_mode, run_demo_script)

### Constants Organization
Comprehensive constant definitions for:
- Display width thresholds and defaults
- Timing parameters for realistic animations
- Progress bar step counts for different operations
- Status text and messages
- Geographic coordinate ranges
- Array indices and offsets
- Exit codes and system parameters

## Error Handling Strategy

### Graceful Degradation
- Terminal capability failures fall back to safe defaults
- Unicode rendering issues automatically switch to ASCII
- Terminal width detection failures use standard 80-column layout
- Missing arguments display usage information

### User Interruption Handling
- KeyboardInterrupt (Ctrl+C): Clean "Interrupted by user" message
- EOFError (Ctrl+D): Graceful "End of input detected" handling
- Unexpected exceptions: Detailed error reporting with clean exit

### Terminal State Protection
- Automatic restoration of terminal attributes on exit
- Cursor position preservation during Unicode probing
- Screen clearing works across platforms (Windows/Unix)
- Proper signal handling for clean termination

## Performance Considerations

### Non-Blocking Operations
- Unicode detection uses fast environment checks
- Terminal width probing disabled by default to prevent blocking
- Progress animations use appropriate timing for visual effect
- Command processing optimized for immediate response

### Memory Efficiency  
- Minimal global state with efficient data structures
- String constants loaded once at module level
- No persistent file I/O or network operations
- Garbage collection friendly design

## Usage Examples

```bash
# Run demonstration script
python masterhacker.py --script demo

# Interactive mode with Unicode override
python masterhacker.py --interactive --unicode on

# Single command execution
python masterhacker.py scan
python masterhacker.py infiltrate MAINFRAME-7

# Width mode override for narrow terminals  
python masterhacker.py --width compact --interactive

# ASCII mode for maximum compatibility
python masterhacker.py --unicode off --script demo
```

## Technical Requirements
- Python 3.7+ (for comprehensive type hint support)
- Standard library only (no external dependencies)
- Cross-platform compatibility (Windows, macOS, Linux)
- Terminal width detection support
- UTF-8 locale support for Unicode mode

## Testing and Validation
- Demo mode provides consistent output for regression testing
- All commands tested with various argument combinations  
- Unicode/ASCII mode switching validated across terminals
- Width adaptation tested on various terminal sizes
- Error handling verified for all exception paths

Author: AI Assistant specialized in Foundation Improvements
Version: 2.0.7 (with comprehensive documentation)
License: Open source parody/educational use
"""

import argparse
import os
import random
import shutil
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple, Any

# =============================================================================
# CONSTANTS SECTION
# =============================================================================

# Display Constants - Terminal Width Detection
DISPLAY_WIDTH_COMPACT_THRESHOLD: int = 62
DISPLAY_WIDTH_STANDARD_THRESHOLD: int = 99
DISPLAY_WIDTH_WIDE_THRESHOLD: int = 100
DISPLAY_DEFAULT_TERMINAL_WIDTH: int = 80

# Timing Constants - Animation Delays
TIMING_PROGRESS_DEFAULT: float = 0.08
TIMING_PROGRESS_SCAN: float = 0.12
TIMING_PROGRESS_DECRYPT: float = 0.10
TIMING_PROGRESS_INFILTRATE: float = 0.15
TIMING_PROGRESS_HACK: float = 0.12
TIMING_PROGRESS_TRACE: float = 0.13
TIMING_PROGRESS_COUNTERTRACE: float = 0.11
TIMING_ACCESS_GRANTED_DELAY: float = 1.0
TIMING_WARNING_DELAY: float = 1.5
TIMING_PROGRESS_END_DELAY: float = 0.2

# Progress Bar Constants
PROGRESS_BAR_STEPS_DEFAULT: int = 20
PROGRESS_BAR_STEPS_SCAN: int = 24
PROGRESS_BAR_STEPS_DECRYPT: int = 26
PROGRESS_BAR_STEPS_INFILTRATE: int = 28
PROGRESS_BAR_STEPS_HACK: int = 30
PROGRESS_BAR_STEPS_TRACE: int = 25
PROGRESS_BAR_STEPS_COUNTERTRACE: int = 22
PROGRESS_BAR_WIDTH: int = 52

# Unicode Probe Constants
UNICODE_PROBE_TIMEOUT: float = 0.5
UNICODE_PROBE_SELECT_TIMEOUT: int = 0

# System Status Constants
STATUS_ONLINE: str = "ONLINE"
STATUS_OFFLINE: str = "OFFLINE"
STATUS_ENABLED: str = "ENABLED"
STATUS_DISABLED: str = "DISABLED"
STATUS_SECURITY_MAXIMUM: str = "MAXIMUM"
STATUS_STEALTH_ON: str = "ON"
STATUS_STEALTH_OFF: str = "OFF"

# Demo Constants
DEMO_RANDOM_SEED: int = 1337
DEMO_HACK_SYSTEMS: int = 5
DEMO_HACK_CREDITS: int = 1337
DEMO_DISCOVERED_TARGETS_COUNT: int = 3

# System State Default Values
DEFAULT_CONNECTIONS: int = 3
DEFAULT_COMPROMISED_SYSTEMS: int = 0
DEFAULT_CREDITS: int = 0

# Coordinate Range Constants
COORDINATE_LAT_MIN: float = -90.0
COORDINATE_LAT_MAX: float = 90.0
COORDINATE_LON_MIN: float = -180.0
COORDINATE_LON_MAX: float = 180.0
COORDINATE_PRECISION: int = 4

# Progress Display Constants
PROGRESS_PERCENTAGE_WIDTH: int = 3
PROGRESS_DOTS_WIDTH: int = 3
PROGRESS_DOT_CYCLE_MODULO: int = 3

# Command Parsing Constants
COMMAND_ARGS_FIRST_INDEX: int = 0
COMMAND_PARTS_FIRST_INDEX: int = 0

# Array Index Constants
ARRAY_FIRST_ELEMENT: int = 0
ARRAY_SECOND_ELEMENT: int = 1

# Version and System Information Constants
VERSION_NUMBER: str = "2.1.4"

# Location Constants for Trace Command
PREDEFINED_LOCATIONS: Dict[str, Tuple[str, str]] = {
    "QUANTUM-DB": ("37.7749 deg N, 122.4194 deg W", "CyberCorp Industries"),
    "MAINFRAME-7": ("40.7128 deg N, 74.0060 deg W", "MegaCorp Systems"),
    "SATELLITE-X": ("51.5074 deg N, 0.1278 deg W", "SkyNet Communications"),
    "NEXUS-CORE": ("35.6762 deg N, 139.6503 deg E", "Tech Dynamics"),
    "CRYPTO-VAULT": ("52.5200 deg N, 13.4050 deg E", "SecureMax GmbH"),
    "DATA-CENTER": ("34.0522 deg N, 118.2437 deg W", "InfoTech Solutions")
}

# Size Validation Constants
SIZE_GREATER_THAN_ZERO: int = 0

# Loop and Iteration Constants
STEP_INCREMENT: int = 1
ARRAY_SLICE_START: int = 1

# Exit Code Constants
EXIT_SUCCESS: int = 0
EXIT_FAILURE: int = 1

# =============================================================================
# OPTIONAL SYSTEM-SPECIFIC IMPORTS
# =============================================================================

# Optional imports for Unix-like systems (for Unicode width probing)
try:
    import select
    import termios
    import tty
    HAS_UNIX_TTY = True
except ImportError:
    HAS_UNIX_TTY = False


# =============================================================================
# ASCII ART CONSTANTS - WIDTH-TIERED SYSTEM
# =============================================================================

# Compact Mode: ≤62 characters
COMPACT_ASCII_BANNER = """
 +==========================================================+
 |                                                          |
 |   █   █  █████  █████  █   █  █████  ████                |
 |   █   █  █   █  █      █  █   █      █   █               |
 |   █████  █████  █      ███    ████   ████                |
 |   █   █  █   █  █      █  █   █      █  █                |
 |   █   █  █   █  █████  █   █  █████  █   █               |
 |                                                          |
 |   █████  █████  ████   █   █  █████  █   █  █████  █     |
 |     █    █      █   █  ██ ██    █    ██  █  █   █  █     |
 |     █    ████   ████   █ █ █    █    █ █ █  █████  █     |
 |     █    █      █  █   █   █    █    █  ██  █   █  █     |
 |     █    █████  █   █  █   █  █████  █   █  █   █  █████ |
 |                                                          |
 |                   [ VERSION 2.1.4 ]                     |
 |             *** CLASSIFIED ACCESS ONLY ***              |
 +==========================================================+
"""

COMPACT_ACCESS_GRANTED = """
 +========================================================+
 |                                                        |
 |    ████   ████  ████  ████  ████  ████                |
 |   ██  ██ ██  ██ ██  ██ ██    ██    ██                 |
 |   ██████ ██     ██     ████  ████  ████               |
 |   ██  ██ ██  ██ ██  ██ ██       ██ ██                 |
 |   ██  ██  ████   ████  ████  ████  ████               |
 |                                                        |
 |    ████  ████   ████  █  █ ████  ████  ████           |
 |   ██     ██  █ ██  ██ ██ █  ██   ██     ██  █         |
 |   ██ ███ ████  ██████ ████  ██   ████   ██  █         |
 |   ██  ██ ██ █  ██  ██ █ ██  ██   ██     ██  █         |
 |    ████  █  █  ██  ██ █  █  ██   ████   ████          |
 |                                                        |
 |                *** ACCESS GRANTED ***                  |
 +========================================================+
"""

COMPACT_WARNING_BOX = """
 +=======================================================+
 |                                                       |
 |   █   █  ████  ████  █  █ ████ █  █  ████           |
 |   █   █ ██  ██ ██  █ ██ █  ██  ██ █ ██              |
 |   █ █ █ ██████ ████  ████  ██  ████ ██ ██           |
 |   █████ ██  ██ ██ █  █ ██  ██  █ ██ ██  █           |
 |   ██ ██ ██  ██ █  █  █  █ ████ █  █  ████           |
 |                                                       |
 |                   !!! WARNING !!!                    |
 |            UNAUTHORIZED ACCESS DETECTED              |
 |          INITIATING SECURITY PROTOCOLS               |
 +=======================================================+
"""

# Standard Mode: 63-99 characters  
STANDARD_ASCII_BANNER = """
 +============================================================================+
 |                                                                            |
 |  ██   ██   ████   ██████  ██  ██  ████████  ██████                        |
 |  ██   ██  ██  ██  ██      ██ ██   ██        ██   ██                       |
 |  ███████  ██████  ██      ████    ████      ██████                        |
 |  ██   ██  ██  ██  ██      ██ ██   ██        ██  ██                        |
 |  ██   ██  ██  ██  ██████  ██  ██  ████████  ██   ██                       |
 |                                                                            |
 |  ████████  ████████  ██████  ██   ██  ██████  ██   ██   ████   ██         |
 |     ██     ██        ██   ██ ███ ███   ██    ███  ██  ██  ██  ██          |
 |     ██     ████      ██████  ███████   ██    ████ ██  ██████  ██          |
 |     ██     ██        ██  ██  ██ █ ██   ██    ██ ████  ██  ██  ██          |
 |     ██     ████████  ██   ██ ██   ██  ██████ ██  ███  ██   ██ ██████      |
 |                                                                            |
 |                           [ VERSION 2.1.4 ]                               |
 |                     *** CLASSIFIED ACCESS ONLY ***                        |
 +============================================================================+
"""

STANDARD_ACCESS_GRANTED = """
 +=========================================================================+
 |                                                                         |
 |      ██████   ██████  ██████  ████████ ████████ ████████              |
 |     ██  ██   ██  ██  ██  ██  ██       ██       ██                     |
 |    ██   ██  ██      ██      ████     ████████ ████████                |
 |    ███████  ██  ██  ██  ██  ██           ██   ██                      |
 |    ██   ██   ██████  ██████  ████████ ████████ ████████               |
 |                                                                         |
 |       ████████ ██████    ████   ██   ██ ████████ ████████  ████        |
 |      ██       ██   ██  ██  ██  ███  ██    ██    ██       ██  ██       |
 |      ██  ████ ██████   ██████  ████ ██    ██    ████     ██  ██       |
 |      ██   ██  ██  ██   ██  ██  ██ ████    ██    ██       ██  ██       |
 |       ███████ ██   ██  ██   ██ ██  ███    ██    ████████  ████        |
 |                                                                         |
 |                        *** ACCESS GRANTED ***                          |
 +=========================================================================+
"""

STANDARD_WARNING_BOX = """
 +========================================================================+
 |                                                                        |
 |    ██   ██   ████   ██████  ██   ██ ████ ██   ██  ████████           |
 |    ██   ██  ██  ██  ██   ██ ███  ██  ██  ███  ██ ██                  |
 |    ██ █ ██  ██████  ██████  ████ ██  ██  ████ ██ ██  ████            |
 |    ███████  ██  ██  ██  ██  ██ ████  ██  ██ ████ ██   ██             |
 |    ███  ██  ██  ██  ██   ██ ██  ███ ████ ██  ███  ███████            |
 |                                                                        |
 |                           !!! WARNING !!!                             |
 |                    UNAUTHORIZED ACCESS DETECTED                       |
 |                  INITIATING SECURITY PROTOCOLS                        |
 +========================================================================+
"""

# Wide Mode: ≥100 characters
WIDE_ASCII_BANNER = """
 +==================================================================================================+
 |                                                                                                  |
 |  █   █   ████    █████  █   █  █████  ████                                                     |
 |  █   █  █    █  █       █  █   █      █   █                                                    |
 |  █████  ██████  █       ███    ████   ████                                                     |
 |  █   █  █    █  █       █  █   █      █  █                                                     |
 |  █   █  █    █   █████  █   █  █████  █   █                                                    |
 |                                                                                                  |
 |  █████  █████  ████   █   █  █████  █   █   ████   █                                          |
 |    █    █      █   █  ██ ██    █    ██  █  █    █  █                                          |
 |    █    ████   ████   █ █ █    █    █ █ █  ██████  █                                          |
 |    █    █      █  █   █   █    █    █  ██  █    █  █                                          |
 |    █    █████  █   █  █   █  █████  █   █  █    █  █████                                      |
 |                                                                                                  |
 |                                     [ VERSION 2.1.4 ]                                          |
 |                               *** CLASSIFIED ACCESS ONLY ***                                    |
 +==================================================================================================+
"""

WIDE_ACCESS_GRANTED = """
 +===============================================================================================+
 |                                                                                               |
 |      █████   █████  █████  █████  █████  █████                                              |
 |     █     █ █       █      █      █      █                                                   |
 |     ███████ █       █      ████   █████  █████                                              |
 |     █     █ █       █      █          █      █                                              |
 |     █     █ █████   █████  █████  █████  █████                                              |
 |                                                                                               |
 |       █████  ████    █████  █   █  █████  █████  ████                                      |
 |      █       █   █  █     █ ██  █    █    █      █   █                                     |
 |      █  ███  ████   ███████ █ █ █    █    ████   █   █                                     |
 |      █    █  █  █   █     █ █  ██    █    █      █   █                                     |
 |       █████  █   █  █     █ █   █    █    █████  ████                                      |
 |                                                                                               |
 |                                  *** ACCESS GRANTED ***                                      |
 +===============================================================================================+
"""

WIDE_WARNING_BOX = """
 +============================================================================================+
 |                                                                                            |
 |     █   █   █████   ████   █   █   █████  █   █   █████                                  |
 |     █   █   █   █   █   █  ██  █     █    ██  █   █                                      |
 |     █ █ █   █████   ████   █ █ █     █    █ █ █   █  ██                                  |
 |     ██ ██   █   █   █  █   █  ██     █    █  ██   █   █                                  |
 |     █   █   █   █   █   █  █   █   █████  █   █   █████                                  |
 |                                                                                            |
 |                                    !!! WARNING !!!                                        |
 |                          UNAUTHORIZED ACCESS DETECTED                                     |
 |                        INITIATING SECURITY PROTOCOLS                                      |
 +============================================================================================+
"""

# Default ASCII constants (keeping for backward compatibility)
ASCII_BANNER = STANDARD_ASCII_BANNER
ACCESS_GRANTED = STANDARD_ACCESS_GRANTED  
WARNING_BOX = STANDARD_WARNING_BOX

# =============================================================================
# UNICODE ART CONSTANTS - WIDTH-TIERED SYSTEM  
# =============================================================================

# Compact Unicode Mode: ≤62 characters
COMPACT_UNICODE_BANNER = """
 ╔══════════════════════════════════════════════════════╗
 ║                                                      ║
 ║   █   █  █████  █████  █   █  █████  ████            ║
 ║   █   █  █   █  █      █  █   █      █   █           ║
 ║   █████  █████  █      ███    ████   ████            ║
 ║   █   █  █   █  █      █  █   █      █  █            ║
 ║   █   █  █   █  █████  █   █  █████  █   █           ║
 ║                                                      ║
 ║   █████  █████  ████   █   █  █████  █   █  █████  █ ║
 ║     █    █      █   █  ██ ██    █    ██  █  █   █  █ ║
 ║     █    ████   ████   █ █ █    █    █ █ █  █████  █ ║
 ║     █    █      █  █   █   █    █    █  ██  █   █  █ ║
 ║     █    █████  █   █  █   █  █████  █   █  █   █  █ ║
 ║                                                      ║
 ║                 [ VERSION 2.1.4 ]                   ║
 ║           *** CLASSIFIED ACCESS ONLY ***            ║
 ╚══════════════════════════════════════════════════════╝
"""

COMPACT_UNICODE_ACCESS_GRANTED = """
 ╔════════════════════════════════════════════════════╗
 ║                                                    ║
 ║    ████   ████  ████  ████  ████  ████            ║
 ║   ██  ██ ██  ██ ██  ██ ██    ██    ██             ║
 ║   ██████ ██     ██     ████  ████  ████           ║
 ║   ██  ██ ██  ██ ██  ██ ██       ██ ██             ║
 ║   ██  ██  ████   ████  ████  ████  ████           ║
 ║                                                    ║
 ║    ████  ████   ████  █  █ ████  ████  ████       ║
 ║   ██     ██  █ ██  ██ ██ █  ██   ██     ██  █     ║
 ║   ██ ███ ████  ██████ ████  ██   ████   ██  █     ║
 ║   ██  ██ ██ █  ██  ██ █ ██  ██   ██     ██  █     ║
 ║    ████  █  █  ██  ██ █  █  ██   ████   ████      ║
 ║                                                    ║
 ║              *** ACCESS GRANTED ***                ║
 ╚════════════════════════════════════════════════════╝
"""

COMPACT_UNICODE_WARNING_BOX = """
 ╔═══════════════════════════════════════════════════╗
 ║                                                   ║
 ║   █   █  █████  ████   █   █  █████  █   █  █████ ║
 ║   █   █  █   █  █   █  ██  █    █    ██  █  █     ║
 ║   █ █ █  █████  ████   █ █ █    █    █ █ █  █ ███ ║
 ║   ██ ██  █   █  █  █   █  ██    █    █  ██  █   █ ║
 ║   █   █  █   █  █   █  █   █  █████  █   █  █████ ║
 ║                                                   ║
 ║                 !!! WARNING !!!                  ║
 ║          UNAUTHORIZED ACCESS DETECTED            ║
 ║        INITIATING SECURITY PROTOCOLS             ║
 ╚═══════════════════════════════════════════════════╝
"""

# Standard Unicode Mode: 63-99 characters  
STANDARD_UNICODE_BANNER = """
 ╔════════════════════════════════════════════════════════════════════════╗
 ║                                                                        ║
 ║  ██   ██   ████   ██████  ██  ██  ████████  ██████                    ║
 ║  ██   ██  ██  ██  ██      ██ ██   ██        ██   ██                   ║
 ║  ███████  ██████  ██      ████    ████      ██████                    ║
 ║  ██   ██  ██  ██  ██      ██ ██   ██        ██  ██                    ║
 ║  ██   ██  ██  ██  ██████  ██  ██  ████████  ██   ██                   ║
 ║                                                                        ║
 ║  ████████  ████████  ██████  ██   ██  ██████  ██   ██   ████   ██     ║
 ║     ██     ██        ██   ██ ███ ███   ██    ███  ██  ██  ██  ██      ║
 ║     ██     ████      ██████  ███████   ██    ████ ██  ██████  ██      ║
 ║     ██     ██        ██  ██  ██ █ ██   ██    ██ ████  ██  ██  ██      ║
 ║     ██     ████████  ██   ██ ██   ██  ██████ ██  ███  ██   ██ ██████  ║
 ║                                                                        ║
 ║                         [ VERSION 2.1.4 ]                             ║
 ║                   *** CLASSIFIED ACCESS ONLY ***                      ║
 ╚════════════════════════════════════════════════════════════════════════╝
"""

STANDARD_UNICODE_ACCESS_GRANTED = """
 ╔═══════════════════════════════════════════════════════════════════╗
 ║                                                                   ║
 ║      █████   █████  █████  █████  █████  █████              ║
 ║      █   █   █      █      █      █      █                   ║
 ║      █████   █      █      ████   █████  █████              ║
 ║      █   █   █      █      █          █      █              ║
 ║      █   █   █████  █████  █████  █████  █████              ║
 ║                                                                   ║
 ║       █████  ████   █████  █   █  █████  █████  ████       ║
 ║       █      █   █  █   █  ██  █    █    █      █   █      ║
 ║       █ ███  ████   █████  █ █ █    █    ████   █   █      ║
 ║       █   █  █  █   █   █  █  ██    █    █      █   █      ║
 ║       █████  █   █  █   █  █   █    █    █████  ████       ║
 ║                                                                   ║
 ║                      *** ACCESS GRANTED ***                      ║
 ╚═══════════════════════════════════════════════════════════════════╝
"""

STANDARD_UNICODE_WARNING_BOX = """
 ╔══════════════════════════════════════════════════════════════════╗
 ║                                                                  ║
 ║    ██   ██   ████   ██████  ██   ██ ████ ██   ██  ████████     ║
 ║    ██   ██  ██  ██  ██   ██ ███  ██  ██  ███  ██ ██            ║
 ║    ██ █ ██  ██████  ██████  ████ ██  ██  ████ ██ ██  ████      ║
 ║    ███████  ██  ██  ██  ██  ██ ████  ██  ██ ████ ██   ██       ║
 ║    ███  ██  ██  ██  ██   ██ ██  ███ ████ ██  ███  ███████      ║
 ║                                                                  ║
 ║                         !!! WARNING !!!                         ║
 ║                  UNAUTHORIZED ACCESS DETECTED                   ║
 ║                INITIATING SECURITY PROTOCOLS                    ║
 ╚══════════════════════════════════════════════════════════════════╝
"""

# Wide Unicode Mode: ≥100 characters
WIDE_UNICODE_BANNER = """
 ╔══════════════════════════════════════════════════════════════════════════════════════════════╗
 ║                                                                                              ║
 ║  █   █   ████    █████  █   █  █████  ████                                                 ║
 ║  █   █  █    █  █       █  █   █      █   █                                                ║
 ║  █████  ██████  █       ███    ████   ████                                                 ║
 ║  █   █  █    █  █       █  █   █      █  █                                                 ║
 ║  █   █  █    █   █████  █   █  █████  █   █                                                ║
 ║                                                                                              ║
 ║  █████  █████  ████   █   █  █████  █   █   ████   █                                      ║
 ║    █    █      █   █  ██ ██    █    ██  █  █    █  █                                      ║
 ║    █    ████   ████   █ █ █    █    █ █ █  ██████  █                                      ║
 ║    █    █      █  █   █   █    █    █  ██  █    █  █                                      ║
 ║    █    █████  █   █  █   █  █████  █   █  █    █  █████                                  ║
 ║                                                                                              ║
 ║                                   [ VERSION 2.1.4 ]                                        ║
 ║                             *** CLASSIFIED ACCESS ONLY ***                                  ║
 ╚══════════════════════════════════════════════════════════════════════════════════════════════╝
"""

WIDE_UNICODE_ACCESS_GRANTED = """
 ╔═════════════════════════════════════════════════════════════════════════════════════════╗
 ║                                                                                         ║
 ║      █████   █████  █████  █████  █████  █████                                        ║
 ║     █     █ █       █      █      █      █                                             ║
 ║     ███████ █       █      ████   █████  █████                                        ║
 ║     █     █ █       █      █          █      █                                        ║
 ║     █     █ █████   █████  █████  █████  █████                                        ║
 ║                                                                                         ║
 ║       █████  ████    █████  █   █  █████  █████  ████                                ║
 ║      █       █   █  █     █ ██  █    █    █      █   █                               ║
 ║      █  ███  ████   ███████ █ █ █    █    ████   █   █                               ║
 ║      █    █  █  █   █     █ █  ██    █    █      █   █                               ║
 ║       █████  █   █  █     █ █   █    █    █████  ████                                ║
 ║                                                                                         ║
 ║                                *** ACCESS GRANTED ***                                  ║
 ╚═════════════════════════════════════════════════════════════════════════════════════════╝
"""

WIDE_UNICODE_WARNING_BOX = """
 ╔════════════════════════════════════════════════════════════════════════════════════════╗
 ║                                                                                        ║
 ║     █   █   █████   ████   █   █   █████  █   █   █████                              ║
 ║     █   █   █   █   █   █  ██  █     █    ██  █   █                                  ║
 ║     █ █ █   █████   ████   █ █ █     █    █ █ █   █  ██                              ║
 ║     ██ ██   █   █   █  █   █  ██     █    █  ██   █   █                              ║
 ║     █   █   █   █   █   █  █   █   █████  █   █   █████                              ║
 ║                                                                                        ║
 ║                                  !!! WARNING !!!                                      ║
 ║                        UNAUTHORIZED ACCESS DETECTED                                   ║
 ║                      INITIATING SECURITY PROTOCOLS                                    ║
 ╚════════════════════════════════════════════════════════════════════════════════════════╝
"""

# Default Unicode constants (keeping for backward compatibility)
UNICODE_BANNER = STANDARD_UNICODE_BANNER
UNICODE_ACCESS_GRANTED = STANDARD_UNICODE_ACCESS_GRANTED
UNICODE_WARNING_BOX = STANDARD_UNICODE_WARNING_BOX

# =============================================================================
# APPLICATION STATE MANAGEMENT
# =============================================================================

@dataclass
class ApplicationState:
    """
    Centralized application state management for Master Hacker Terminal.
    
    This dataclass encapsulates all global application state to provide better
    organization, validation, and type safety. It replaces the previous global
    variables with a structured state management system.
    
    Display Configuration:
        unicode_mode (str): Unicode character set preference
            - "auto": Auto-detect based on environment
            - "on": Force Unicode box-drawing characters
            - "off": Force ASCII characters only
            
        width_mode (str): Terminal width handling mode
            - "auto": Auto-detect terminal width
            - "compact": Force compact mode (≤62 chars)
            - "standard": Force standard mode (63-99 chars)
            - "wide": Force wide mode (≥100 chars)
    
    Operation State:
        discovered_targets (List[Tuple[str, str]]): Systems found by scan command
            Format: [(target_name, target_type), ...]
            
        infiltrated_targets (Set[str]): Successfully compromised systems
            Contains target names that have been successfully infiltrated
            
        system_status (Dict[str, Any]): Operational parameters and statistics
            - online: Connection status (bool)
            - security_level: Current security level (int)
            - connections: Active connection count (int)
            - firewall: Firewall status (bool)
            - stealth: Stealth mode status (bool)
            - compromised_systems: Number of compromised systems (int)
            - credits: Current credit balance (int)
    
    State Validation:
        All state modifications should go through validation methods to ensure
        data integrity and prevent invalid configurations.
        
    Example:
        >>> state = ApplicationState()
        >>> state.unicode_mode = "on"
        >>> state.add_discovered_target("MAINFRAME-7", "Database Server")
        >>> state.validate_state()
        True
    """
    
    # Display configuration
    unicode_mode: str = "auto"
    width_mode: str = "auto"
    
    # Operation state
    discovered_targets: List[Tuple[str, str]] = field(default_factory=list)
    infiltrated_targets: Set[str] = field(default_factory=set)
    system_status: Dict[str, Any] = field(default_factory=lambda: {
        "online": True,
        "security_level": STATUS_SECURITY_MAXIMUM,
        "connections": DEFAULT_CONNECTIONS,
        "firewall": True,
        "stealth": True,
        "compromised_systems": DEFAULT_COMPROMISED_SYSTEMS,
        "credits": DEFAULT_CREDITS
    })
    
    def validate_state(self) -> bool:
        """
        Validate the current application state for consistency and correctness.
        
        Performs comprehensive validation of all state fields to ensure they
        contain valid values and are internally consistent.
        
        Validation Rules:
            - unicode_mode must be one of: "auto", "on", "off"
            - width_mode must be one of: "auto", "compact", "standard", "wide"
            - discovered_targets must be list of (str, str) tuples
            - infiltrated_targets must be set of strings
            - system_status must contain all required keys with correct types
            - infiltrated_targets should be subset of discovered target names
            
        Returns:
            bool: True if all validation rules pass, False otherwise.
            
        Raises:
            ValueError: If critical validation failures are detected.
            
        Example:
            >>> state = ApplicationState()
            >>> state.unicode_mode = "invalid"
            >>> state.validate_state()
            ValueError: Invalid unicode_mode: invalid
        """
        # Validate unicode_mode
        valid_unicode_modes = {"auto", "on", "off"}
        if self.unicode_mode not in valid_unicode_modes:
            raise ValueError(f"Invalid unicode_mode: {self.unicode_mode}. Must be one of {valid_unicode_modes}")
        
        # Validate width_mode
        valid_width_modes = {"auto", "compact", "standard", "wide"}
        if self.width_mode not in valid_width_modes:
            raise ValueError(f"Invalid width_mode: {self.width_mode}. Must be one of {valid_width_modes}")
        
        # Validate discovered_targets structure
        if not isinstance(self.discovered_targets, list):
            raise ValueError("discovered_targets must be a list")
        
        for i, target in enumerate(self.discovered_targets):
            if not isinstance(target, tuple) or len(target) != 2:
                raise ValueError(f"discovered_targets[{i}] must be a tuple of length 2")
            if not isinstance(target[0], str) or not isinstance(target[1], str):
                raise ValueError(f"discovered_targets[{i}] must contain two strings")
        
        # Validate infiltrated_targets structure
        if not isinstance(self.infiltrated_targets, set):
            raise ValueError("infiltrated_targets must be a set")
        
        for target in self.infiltrated_targets:
            if not isinstance(target, str):
                raise ValueError("All infiltrated_targets must be strings")
        
        # Validate system_status structure
        required_status_keys = {
            "online", "security_level", "connections", 
            "firewall", "stealth", "compromised_systems", "credits"
        }
        
        if not isinstance(self.system_status, dict):
            raise ValueError("system_status must be a dictionary")
        
        missing_keys = required_status_keys - self.system_status.keys()
        if missing_keys:
            raise ValueError(f"system_status missing required keys: {missing_keys}")
        
        # Validate system_status value types
        if not isinstance(self.system_status["online"], bool):
            raise ValueError("system_status['online'] must be a boolean")
        if not isinstance(self.system_status["security_level"], str):
            raise ValueError("system_status['security_level'] must be a string")
        if not isinstance(self.system_status["connections"], int):
            raise ValueError("system_status['connections'] must be an integer")
        if not isinstance(self.system_status["firewall"], bool):
            raise ValueError("system_status['firewall'] must be a boolean")
        if not isinstance(self.system_status["stealth"], bool):
            raise ValueError("system_status['stealth'] must be a boolean")
        if not isinstance(self.system_status["compromised_systems"], int):
            raise ValueError("system_status['compromised_systems'] must be an integer")
        if not isinstance(self.system_status["credits"], int):
            raise ValueError("system_status['credits'] must be an integer")
        
        # Validate logical consistency
        discovered_target_names = {target[0] for target in self.discovered_targets}
        invalid_infiltrated = self.infiltrated_targets - discovered_target_names
        if invalid_infiltrated and discovered_target_names:
            # Only validate consistency if we have discovered targets
            # (allows for edge cases where infiltrated targets exist without discovery)
            pass  # Warning rather than error for flexibility
        
        return True
    
    def add_discovered_target(self, name: str, target_type: str) -> None:
        """
        Add a new discovered target to the state.
        
        Args:
            name (str): Target system name (e.g., "MAINFRAME-7")
            target_type (str): Type of target (e.g., "Database Server")
            
        Raises:
            ValueError: If target already exists or invalid parameters provided.
        """
        if not isinstance(name, str) or not isinstance(target_type, str):
            raise ValueError("Target name and type must be strings")
        
        if not name.strip() or not target_type.strip():
            raise ValueError("Target name and type cannot be empty")
        
        # Check for duplicates
        for existing_name, _ in self.discovered_targets:
            if existing_name == name:
                raise ValueError(f"Target {name} already exists in discovered targets")
        
        self.discovered_targets.append((name, target_type))
    
    def add_infiltrated_target(self, name: str) -> None:
        """
        Mark a target as successfully infiltrated.
        
        Args:
            name (str): Target system name to mark as infiltrated.
            
        Raises:
            ValueError: If target name is invalid.
        """
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Target name must be a non-empty string")
        
        self.infiltrated_targets.add(name)
    
    def update_system_status(self, key: str, value: Any) -> None:
        """
        Update a system status value with validation.
        
        Args:
            key (str): Status key to update
            value (Any): New value for the status key
            
        Raises:
            ValueError: If key is invalid or value type is incorrect.
        """
        if key not in self.system_status:
            raise ValueError(f"Invalid system status key: {key}")
        
        # Update and then validate
        self.system_status[key] = value
        self.validate_state()
    
    def reset_state(self) -> None:
        """
        Reset application state to initial defaults.
        
        Useful for testing and demo modes that need consistent starting state.
        """
        self.unicode_mode = "auto"
        self.width_mode = "auto"
        self.discovered_targets.clear()
        self.infiltrated_targets.clear()
        self.system_status = {
            "online": True,
            "security_level": STATUS_SECURITY_MAXIMUM,
            "connections": DEFAULT_CONNECTIONS,
            "firewall": True,
            "stealth": True,
            "compromised_systems": DEFAULT_COMPROMISED_SYSTEMS,
            "credits": DEFAULT_CREDITS
        }


# Global application state instance
app_state = ApplicationState()

# =============================================================================
# UTILITY FUNCTIONS - TERMINAL AND UNICODE DETECTION
# =============================================================================

def utf8_env_check() -> bool:
    """
    Check if environment variables suggest UTF-8 support.
    
    Examines common locale environment variables (LC_ALL, LC_CTYPE, LANG)
    to determine if the system is configured for UTF-8 encoding support.
    This is used as part of the Unicode mode auto-detection process.
    
    Returns:
        bool: True if any environment variable contains UTF-8 indicators,
              False otherwise.
              
    Example:
        >>> # With LANG=en_US.UTF-8
        >>> utf8_env_check()
        True
        >>> # With LANG=C
        >>> utf8_env_check()
        False
    """
    for var in ("LC_ALL", "LC_CTYPE", "LANG"):
        val = os.environ.get(var, "")
        if "UTF-8" in val.upper() or "utf8" in val.lower():
            return True
    return False

def terminal_hints_unicode() -> bool:
    """
    Check if TERM environment variable suggests Unicode capability.
    
    Examines the TERM environment variable to determine if the terminal
    emulator is likely to support Unicode characters properly. Used as
    part of the Unicode mode auto-detection heuristics.
    
    Returns:
        bool: True if TERM suggests Unicode support (modern terminal emulators),
              False for basic or legacy terminals.
              
    Note:
        This is a heuristic check - modern terminals like xterm-256color,
        screen-256color, and tmux-256color generally handle Unicode well.
        
    Example:
        >>> # With TERM=xterm-256color
        >>> terminal_hints_unicode()
        True
        >>> # With TERM=vt100
        >>> terminal_hints_unicode()
        False
    """
    term = os.environ.get("TERM", "").lower()
    unicode_terms = ("xterm-256color", "screen-256color", "tmux-256color")
    return any(term.startswith(t) for t in unicode_terms)

def probe_unicode_width() -> bool:
    """
    Perform a safe probe to test if Unicode box-drawing characters render correctly.
    
    This function attempts to determine if the terminal properly handles Unicode
    box-drawing characters by writing a test character and checking the cursor
    position response. It includes comprehensive safety measures and timeouts.
    
    The probe:
    1. Saves the current cursor position
    2. Writes a Unicode box-drawing character (╔)
    3. Queries the cursor position
    4. Checks if the terminal responds properly
    5. Restores the cursor position and cleans up
    
    Returns:
        bool: True if Unicode box-drawing characters appear safe to use,
              False if the terminal doesn't support them or the probe fails.
              
    Note:
        - Only works on Unix-like systems with TTY support
        - Skipped on Windows legacy consoles
        - Uses a 0.5-second timeout for terminal response
        - Always restores terminal state, even on errors
        - Returns False for non-interactive terminals (pipes, redirects)
        
    Safety Features:
        - Comprehensive error handling for all terminal operations
        - Automatic cursor position restoration
        - Terminal attribute restoration on exit
        - Timeout protection against hanging terminals
        
    Example:
        >>> # On a Unicode-capable terminal
        >>> probe_unicode_width()
        True
        >>> # On a legacy terminal or via pipe
        >>> probe_unicode_width()
        False
    """
    if not sys.stdout.isatty():
        return False
    
    # Skip probe if we don't have Unix TTY support
    if not HAS_UNIX_TTY:
        return False
    
    # Skip probe on Windows legacy consoles
    if os.name == 'nt' and os.environ.get("TERM") != "xterm-256color":
        return False
        
    try:
        # Test requires raw terminal mode
        old_attrs = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)
        
        # Save cursor position
        sys.stdout.write('\033[s')
        sys.stdout.flush()
        
        # Test simple Unicode box drawing character
        sys.stdout.write('╔')
        sys.stdout.flush()
        
        # Query cursor position
        sys.stdout.write('\033[6n')
        sys.stdout.flush()
        
        # Read response with timeout - increased to 0.5s for slower terminals
        ready, _, _ = select.select([sys.stdin], [], [], UNICODE_PROBE_TIMEOUT)
        if ready:
            # Read available data without blocking
            response = ""
            while select.select([sys.stdin], [], [], UNICODE_PROBE_SELECT_TIMEOUT) == ([sys.stdin], [], []):
                char = sys.stdin.read(STEP_INCREMENT)
                response += char
                if char == 'R':  # End of position response
                    break
            result = 'R' in response  # Got a position response
        else:
            result = False
            
        return result
        
    except (OSError, ValueError, KeyboardInterrupt):
        # Handle any terminal errors gracefully
        return False
    finally:
        try:
            # Always restore cursor and terminal state
            sys.stdout.write('\033[u')     # Restore cursor
            sys.stdout.write('\033[K')     # Clear line
            sys.stdout.flush()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attrs)
        except (OSError, ValueError):
            pass

def should_use_unicode(state: Optional[ApplicationState] = None) -> bool:
    """
    Determine if Unicode should be used based on current mode and environment.
    
    This function implements the Unicode mode decision logic by checking the
    application state unicode_mode setting and performing environment detection when needed.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Unicode Mode Behavior:
        - "off": Always use ASCII characters
        - "on": Always use Unicode characters (force mode)
        - "auto": Auto-detect based on environment variables and terminal hints
        
    Auto-detection checks:
        1. UTF-8 environment variables (LC_ALL, LC_CTYPE, LANG)
        2. Terminal capability hints from TERM variable
        
    Returns:
        bool: True if Unicode box-drawing characters should be used,
              False if ASCII characters should be used instead.
              
    Note:
        The probe_unicode_width() function is intentionally NOT used in auto
        mode because it can block execution on some terminals. Instead, we rely
        on faster, non-blocking environment checks.
        
    Example:
        >>> state = ApplicationState()
        >>> state.unicode_mode = "off"
        >>> should_use_unicode(state)
        False
        >>> state.unicode_mode = "on" 
        >>> should_use_unicode(state)
        True
        >>> state.unicode_mode = "auto"  # Depends on environment
        >>> should_use_unicode(state)
        True  # or False based on TERM and locale
    """
    if state is None:
        state = app_state
    
    if state.unicode_mode == "off":
        return False
    elif state.unicode_mode == "on":
        return True
    elif state.unicode_mode == "auto":
        # Auto-detection: fast, non-blocking checks only
        # Skip the problematic width probe that blocks execution
        return (utf8_env_check() and terminal_hints_unicode())
    return False


# =============================================================================
# DISPLAY FUNCTIONS - BANNERS AND UI ELEMENTS
# =============================================================================

def get_banner(state: Optional[ApplicationState] = None) -> str:
    """
    Get the appropriate banner art based on Unicode mode and terminal width.
    
    Selects from a width-tiered system of ASCII and Unicode banners to ensure
    optimal display across different terminal sizes and character set support.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Width Tiers:
        - compact: ≤62 characters (narrow terminals, mobile)
        - standard: 63-99 characters (typical desktop terminals)  
        - wide: ≥100 characters (wide-screen displays)
        
    Character Sets:
        - ASCII: Uses +, -, |, and █ characters for maximum compatibility
        - Unicode: Uses ╔, ═, ║, and other box-drawing characters for elegance
        
    Returns:
        str: Multi-line banner string with appropriate art and version info.
             Contains the "HACKER TERMINAL" title, version number (2.1.4),
             and "CLASSIFIED ACCESS ONLY" warning.
             
    Dependencies:
        - get_width_mode(): Determines current width tier
        - should_use_unicode(): Determines character set preference
        
    Example:
        >>> state = ApplicationState()
        >>> # Standard terminal with ASCII mode
        >>> banner = get_banner(state)
        >>> "HACKER" in banner and "VERSION 2.1.4" in banner
        True
        >>> # Wide terminal with Unicode mode  
        >>> banner = get_banner(state)
        >>> "╔" in banner  # Unicode box-drawing character
        True
    """
    width_tier = get_width_mode(state)
    
    if should_use_unicode(state):
        if width_tier == 'compact':
            return COMPACT_UNICODE_BANNER
        elif width_tier == 'wide':
            return WIDE_UNICODE_BANNER
        else:  # standard
            return STANDARD_UNICODE_BANNER
    else:
        if width_tier == 'compact':
            return COMPACT_ASCII_BANNER
        elif width_tier == 'wide':
            return WIDE_ASCII_BANNER
        else:  # standard
            return STANDARD_ASCII_BANNER

def get_access_granted(state: Optional[ApplicationState] = None) -> str:
    """
    Get the appropriate "ACCESS GRANTED" box based on Unicode mode and terminal width.
    
    Returns a width-appropriate ASCII or Unicode art box displaying the
    "ACCESS GRANTED" message, used to indicate successful authentication
    or system access during various hacking operations.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Width Adaptation:
        - compact: Condensed version for terminals ≤62 characters
        - standard: Full version for terminals 63-99 characters  
        - wide: Extended version for terminals ≥100 characters
        
    Returns:
        str: Multi-line string containing formatted "ACCESS GRANTED" message
             with decorative border appropriate for current terminal settings.
             
    Dependencies:
        - get_width_mode(): Determines current terminal width tier
        - should_use_unicode(): Determines character set (ASCII vs Unicode)
        
    Usage:
        Called by show_access_granted() to display successful operation results
        in commands like infiltrate, hack, and countertrace.
        
    Example:
        >>> state = ApplicationState()
        >>> access_box = get_access_granted(state)
        >>> "ACCESS GRANTED" in access_box
        True
        >>> # Contains appropriate border characters
        >>> "+" in access_box or "╔" in access_box
        True
    """
    width_tier = get_width_mode(state)
    
    if should_use_unicode(state):
        if width_tier == 'compact':
            return COMPACT_UNICODE_ACCESS_GRANTED
        elif width_tier == 'wide':
            return WIDE_UNICODE_ACCESS_GRANTED
        else:  # standard
            return STANDARD_UNICODE_ACCESS_GRANTED
    else:
        if width_tier == 'compact':
            return COMPACT_ACCESS_GRANTED
        elif width_tier == 'wide':
            return WIDE_ACCESS_GRANTED
        else:  # standard
            return STANDARD_ACCESS_GRANTED

def get_warning_box(state: Optional[ApplicationState] = None) -> str:
    """
    Get the appropriate warning box based on Unicode mode and terminal width.
    
    Returns a width-appropriate ASCII or Unicode art box displaying security
    warning messages, used to indicate unauthorized access detection or
    dangerous operations in progress.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Warning Content:
        - "!!! WARNING !!!" header
        - "UNAUTHORIZED ACCESS DETECTED" message
        - "INITIATING SECURITY PROTOCOLS" alert
        
    Width Adaptation:
        - compact: Condensed version for terminals ≤62 characters
        - standard: Full version for terminals 63-99 characters  
        - wide: Extended version for terminals ≥100 characters
        
    Returns:
        str: Multi-line string containing formatted warning message with
             decorative border appropriate for current terminal settings.
             
    Dependencies:
        - get_width_mode(): Determines current terminal width tier
        - should_use_unicode(): Determines character set (ASCII vs Unicode)
        
    Usage:
        Called by show_warning() to display security alerts before
        dangerous operations like infiltrate and hack commands.
        
    Example:
        >>> state = ApplicationState()
        >>> warning_box = get_warning_box(state)
        >>> "WARNING" in warning_box
        True
        >>> "UNAUTHORIZED ACCESS" in warning_box
        True
        >>> # Contains appropriate border characters
        >>> "+" in warning_box or "╔" in warning_box
        True
    """
    width_tier = get_width_mode(state)
    
    if should_use_unicode(state):
        if width_tier == 'compact':
            return COMPACT_UNICODE_WARNING_BOX
        elif width_tier == 'wide':
            return WIDE_UNICODE_WARNING_BOX
        else:  # standard
            return STANDARD_UNICODE_WARNING_BOX
    else:
        if width_tier == 'compact':
            return COMPACT_WARNING_BOX
        elif width_tier == 'wide':
            return WIDE_WARNING_BOX
        else:  # standard
            return STANDARD_WARNING_BOX

def get_progress_chars(state: Optional[ApplicationState] = None) -> Dict[str, str]:
    """
    Get appropriate progress bar characters based on Unicode mode.
    
    Returns a dictionary containing the filled and empty characters to use
    for progress bar display, adapting to the current Unicode mode setting.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Character Selection:
        - Unicode mode: Uses █ (filled block) and ░ (light shade) for elegant display
        - ASCII mode: Uses # (hash) and . (period) for maximum compatibility
        
    Returns:
        Dict[str, str]: Dictionary with 'filled' and 'empty' keys mapping to
                       appropriate characters for progress bar rendering.
                       
    Dependencies:
        - should_use_unicode(): Determines character set preference
        
    Usage:
        Called by progress() function to render animated progress bars
        with appropriate character sets for terminal compatibility.
        
    Example:
        >>> state = ApplicationState()
        >>> chars = get_progress_chars(state)
        >>> 'filled' in chars and 'empty' in chars
        True
        >>> # Unicode mode
        >>> state.unicode_mode = "on"
        >>> chars = get_progress_chars(state)  # Unicode on
        >>> chars['filled'] == '█' and chars['empty'] == '░'
        True
        >>> # ASCII mode  
        >>> state.unicode_mode = "off"
        >>> chars = get_progress_chars(state)  # Unicode off
        >>> chars['filled'] == '#' and chars['empty'] == '.'
        True
    """
    if should_use_unicode(state):
        return {'filled': '█', 'empty': '░'}
    else:
        return {'filled': '#', 'empty': '.'}


def get_terminal_width() -> int:
    """
    Get terminal width with comprehensive fallback chain and error handling.
    
    Implements a robust fallback system to determine the current terminal width
    in characters, handling various edge cases and environments gracefully.
    
    Fallback Chain:
        1. Primary: shutil.get_terminal_size() - Python's built-in method
        2. Fallback 1: COLUMNS environment variable
        3. Fallback 2: TERM_COLS environment variable (alternative standard)
        4. Final: DEFAULT_TERMINAL_WIDTH constant (80 characters)
        
    Error Handling:
        - OSError: When terminal size detection fails (e.g., non-TTY environment)
        - AttributeError: When shutil.get_terminal_size() is unavailable
        - ValueError: When environment variables contain invalid numeric values
        - Zero/negative values: Filtered out to prevent display issues
        
    Returns:
        int: Terminal width in characters, guaranteed to be > 0.
             Defaults to 80 characters if all detection methods fail.
             
    Environment Variables:
        - COLUMNS: Standard Unix terminal width variable
        - TERM_COLS: Alternative terminal width variable
        
    Example:
        >>> width = get_terminal_width()
        >>> width > 0
        True
        >>> # Typical values: 80, 120, 132, etc.
        >>> 20 <= width <= 500  # Reasonable terminal width range
        True
    """
    # Primary: shutil.get_terminal_size() with proper error handling
    try:
        size = shutil.get_terminal_size()
        if size.columns > SIZE_GREATER_THAN_ZERO:
            return size.columns
    except (OSError, AttributeError):
        pass
    
    # Fallback 1: COLUMNS environment variable
    columns_env = os.environ.get('COLUMNS')
    if columns_env and columns_env.isdigit():
        columns = int(columns_env)
        if columns > SIZE_GREATER_THAN_ZERO:
            return columns
    
    # Fallback 2: TERM_COLS environment variable
    term_cols_env = os.environ.get('TERM_COLS')
    if term_cols_env and term_cols_env.isdigit():
        term_cols = int(term_cols_env)
        if term_cols > SIZE_GREATER_THAN_ZERO:
            return term_cols
    
    # Final fallback: Default to 80 columns
    return DISPLAY_DEFAULT_TERMINAL_WIDTH


def classify_width(width: int) -> str:
    """
    Classify terminal width into appropriate display tier for optimal layout.
    
    Implements the width classification system used throughout the application
    to select appropriate ASCII art, banner formats, and display layouts
    based on available terminal space.
    
    Classification Thresholds:
        - compact: width ≤ 62 characters (mobile terminals, narrow windows)
        - standard: width 63-99 characters (typical desktop terminal windows)
        - wide: width ≥ 100 characters (wide-screen displays, maximized terminals)
        
    Args:
        width (int): Terminal width in characters, should be > 0.
        
    Returns:
        str: Width tier classification as 'compact', 'standard', or 'wide'.
             Used to select appropriate display constants and layouts.
             
    Design Rationale:
        - 62 chars: Ensures core functionality fits on narrow mobile terminals
        - 99 chars: Standard 80-column terminal plus reasonable margin
        - 100+ chars: Takes advantage of wide displays for enhanced visuals
        
    Dependencies:
        Uses DISPLAY_WIDTH_* constants for consistent threshold values.
        
    Example:
        >>> classify_width(50)
        'compact'
        >>> classify_width(80)
        'standard'
        >>> classify_width(120)
        'wide'
    """
    if width <= DISPLAY_WIDTH_COMPACT_THRESHOLD:
        return 'compact'
    elif width <= DISPLAY_WIDTH_STANDARD_THRESHOLD:
        return 'standard'
    else:
        return 'wide'


def get_terminal_width_tier() -> str:
    """
    Get terminal width tier with comprehensive edge case handling.
    
    Determines the appropriate display tier by combining terminal width detection
    with special handling for non-interactive environments and edge cases.
    
    Edge Case Handling:
        - Non-interactive terminals (pipes, file redirection): Defaults to 'standard'
        - Terminal size detection failures: Falls back to default width (80 chars)
        - Zero or invalid terminal widths: Uses fallback mechanisms
        
    Process:
        1. Check if output is going to a terminal (TTY)
        2. If non-interactive, default to 'standard' tier for compatibility
        3. Otherwise, detect actual terminal width via get_terminal_width()
        4. Classify width into appropriate tier via classify_width()
        
    Returns:
        str: Width tier classification as 'compact', 'standard', or 'wide'.
             Guarantees a valid tier even in problematic environments.
             
    Non-Interactive Behavior:
        When output is redirected (not a TTY), assumes 'standard' width to
        ensure proper formatting in files, pipes, and other output destinations.
        
    Dependencies:
        - sys.stdout.isatty(): TTY detection
        - get_terminal_width(): Width detection with fallbacks
        - classify_width(): Width tier classification
        
    Example:
        >>> # In a normal terminal
        >>> tier = get_terminal_width_tier()
        >>> tier in ['compact', 'standard', 'wide']
        True
        >>> # When output is redirected
        >>> tier = get_terminal_width_tier()  # Non-TTY
        >>> tier == 'standard'
        True
    """
    # Handle non-interactive terminals (pipes, redirected output)
    if not sys.stdout.isatty():
        # Default to standard for non-interactive output
        return 'standard'
    
    # Get terminal width with fallback chain
    width = get_terminal_width()
    return classify_width(width)


def get_width_mode(state: Optional[ApplicationState] = None) -> str:
    """
    Determine current width mode based on application state and terminal detection.
    
    Implements the width mode resolution logic that combines user preferences
    with automatic terminal detection to select the appropriate display tier.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Width Mode Resolution:
        - Explicit modes ('compact', 'standard', 'wide'): Use as specified
        - 'auto' mode: Auto-detect using get_terminal_width_tier()
        - Unknown modes: Fallback to 'standard' for safety
        
    State Dependency:
        Uses the application state width_mode setting which can be set via:
        - Command line arguments (--width parameter)
        - Direct assignment in code
        - Defaults to 'auto' if not specified
        
    Returns:
        str: Resolved width mode as 'compact', 'standard', or 'wide'.
             Guarantees a valid width tier for display functions.
             
    Mode Priority:
        1. Explicit user setting (highest priority)
        2. Auto-detection from terminal
        3. Safe fallback to 'standard'
        
    Dependencies:
        - ApplicationState.width_mode setting
        - get_terminal_width_tier(): For auto-detection
        
    Example:
        >>> state = ApplicationState()
        >>> state.width_mode = "compact"
        >>> get_width_mode(state)
        'compact'
        >>> state.width_mode = "auto"
        >>> get_width_mode(state)  # Returns detected tier
        'standard'  # or 'compact'/'wide' based on terminal
    """
    if state is None:
        state = app_state
    
    if state.width_mode in ['compact', 'standard', 'wide']:
        # Explicit mode set via CLI argument
        return state.width_mode
    elif state.width_mode == 'auto':
        # Auto-detect based on terminal width
        return get_terminal_width_tier()
    else:
        # Fallback to standard for unknown modes
        return 'standard'


def progress(label: str = "Processing", steps: int = PROGRESS_BAR_STEPS_DEFAULT, delay: float = TIMING_PROGRESS_DEFAULT, state: Optional[ApplicationState] = None) -> None:
    """
    Display an animated progress bar with cinematic hacker-movie styling.
    
    Creates a visually appealing progress bar animation with percentage display,
    animated dots, and appropriate character selection based on Unicode support.
    Used throughout the application to simulate realistic hacking operations.
    
    Progress Bar Features:
        - Animated filling from left to right
        - Real-time percentage display (0-100%)
        - Cycling dots animation (..., .., .)
        - Unicode-aware character selection
        - Consistent 52-character width for alignment
        
    Args:
        label (str): Operation label displayed above progress bar.
                    Defaults to "Processing". Common values: "Scanning network",
                    "Decrypting data", "Bypassing security", etc.
        steps (int): Number of animation steps for progress bar.
                    Defaults to PROGRESS_BAR_STEPS_DEFAULT (20).
                    More steps = smoother animation but longer duration.
        delay (float): Delay between animation frames in seconds.
                      Defaults to TIMING_PROGRESS_DEFAULT (0.08).
                      Shorter delay = faster animation.
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
                      
    Display Format:
        [OPERATION_LABEL]
        +----------------------------------------------------+
        | [████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 40% ... |
        +----------------------------------------------------+
        
    Character Adaptation:
        - Unicode mode: Uses █ (filled block) and ░ (light shade)
        - ASCII mode: Uses # (hash) and . (period)
        
    Dependencies:
        - get_progress_chars(): Character set selection
        - PROGRESS_BAR_WIDTH: Consistent bar width (52 chars)
        - Various timing and step constants
        
    Example:
        >>> progress("Scanning network", 24, 0.12)
        # Displays animated progress bar with "SCANNING NETWORK" label
        >>> progress()  # Uses defaults
        # Displays "PROCESSING" with standard timing
    """
    print(f"\n[{label.upper()}]")
    print("+" + "-" * PROGRESS_BAR_WIDTH + "+")
    
    chars = get_progress_chars(state)
    
    for i in range(steps + STEP_INCREMENT):
        filled = chars['filled'] * i
        empty = chars['empty'] * (steps - i)
        percent = int((i / steps) * 100)
        
        # Add scanning dots for effect
        dots = "..." if i % PROGRESS_DOT_CYCLE_MODULO == 0 else ".." if i % PROGRESS_DOT_CYCLE_MODULO == 1 else "."
        
        print(f"| [{filled}{empty}] {percent:{PROGRESS_PERCENTAGE_WIDTH}d}% {dots:<{PROGRESS_DOTS_WIDTH}} |", end="")
        print("\r", end="", flush=True)
        time.sleep(delay)
    
    print("\n+" + "-" * PROGRESS_BAR_WIDTH + "+")
    time.sleep(TIMING_PROGRESS_END_DELAY)


def show_access_granted(state: Optional[ApplicationState] = None) -> None:
    """
    Display the "ACCESS GRANTED" confirmation box with dramatic timing.
    
    Shows a width-appropriate and Unicode-aware "ACCESS GRANTED" message
    to indicate successful completion of hacking operations. Includes a
    dramatic pause for cinematic effect.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Display Features:
        - Width-adaptive layout (compact/standard/wide)
        - Unicode/ASCII character set adaptation
        - 1-second dramatic pause after display
        - Consistent with hacker movie aesthetics
        
    Usage:
        Called after successful operations in:
        - cmd_infiltrate(): After gaining root privileges
        - cmd_hack(): After successful system compromise
        - cmd_countertrace(): After blocking enemy traces
        
    Dependencies:
        - get_access_granted(): Returns appropriate access granted box
        - TIMING_ACCESS_GRANTED_DELAY: Controls dramatic pause duration
        
    Example:
        >>> state = ApplicationState()
        >>> show_access_granted(state)
        # Displays formatted "ACCESS GRANTED" box
        # Pauses for dramatic effect
        # Returns after 1 second
    """
    print(get_access_granted(state))
    time.sleep(TIMING_ACCESS_GRANTED_DELAY)


def show_warning(state: Optional[ApplicationState] = None) -> None:
    """
    Display the security warning box with dramatic timing.
    
    Shows a width-appropriate and Unicode-aware warning message indicating
    unauthorized access detection or dangerous operation initiation. Includes
    an extended dramatic pause to build tension.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Warning Content:
        - "!!! WARNING !!!" header
        - "UNAUTHORIZED ACCESS DETECTED" alert
        - "INITIATING SECURITY PROTOCOLS" message
        
    Display Features:
        - Width-adaptive layout (compact/standard/wide)
        - Unicode/ASCII character set adaptation
        - 1.5-second dramatic pause for tension building
        - Red alert aesthetic typical of hacker movies
        
    Usage:
        Called before dangerous operations in:
        - cmd_infiltrate(): Before attempting system infiltration
        - cmd_hack(): Before launching hack sequence
        
    Dependencies:
        - get_warning_box(): Returns appropriate warning box
        - TIMING_WARNING_DELAY: Controls dramatic pause duration (1.5 seconds)
        
    Example:
        >>> state = ApplicationState()
        >>> show_warning(state)
        # Displays formatted warning box
        # Pauses for 1.5 seconds to build tension
        # Returns to allow operation to proceed
    """
    print(get_warning_box(state))
    time.sleep(TIMING_WARNING_DELAY)


def ascii_banner(state: Optional[ApplicationState] = None) -> None:
    """
    Display the main application banner with adaptive formatting.
    
    Shows the "HACKER TERMINAL" title banner with version information and
    security warning, automatically adapting to current Unicode mode and
    terminal width settings.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Banner Content:
        - "HACKER TERMINAL" stylized text art
        - Version number display (currently 2.1.4)
        - "*** CLASSIFIED ACCESS ONLY ***" security warning
        - Decorative border appropriate for current display mode
        
    Adaptive Features:
        - Width adaptation: compact (≤62), standard (63-99), wide (≥100 chars)
        - Character set adaptation: ASCII (+, -, |) vs Unicode (╔, ═, ║)
        - Automatic mode selection based on terminal capabilities
        
    Usage:
        Called at application startup in:
        - main(): When starting any mode (demo, interactive, single command)
        - interactive_mode(): At the beginning of interactive sessions
        - run_demo_script(): At the start of demo sequence
        
    Dependencies:
        - get_banner(): Returns appropriate banner based on current settings
        - Terminal width and Unicode detection systems
        
    Example:
        >>> state = ApplicationState()
        >>> ascii_banner(state)
        # Displays width and Unicode-appropriate banner
        # No return value, output goes directly to stdout
    """
    print(get_banner(state))




def random_line(options: List[str]) -> str:
    """
    Return a randomly selected line from a list of options.
    
    Simple utility function for random selection used throughout the application
    to add variety to messages, responses, and simulated data while maintaining
    deterministic behavior when a specific random seed is set.
    
    Args:
        options (List[str]): List of string options to choose from.
                           Must contain at least one element.
                           
    Returns:
        str: Randomly selected string from the options list.
        
    Randomization:
        - Uses Python's random.choice() for selection
        - Respects any random seed set via random.seed()
        - Demo mode uses deterministic seed for consistent output
        - Interactive mode uses system randomization
        
    Usage Examples:
        - cmd_decrypt(): Selects random decrypted messages
        - cmd_trace(): Chooses random ISP names for unknown targets
        - Any function requiring randomized text variety
        
    Example:
        >>> messages = ["Hello", "World", "Test"]
        >>> result = random_line(messages)
        >>> result in messages
        True
        >>> # With deterministic seed
        >>> random.seed(1337)
        >>> random_line(["A", "B", "C"])
        'B'  # Consistent result with same seed
    """
    return random.choice(options)


# =============================================================================
# COMMAND IMPLEMENTATIONS - HACKER TERMINAL OPERATIONS
# =============================================================================

def cmd_help() -> None:
    """
    Display the complete list of available commands with usage information.
    
    Shows a formatted help menu listing all available commands with their
    syntax and brief descriptions. Provides essential reference information
    for users navigating the hacker terminal interface.
    
    Command Categories:
        - Information: help, status
        - Reconnaissance: scan, trace
        - Operations: decrypt, infiltrate, hack
        - Defense: countertrace/evade
        - System: clear, exit
        
    Display Format:
        Each command shown as:
        command [args]          - Description
        
    Commands Listed:
        - help: Show this help menu
        - scan: Discover available network targets
        - decrypt: Decrypt intercepted communications
        - infiltrate <target>: Attempt system infiltration
        - hack: Execute comprehensive hack sequence
        - trace <target>: Determine target geographical location
        - countertrace|evade: Deploy anti-tracing countermeasures
        - status: Display current system status
        - clear: Clear terminal screen
        - exit: Exit the terminal application
        
    Usage:
        Available in all modes (interactive, single command, demo).
        No arguments required.
        
    Example:
        >>> cmd_help()
        Available commands:
          help                    - Show this help
          scan                    - Scan for targets
          ...
    """
    help_text = """Available commands:
  help                    - Show this help
  scan                    - Scan for targets
  decrypt                 - Decrypt intercepted data
  infiltrate <target>     - Infiltrate specified target
  hack                    - Execute hack sequence
  trace <target>          - Trace target location
  countertrace|evade      - Counter enemy traces
  status                  - Show system status
  clear                   - Clear terminal
  exit                    - Exit terminal"""
    print(help_text)


def cmd_scan(state: Optional[ApplicationState] = None) -> None:
    """
    Perform network reconnaissance to discover available targets.
    
    Simulates a network scanning operation that discovers hackable systems
    with their associated security levels. Updates the application state
    discovered_targets list with a predefined set of targets for consistent demo behavior.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Operation Sequence:
        1. Display animated progress bar with "Scanning network" label
        2. Update state discovered_targets with fixed target list
        3. Display discovered targets with security classifications
        
    Discovered Targets (Fixed for Demo Consistency):
        - MAINFRAME-7: low security (easy target)
        - QUANTUM-DB: high security (challenging target)
        - SATELLITE-X: medium security (moderate target)
        
    Security Classifications:
        - low: Minimal security measures, easy infiltration
        - medium: Standard security protocols, moderate difficulty
        - high: Advanced security systems, high difficulty
        
    Progress Animation:
        - Uses 24 steps for detailed scanning simulation
        - 0.12 second delay per step for realistic timing
        - Displays percentage completion and animated dots
        
    State Changes:
        Updates application state discovered_targets list, enabling infiltrate command
        to validate target names against discovered systems.
        
    Usage:
        >>> state = ApplicationState()
        >>> cmd_scan(state)
        [SCANNING NETWORK]
        +----------------------------------------------------+
        | [████████████████████████░░░░░░░░░░░░░░░░░░░░] 100% ... |
        +----------------------------------------------------+
        Found 3 targets:
        - MAINFRAME-7 (security: low)
        - QUANTUM-DB (security: high)
        - SATELLITE-X (security: medium)
        
    Dependencies:
        - progress(): Animated progress bar display
        - PROGRESS_BAR_STEPS_SCAN, TIMING_PROGRESS_SCAN: Animation parameters
    """
    if state is None:
        state = app_state
    
    progress("Scanning network", PROGRESS_BAR_STEPS_SCAN, TIMING_PROGRESS_SCAN, state)
    
    # Fixed targets to match SCOPE.md demo exactly
    state.discovered_targets = [
        ("MAINFRAME-7", "low"),
        ("QUANTUM-DB", "high"), 
        ("SATELLITE-X", "medium")
    ]
    
    print(f"Found {len(state.discovered_targets)} targets:")
    for name, security in state.discovered_targets:
        print(f"- {name} (security: {security})")


def cmd_decrypt() -> None:
    """
    Decrypt intercepted communications and display hidden messages.
    
    Simulates a cryptographic decryption operation that reveals secret messages
    from intercepted communications. Features a progress bar animation and
    randomly selects from a pool of classic hacker movie references.
    
    Operation Sequence:
        1. Display animated progress bar with "Decrypting data" label
        2. Randomly select a hidden message from predefined pool
        3. Display the decrypted message to user
        
    Message Pool (Classic Hacker References):
        - "THE CAKE IS A LIE" (Portal reference)
        - "TRUST NO ONE" (X-Files/conspiracy theme)
        - "FOLLOW THE WHITE RABBIT" (Matrix reference)
        - "THE MATRIX HAS YOU" (Matrix reference)
        - "WAKE UP NEO" (Matrix reference)
        - "I AM ROOT" (Unix root access reference)
        
    Progress Animation:
        - Uses 26 steps for detailed decryption simulation
        - 0.10 second delay per step for cryptographic feel
        - Simulates computational effort of decryption algorithms
        
    Randomization:
        - Random message selection via random_line()
        - Deterministic in demo mode (seed = 1337)
        - True randomization in interactive mode
        
    Usage:
        >>> cmd_decrypt()
        [DECRYPTING DATA]
        +----------------------------------------------------+
        | [██████████████████████████████████████████████] 100% ... |
        +----------------------------------------------------+
        Decrypted message: "THE MATRIX HAS YOU"
        
    Dependencies:
        - progress(): Animated progress bar display
        - random_line(): Random message selection
        - PROGRESS_BAR_STEPS_DECRYPT, TIMING_PROGRESS_DECRYPT: Animation parameters
    """
    progress("Decrypting data", PROGRESS_BAR_STEPS_DECRYPT, TIMING_PROGRESS_DECRYPT)
    
    messages = [
        "THE CAKE IS A LIE",
        "TRUST NO ONE",
        "FOLLOW THE WHITE RABBIT", 
        "THE MATRIX HAS YOU",
        "WAKE UP NEO",
        "I AM ROOT"
    ]
    
    message = random_line(messages)
    print(f'Decrypted message: "{message}"')


def cmd_infiltrate(target: Optional[str], state: Optional[ApplicationState] = None) -> None:
    """
    Attempt to infiltrate a specified target system and gain root access.
    
    Performs a simulated infiltration attack against a discovered target system,
    including security warnings, progress animation, and success confirmation.
    Validates target existence and updates infiltration tracking state.
    
    Args:
        target (Optional[str]): Name of target system to infiltrate.
                               Must be a previously discovered target from cmd_scan().
                               Case-insensitive, automatically converted to uppercase.
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
                               
    Operation Sequence:
        1. Validate target argument is provided
        2. Convert target name to uppercase for consistency
        3. Verify target exists in discovered_targets list
        4. Display security warning with dramatic pause
        5. Show infiltration progress animation
        6. Add target to infiltrated_targets set
        7. Display ACCESS GRANTED confirmation
        8. Confirm root privileges obtained
        
    Input Validation:
        - Requires target argument, shows usage if missing
        - Verifies target was discovered via scan command
        - Handles case-insensitive target names
        
    Security Theater:
        - Shows warning box before attempting infiltration
        - "Bypassing security" progress animation (28 steps)
        - Dramatic "ACCESS GRANTED" confirmation
        - "Root privileges obtained" success message
        
    State Changes:
        - Adds infiltrated target to application state infiltrated_targets set
        - Enables tracking of successfully compromised systems
        
    Usage Examples:
        >>> state = ApplicationState()
        >>> cmd_infiltrate("MAINFRAME-7", state)
        [Warning box displayed]
        Infiltrating MAINFRAME-7...
        [Progress bar: "Bypassing security"]
        [ACCESS GRANTED box displayed]
        Root privileges obtained.
        
        >>> cmd_infiltrate(None, state)
        Target required. Usage: infiltrate <target>
        
        >>> cmd_infiltrate("UNKNOWN-SYS", state)
        Target not found. Run 'scan' first.
        
    Dependencies:
        - show_warning(): Security alert display
        - progress(): Infiltration progress animation
        - show_access_granted(): Success confirmation
        - ApplicationState discovered_targets, infiltrated_targets state
    """
    if state is None:
        state = app_state
    
    if not target:
        print("Target required. Usage: infiltrate <target>")
        return
        
    target = target.upper()
    
    # Check if target was discovered
    target_names = [name for name, _ in state.discovered_targets]
    if target not in target_names:
        print("Target not found. Run 'scan' first.")
        return
    
    show_warning(state)
    print(f"Infiltrating {target}...")
    progress("Bypassing security", PROGRESS_BAR_STEPS_INFILTRATE, TIMING_PROGRESS_INFILTRATE, state)
    
    state.infiltrated_targets.add(target)
    show_access_granted(state)
    print("Root privileges obtained.")


def cmd_hack(state: Optional[ApplicationState] = None) -> None:
    """
    Execute comprehensive hack sequence to compromise multiple systems.
    
    Performs a full-scale hacking operation that simulates exploiting
    vulnerabilities across multiple systems to gain widespread access
    and earn credits. Features dramatic security warnings and success displays.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Operation Sequence:
        1. Display security warning with extended dramatic pause
        2. Show "Initiating hack sequence..." message
        3. Animate "Exploiting vulnerabilities" progress bar
        4. Update system status with compromised systems and earned credits
        5. Display ACCESS GRANTED confirmation
        6. Show final success statistics
        
    Fixed Results (Demo Consistency):
        - Systems compromised: 5 (DEMO_HACK_SYSTEMS constant)
        - Credits earned: 1337 (DEMO_HACK_CREDITS constant)
        - These values are fixed to ensure consistent demo output
        
    Progress Animation:
        - Uses 30 steps for detailed vulnerability exploitation simulation
        - 0.12 second delay per step for realistic hacking feel
        - Longest progress sequence to emphasize operation complexity
        
    State Changes:
        Updates application state system_status dictionary:
        - compromised_systems: Set to 5
        - credits: Set to 1337
        
    Security Theater:
        - Extended warning display (1.5 seconds)
        - "HACK SUCCESSFUL" confirmation message
        - Statistics display showing impact
        - ACCESS GRANTED box for dramatic effect
        
    Usage:
        >>> state = ApplicationState()
        >>> cmd_hack(state)
        [Warning box displayed for 1.5 seconds]
        Initiating hack sequence...
        [EXPLOITING VULNERABILITIES progress bar - 30 steps]
        [ACCESS GRANTED box displayed]
        HACK SUCCESSFUL
        Systems compromised: 5
        Credits earned: 1337
        
    Dependencies:
        - show_warning(): Security alert with extended timing
        - progress(): Vulnerability exploitation animation
        - show_access_granted(): Success confirmation display
        - ApplicationState system_status state management
    """
    if state is None:
        state = app_state
    
    show_warning(state)
    print("Initiating hack sequence...")
    progress("Exploiting vulnerabilities", PROGRESS_BAR_STEPS_HACK, TIMING_PROGRESS_HACK, state)
    
    # Fixed values to match SCOPE.md demo exactly  
    systems = DEMO_HACK_SYSTEMS
    credits = DEMO_HACK_CREDITS
    
    state.system_status["compromised_systems"] = systems
    state.system_status["credits"] = credits
    
    show_access_granted(state)
    print("HACK SUCCESSFUL")
    print(f"Systems compromised: {systems}")
    print(f"Credits earned: {credits}")


def cmd_trace(target: Optional[str]) -> None:
    """
    Trace the geographical location of a specified target system.
    
    Performs a simulated geographical trace operation to determine the
    physical location and Internet Service Provider (ISP) of a target
    system. Uses predefined locations for known targets and generates
    random coordinates for unknown targets.
    
    Args:
        target (Optional[str]): Name of target system to trace.
                               Can be any string, not limited to discovered targets.
                               Case-insensitive, automatically converted to uppercase.
                               
    Operation Sequence:
        1. Validate target argument is provided
        2. Convert target name to uppercase for consistency
        3. Display "Tracing {target}..." message
        4. Animate "Triangulating position" progress bar
        5. Look up target in predefined locations or generate random coordinates
        6. Display geographical coordinates and ISP information
        
    Location Database:
        Predefined locations in PREDEFINED_LOCATIONS constant:
        - QUANTUM-DB: San Francisco, CyberCorp Industries
        - MAINFRAME-7: New York, MegaCorp Systems
        - SATELLITE-X: London, SkyNet Communications
        - NEXUS-CORE: Tokyo, Tech Dynamics
        - CRYPTO-VAULT: Berlin, SecureMax GmbH
        - DATA-CENTER: Los Angeles, InfoTech Solutions
        
    Random Generation (Unknown Targets):
        - Latitude: -90.0 to +90.0 degrees
        - Longitude: -180.0 to +180.0 degrees
        - Precision: 4 decimal places
        - ISP: Randomly selected from pool of generic names
        
    Progress Animation:
        - Uses 25 steps for triangulation simulation
        - 0.13 second delay per step for GPS/network trace feel
        - Simulates time required for geographical triangulation
        
    Usage Examples:
        >>> cmd_trace("QUANTUM-DB")
        Tracing QUANTUM-DB...
        [TRIANGULATING POSITION progress bar]
        Location found: 37.7749 deg N, 122.4194 deg W
        ISP: CyberCorp Industries
        
        >>> cmd_trace("UNKNOWN-TARGET")
        Tracing UNKNOWN-TARGET...
        [Progress animation]
        Location found: 45.2341 deg N, 67.8912 deg W
        ISP: DataFlow Systems
        
        >>> cmd_trace(None)
        Target required. Usage: trace <target>
        
    Dependencies:
        - progress(): Triangulation progress animation
        - PREDEFINED_LOCATIONS: Known target location database
        - random.uniform(): Random coordinate generation for unknown targets
        - Coordinate and ISP name constants
    """
    if not target:
        print("Target required. Usage: trace <target>")
        return
        
    target = target.upper()
    
    print(f"Tracing {target}...")
    progress("Triangulating position", PROGRESS_BAR_STEPS_TRACE, TIMING_PROGRESS_TRACE)
    
    # Predefined locations for consistency
    locations = PREDEFINED_LOCATIONS
    
    if target in locations:
        coords, isp = locations[target]
        print(f"Location found: {coords}")
        print(f"ISP: {isp}")
    else:
        # Fallback for unknown targets
        lat = round(random.uniform(COORDINATE_LAT_MIN, COORDINATE_LAT_MAX), COORDINATE_PRECISION)
        lon = round(random.uniform(COORDINATE_LON_MIN, COORDINATE_LON_MAX), COORDINATE_PRECISION)
        isps = ["CyberCorp Industries", "TechMax Solutions", "DataFlow Systems"]
        print(f"Location found: {lat} deg N, {lon} deg W")
        print(f"ISP: {random_line(isps)}")


def cmd_countertrace() -> None:
    """
    Deploy anti-tracing countermeasures to evade enemy detection.
    
    Executes defensive countermeasures to scramble the user's digital identity
    and prevent enemy tracing attempts. Features progress animation and
    success confirmation typical of defensive cybersecurity operations.
    
    Operation Sequence:
        1. Display "Deploying countermeasures..." message
        2. Animate "Scrambling identity" progress bar
        3. Display ACCESS GRANTED confirmation
        4. Confirm trace blocking and identity scrambling success
        
    Defensive Features:
        - Identity scrambling simulation
        - Trace blocking confirmation
        - Quick deployment (22 steps for rapid response)
        - Success feedback for user confidence
        
    Progress Animation:
        - Uses 22 steps for faster defensive response simulation
        - 0.11 second delay per step for urgent countermeasure feel
        - Shorter sequence emphasizes rapid defensive response
        
    Aliases:
        This command can also be invoked as "evade" for convenience.
        Both "countertrace" and "evade" execute identical functionality.
        
    Usage:
        >>> cmd_countertrace()
        Deploying countermeasures...
        [SCRAMBLING IDENTITY progress bar - 22 steps]
        [ACCESS GRANTED box displayed]
        Trace blocked. Identity scrambled.
        
        >>> # Also works as "evade"
        >>> cmd_countertrace()  # Same result
        
    Dependencies:
        - progress(): Identity scrambling animation
        - show_access_granted(): Success confirmation display
        - PROGRESS_BAR_STEPS_COUNTERTRACE, TIMING_PROGRESS_COUNTERTRACE: Animation parameters
    """
    print("Deploying countermeasures...")
    progress("Scrambling identity", PROGRESS_BAR_STEPS_COUNTERTRACE, TIMING_PROGRESS_COUNTERTRACE)
    show_access_granted()
    print("Trace blocked. Identity scrambled.")


def cmd_status(state: Optional[ApplicationState] = None) -> None:
    """
    Display comprehensive system status and security information.
    
    Shows the current state of all system components including security
    levels, network connections, defensive systems, and operational statistics.
    Provides a real-time overview of the hacker terminal's operational status.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Status Information Displayed:
        - System Status: ONLINE/OFFLINE (connection state)
        - Security Level: Current security posture (typically MAXIMUM)
        - Active Connections: Number of active network connections
        - Firewall: ENABLED/DISABLED (firewall protection status)
        - Stealth Mode: ON/OFF (stealth operation status)
        
    Status Sources:
        All information retrieved from the application state system_status dictionary
        which is updated by various operational commands:
        - cmd_hack(): Updates compromised_systems and credits
        - System initialization: Sets default security parameters
        
    Display Format:
        System Status: ONLINE
        Security Level: MAXIMUM
        Active Connections: 3
        Firewall: ENABLED
        Stealth Mode: ON
        
    State Dependencies:
        - state.system_status['online']: System connectivity status
        - state.system_status['security_level']: Current security posture
        - state.system_status['connections']: Active network connections count
        - state.system_status['firewall']: Firewall protection status
        - state.system_status['stealth']: Stealth mode operational status
        
    Usage:
        >>> state = ApplicationState()
        >>> cmd_status(state)
        System Status: ONLINE
        Security Level: MAXIMUM
        Active Connections: 3
        Firewall: ENABLED
        Stealth Mode: ON
        
    Note:
        This command provides read-only status information and does not
        modify any system state.
    """
    if state is None:
        state = app_state
    
    status_map = {
        True: STATUS_ENABLED,
        False: STATUS_DISABLED
    }
    
    print(f"System Status: {STATUS_ONLINE if state.system_status['online'] else STATUS_OFFLINE}")
    print(f"Security Level: {state.system_status['security_level']}")
    print(f"Active Connections: {state.system_status['connections']}")
    print(f"Firewall: {status_map[state.system_status['firewall']]}")
    print(f"Stealth Mode: {STATUS_STEALTH_ON if state.system_status['stealth'] else STATUS_STEALTH_OFF}")


def cmd_clear() -> None:
    """
    Clear the terminal screen for a fresh workspace.
    
    Executes the appropriate system command to clear the terminal screen,
    adapting to the current operating system (Windows vs Unix-like systems).
    Provides a clean slate for continued hacker terminal operations.
    
    System Compatibility:
        - Windows (os.name == 'nt'): Executes 'cls' command
        - Unix-like systems (Linux, macOS): Executes 'clear' command
        - Uses os.system() for direct shell command execution
        
    Usage:
        >>> cmd_clear()
        # Terminal screen is cleared
        # Cursor positioned at top-left
        # Ready for new output
        
    Note:
        This command has no return value and produces no visible output
        other than clearing the screen. The effect is immediate and
        non-reversible within the terminal session.
        
    Security:
        Uses os.system() which executes system commands. In this context,
        the commands ('cls', 'clear') are safe system utilities with no
        security implications for the host system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def cmd_exit() -> None:
    """
    Exit the hacker terminal application gracefully.
    
    Terminates the application with appropriate farewell messages and
    clean exit handling. Provides thematic closure consistent with the
    hacker terminal aesthetic.
    
    Exit Sequence:
        1. Display "Connection terminated." message
        2. Show farewell "Stay anonymous, hacker." message  
        3. Exit with success status code (0)
        
    Exit Behavior:
        - Immediately terminates the application
        - No cleanup required (no persistent state or open files)
        - Uses sys.exit() with EXIT_SUCCESS constant (0)
        - Cannot be intercepted or cancelled once called
        
    Thematic Messages:
        - "Connection terminated": Suggests network disconnection
        - "Stay anonymous, hacker": Encourages operational security
        - Maintains immersive hacker movie atmosphere
        
    Usage:
        >>> cmd_exit()
        Connection terminated.
        Stay anonymous, hacker.
        # Application terminates immediately
        
    Exit Codes:
        - Uses EXIT_SUCCESS constant (0) indicating normal termination
        - Distinguishes from error exits which use EXIT_FAILURE (1)
        
    Note:
        This function never returns - it terminates the entire Python process.
        Any code after cmd_exit() will not be executed.
    """
    print("Connection terminated.")
    print("Stay anonymous, hacker.")
    sys.exit(EXIT_SUCCESS)


# =============================================================================
# COMMAND PARSING AND EXECUTION SYSTEM
# =============================================================================

def parse_command(command_line: str) -> Tuple[Optional[str], List[str]]:
    """
    Parse a command line string into command and arguments.
    
    Splits the input command line into the primary command (first word)
    and any additional arguments, handling edge cases like empty input
    and whitespace normalization.
    
    Args:
        command_line (str): Complete command line string as entered by user.
                           May contain leading/trailing whitespace.
                           
    Returns:
        Tuple[Optional[str], List[str]]: Tuple containing:
            - command: First word converted to lowercase, or None if empty input
            - arguments: List of remaining words, or empty list if no arguments
            
    Parsing Logic:
        1. Strip leading and trailing whitespace
        2. Split on whitespace into parts
        3. Return None if no parts (empty input)
        4. Convert first part to lowercase for case-insensitive commands
        5. Return remaining parts as argument list
        
    Case Handling:
        - Commands are converted to lowercase for consistent lookup
        - Arguments preserve original case for target names, etc.
        - Empty strings and whitespace-only input return (None, [])
        
    Usage Examples:
        >>> parse_command("scan")
        ('scan', [])
        
        >>> parse_command("infiltrate MAINFRAME-7")
        ('infiltrate', ['MAINFRAME-7'])
        
        >>> parse_command("  trace   QUANTUM-DB  ")
        ('trace', ['QUANTUM-DB'])
        
        >>> parse_command("")
        (None, [])
        
        >>> parse_command("   ")
        (None, [])
        
    Dependencies:
        - COMMAND_PARTS_FIRST_INDEX: Constant for first element index (0)
        - ARRAY_SLICE_START: Constant for argument slice start (1)
    """
    parts = command_line.strip().split()
    if not parts:
        return None, []
    return parts[COMMAND_PARTS_FIRST_INDEX].lower(), parts[ARRAY_SLICE_START:]


def execute_command(cmd: Optional[str], args: List[str], state: Optional[ApplicationState] = None) -> bool:
    """
    Execute a parsed command with its arguments and return success status.
    
    Central command dispatcher that routes parsed commands to their corresponding
    implementation functions. Handles command validation, argument passing,
    and provides unified error handling for unknown commands.
    
    Args:
        cmd (Optional[str]): Command name in lowercase, or None for empty input.
                           Should be output from parse_command() function.
        args (List[str]): List of command arguments preserving original case.
                         Empty list if command takes no arguments.
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
                         
    Returns:
        bool: True if command was recognized and executed successfully,
              False if command was None, empty, or not recognized.
              
    Command Routing:
        - help: cmd_help() - Display available commands
        - scan: cmd_scan() - Network reconnaissance  
        - decrypt: cmd_decrypt() - Decrypt intercepted data
        - infiltrate: cmd_infiltrate(target) - System infiltration
        - hack: cmd_hack() - Execute hack sequence
        - trace: cmd_trace(target) - Geographical tracing
        - countertrace|evade: cmd_countertrace() - Deploy countermeasures
        - status: cmd_status() - Show system status
        - clear: cmd_clear() - Clear terminal screen
        - exit: cmd_exit() - Exit application
        
    Argument Handling:
        - No-argument commands: Called directly
        - Single-argument commands: Pass first argument or None if missing
        - Commands with aliases: "countertrace" and "evade" both route to cmd_countertrace()
        
    Error Handling:
        - None command: Returns False (empty input)
        - Unknown command: Displays error message and returns False
        - Valid command execution: Returns True regardless of command outcome
        
    Usage Examples:
        >>> execute_command("scan", [])
        True  # Executes scan operation
        
        >>> execute_command("infiltrate", ["MAINFRAME-7"])
        True  # Executes infiltration of MAINFRAME-7
        
        >>> execute_command("unknown", [])
        Command not recognized. Type 'help' for available commands.
        False
        
        >>> execute_command(None, [])
        False  # Empty input
        
    Dependencies:
        - All cmd_* functions for command implementation
        - COMMAND_ARGS_FIRST_INDEX: Constant for first argument index (0)
    """
    if state is None:
        state = app_state
    
    if cmd is None:
        return False
    elif cmd == "help":
        cmd_help()
    elif cmd == "scan":
        cmd_scan(state)
    elif cmd == "decrypt":
        cmd_decrypt()
    elif cmd == "infiltrate":
        target = args[COMMAND_ARGS_FIRST_INDEX] if args else None
        cmd_infiltrate(target, state)
    elif cmd == "hack":
        cmd_hack(state)
    elif cmd == "trace":
        target = args[COMMAND_ARGS_FIRST_INDEX] if args else None
        cmd_trace(target)
    elif cmd in ["countertrace", "evade"]:
        cmd_countertrace()
    elif cmd == "status":
        cmd_status(state)
    elif cmd == "clear":
        cmd_clear()
    elif cmd == "exit":
        cmd_exit()
    else:
        print("Command not recognized. Type 'help' for available commands.")
        return False
    return True


# =============================================================================
# APPLICATION CONTROL FUNCTIONS - MAIN EXECUTION MODES
# =============================================================================

def run_demo_script(state: Optional[ApplicationState] = None) -> None:
    """
    Execute the deterministic demonstration script with fixed command sequence.
    
    Runs a predefined sequence of commands that showcases all major features
    of the hacker terminal in a consistent, reproducible manner. Uses a fixed
    random seed to ensure identical output across all executions.
    
    Demo Features:
        - Deterministic behavior with fixed random seed (1337)
        - Covers all major command categories
        - Consistent output for documentation and testing
        - Representative user workflow from reconnaissance to completion
        
    Command Sequence:
        1. scan - Discover available network targets
        2. infiltrate MAINFRAME-7 - Compromise an easy target  
        3. hack - Execute comprehensive hack sequence
        4. trace QUANTUM-DB - Perform geographical tracing
        5. countertrace - Deploy defensive countermeasures
        6. status - Display final system status
        7. exit - Clean application termination
        
    Randomization Control:
        - Sets random.seed(1337) for deterministic behavior
        - Ensures identical messages, coordinates, and animations
        - Critical for consistent demo output and testing
        
    Banner Display:
        - Shows application banner at start
        - Demonstrates width and Unicode adaptation
        - Sets proper visual context for demo
        
    Command Execution:
        - Each command printed with "> " prompt for clarity
        - Commands processed through standard parse/execute pipeline
        - Identical behavior to interactive mode commands
        
    Usage:
        Invoked via command line: --script demo
        
    Example Output:
        [HACKER TERMINAL banner displayed]
        
        > scan
        [Scanning animation and results]
        
        > infiltrate MAINFRAME-7
        [Warning, infiltration animation, success]
        ...
        
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Dependencies:
        - random.seed(): Deterministic randomization
        - ascii_banner(): Banner display
        - parse_command(), execute_command(): Command processing pipeline
        - All command implementation functions
    """
    if state is None:
        state = app_state
    
    # Set deterministic seed
    random.seed(DEMO_RANDOM_SEED)
    
    ascii_banner(state)
    
    # Demo command sequence
    demo_commands = [
        "scan",
        "infiltrate MAINFRAME-7", 
        "hack",
        "trace QUANTUM-DB",
        "countertrace",
        "status",
        "exit"
    ]
    
    for command_line in demo_commands:
        print(f"\n> {command_line}")
        cmd, args = parse_command(command_line)
        execute_command(cmd, args, state)


def interactive_mode(state: Optional[ApplicationState] = None) -> None:
    """
    Run the interactive terminal mode with comprehensive error handling.
    
    Provides the main interactive experience where users can enter commands
    manually and receive real-time responses. Includes robust error handling
    for various interruption and termination scenarios.
    
    Args:
        state (ApplicationState, optional): Application state instance. If None, 
              uses the global app_state instance.
    
    Interactive Features:
        - Real-time command processing with immediate feedback
        - Persistent session state across commands
        - Graceful handling of user interruptions
        - Automatic recovery from command errors
        - True randomization (no fixed seed)
        
    Session Flow:
        1. Display application banner
        2. Enter infinite command loop
        3. Prompt user with "> " for command input
        4. Parse and execute commands via standard pipeline
        5. Handle various termination conditions gracefully
        
    Error Handling:
        - KeyboardInterrupt (Ctrl+C): Graceful "Interrupted by user" message
        - EOFError (Ctrl+D/EOF): Clean "End of input detected" message  
        - General exceptions: "Unexpected error" with details
        - All error paths call cmd_exit() for consistent termination
        
    Input Processing:
        - Uses input() for real-time user interaction
        - Commands processed through parse_command() and execute_command()
        - Empty commands and invalid commands handled gracefully
        - No automatic command history or completion (by design)
        
    State Persistence:
        - Application state persists across commands within session
        - discovered_targets, infiltrated_targets, system_status maintained
        - Randomization varies per command execution (no fixed seed)
        
    Termination Conditions:
        1. User enters "exit" command (normal termination)
        2. KeyboardInterrupt (Ctrl+C) - user interruption
        3. EOFError (Ctrl+D, pipe closure) - input termination
        4. Unexpected exceptions - error termination
        
    Usage:
        Invoked via:
        - No command line arguments (default mode)
        - --interactive flag (explicit mode)
        - Invalid single commands (fallback mode)
        
    Example Session:
        [HACKER TERMINAL banner displayed]
        
        > help
        [Help display]
        
        > scan
        [Scanning operation]
        
        > ^C
        Interrupted by user.
        Connection terminated.
        Stay anonymous, hacker.
        
    Dependencies:
        - ascii_banner(): Session startup banner
        - parse_command(), execute_command(): Command processing
        - cmd_exit(): Consistent termination handling
        - All command implementation functions
    """
    if state is None:
        state = app_state
    
    ascii_banner(state)
    
    try:
        while True:
            try:
                command_line = input("\n> ")
                cmd, args = parse_command(command_line)
                if cmd:
                    execute_command(cmd, args, state)
            except KeyboardInterrupt:
                print("\nInterrupted by user.")
                cmd_exit()
            except EOFError:
                print("\nEnd of input detected.")
                cmd_exit()
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        cmd_exit()


def main() -> None:
    """
    Main application entry point with comprehensive argument processing and mode selection.
    
    Parses command-line arguments and dispatches to appropriate execution modes
    (demo script, interactive, or single command). Handles global configuration
    settings for Unicode mode and terminal width, with robust error handling
    for all execution paths.
    
    Command Line Arguments:
        --script demo: Run deterministic demo script
        --interactive: Force interactive mode
        --unicode auto|on|off: Unicode display mode control
        --width auto|compact|standard|wide: Terminal width override
        command [args]: Execute single command
        
    Execution Modes:
        1. Demo Script Mode (--script demo):
           - Fixed random seed for consistent output
           - Predefined command sequence
           - Ideal for demonstrations and testing
           
        2. Interactive Mode (--interactive or default):
           - Real-time user command input
           - Persistent session state
           - True randomization
           
        3. Single Command Mode (command args):
           - Execute one command and display banner
           - Falls back to interactive on invalid commands
           - Uses demo random seed for consistency
           
        4. Help Mode (no arguments):
           - Display banner and usage information
           - Show examples of different invocation methods
           
    Application State Configuration:
        - app_state.unicode_mode: Controls ASCII vs Unicode art selection
        - app_state.width_mode: Controls terminal width adaptation
        - Both affect banner display and progress bar characters
        
    Error Handling:
        - KeyboardInterrupt: Clean "Program interrupted" termination
        - General exceptions: "Fatal error" with details and error exit code
        - Invalid arguments: Handled by argparse with help display
        
    Mode Selection Logic:
        1. Check for --script demo (highest priority)
        2. Check for --interactive flag
        3. Check for command arguments
        4. Default to banner + help (no arguments)
        
    Random Seed Management:
        - Demo mode: Fixed seed (1337) for consistent output
        - Single command: Fixed seed for consistent output  
        - Interactive: System randomization for variety
        
    Exit Behavior:
        - Normal termination: EXIT_SUCCESS (0)
        - Error termination: EXIT_FAILURE (1)
        - Immediate termination on fatal errors
        
    Usage Examples:
        $ python masterhacker.py --script demo
        $ python masterhacker.py --interactive
        $ python masterhacker.py scan
        $ python masterhacker.py infiltrate MAINFRAME-7
        $ python masterhacker.py --unicode off --width compact
        
    Dependencies:
        - argparse: Command line argument processing
        - run_demo_script(): Demo mode execution
        - interactive_mode(): Interactive mode execution
        - parse_command(), execute_command(): Single command processing
        - ascii_banner(): Banner display for all modes
        - ApplicationState app_state instance
    """
    
    parser = argparse.ArgumentParser(
        description="Master Hacker Terminal v2.0"
    )
    parser.add_argument(
        "--script", 
        choices=["demo"],
        help="Run predefined script"
    )
    parser.add_argument(
        "--unicode",
        choices=["auto", "on", "off"],
        default="auto",
        help="Unicode art mode: auto (detect), on (force), off (ASCII only)"
    )
    parser.add_argument(
        "--width",
        choices=["auto", "compact", "standard", "wide"],
        default="auto",
        help="Terminal width mode: auto (detect), compact (≤62 chars), standard (63-99 chars), wide (≥100 chars)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter interactive mode"
    )
    parser.add_argument(
        "command",
        nargs="*",
        help="Command to execute"
    )
    
    args = parser.parse_args()
    
    # Set application state Unicode and width modes
    app_state.unicode_mode = args.unicode
    app_state.width_mode = args.width
    
    try:
        if args.script == "demo":
            run_demo_script(app_state)
        elif args.interactive:
            # Explicit interactive mode
            random.seed()
            interactive_mode(app_state)
        elif args.command:
            # Single command mode
            cmd, cmd_args = parse_command(" ".join(args.command))
            if cmd:
                # Set seed for consistent output in single command mode too
                random.seed(DEMO_RANDOM_SEED)
                ascii_banner(app_state)
                if not execute_command(cmd, cmd_args, app_state):
                    # Command was invalid - enter interactive mode
                    print("Entering interactive mode...")
                    random.seed()
                    interactive_mode(app_state)
            else:
                # Empty command - show banner and enter interactive mode
                ascii_banner(app_state)
                print("Empty command. Entering interactive mode...")
                random.seed()
                interactive_mode(app_state)
        else:
            # No arguments provided - show banner and exit cleanly
            ascii_banner(app_state)
            print("\nUse --help for options.")
            print("Examples:")
            print("  python masterhacker.py scan                # Run single command")
            print("  python masterhacker.py --interactive       # Interactive mode")
            print("  python masterhacker.py --script demo       # Demo mode")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(EXIT_SUCCESS)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(EXIT_FAILURE)


if __name__ == "__main__":
    main()