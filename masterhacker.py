#!/usr/bin/env python3
"""
Master Hacker Terminal v2.0 - Single File Implementation
A parody hacker movie terminal simulator
"""

import argparse
import os
import random
import shutil
import sys
import time
from typing import Dict, List, Optional, Set, Tuple, Union, Any

# Optional imports for Unix-like systems (for Unicode width probing)
try:
    import select
    import termios
    import tty
    HAS_UNIX_TTY = True
except ImportError:
    HAS_UNIX_TTY = False


# ASCII Art Constants - Width-Tiered System
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
 |                   [ VERSION 2.0.7 ]                     |
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
 |                           [ VERSION 2.0.7 ]                               |
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
 |                                     [ VERSION 2.0.7 ]                                          |
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

# Unicode Art Constants - Width-Tiered System
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
 ║                 [ VERSION 2.0.7 ]                   ║
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
 ║                         [ VERSION 2.0.7 ]                             ║
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
 ║                                   [ VERSION 2.0.7 ]                                        ║
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

# Global Unicode mode setting and width system
unicode_mode: str = "auto"
width_mode: str = "auto"  # Width detection mode: auto, compact, standard, wide

def utf8_env_check() -> bool:
    """Check if environment variables suggest UTF-8 support"""
    for var in ("LC_ALL", "LC_CTYPE", "LANG"):
        val = os.environ.get(var, "")
        if "UTF-8" in val.upper() or "utf8" in val.lower():
            return True
    return False

def terminal_hints_unicode() -> bool:
    """Check if TERM variable suggests Unicode capability"""
    term = os.environ.get("TERM", "").lower()
    unicode_terms = ("xterm-256color", "screen-256color", "tmux-256color")
    return any(term.startswith(t) for t in unicode_terms)

def probe_unicode_width() -> bool:
    """
    Safe probe to test if Unicode renders with expected width.
    Returns True if Unicode appears safe to use.
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
        ready, _, _ = select.select([sys.stdin], [], [], 0.5)
        if ready:
            # Read available data without blocking
            response = ""
            while select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                char = sys.stdin.read(1)
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

def should_use_unicode() -> bool:
    """Determine if Unicode should be used based on current mode and environment"""
    global unicode_mode
    
    if unicode_mode == "off":
        return False
    elif unicode_mode == "on":
        return True
    elif unicode_mode == "auto":
        # Auto-detection: fast, non-blocking checks only
        # Skip the problematic width probe that blocks execution
        return (utf8_env_check() and terminal_hints_unicode())
    return False

def get_banner() -> str:
    """Get appropriate banner based on Unicode mode and terminal width"""
    width_tier = get_width_mode()
    
    if should_use_unicode():
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

def get_access_granted() -> str:
    """Get appropriate access granted box based on Unicode mode and terminal width"""
    width_tier = get_width_mode()
    
    if should_use_unicode():
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

def get_warning_box() -> str:
    """Get appropriate warning box based on Unicode mode and terminal width"""
    width_tier = get_width_mode()
    
    if should_use_unicode():
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

def get_progress_chars() -> Dict[str, str]:
    """Get appropriate progress bar characters based on Unicode mode"""
    if should_use_unicode():
        return {'filled': '█', 'empty': '░'}
    else:
        return {'filled': '#', 'empty': '.'}


def get_terminal_width() -> int:
    """
    Get terminal width with comprehensive fallback chain.
    
    Returns:
        int: Terminal width in characters
    """
    # Primary: shutil.get_terminal_size() with proper error handling
    try:
        size = shutil.get_terminal_size()
        if size.columns > 0:
            return size.columns
    except (OSError, AttributeError):
        pass
    
    # Fallback 1: COLUMNS environment variable
    columns_env = os.environ.get('COLUMNS')
    if columns_env and columns_env.isdigit():
        columns = int(columns_env)
        if columns > 0:
            return columns
    
    # Fallback 2: TERM_COLS environment variable
    term_cols_env = os.environ.get('TERM_COLS')
    if term_cols_env and term_cols_env.isdigit():
        term_cols = int(term_cols_env)
        if term_cols > 0:
            return term_cols
    
    # Final fallback: Default to 80 columns
    return 80


def classify_width(width: int) -> str:
    """Classify terminal width into compact, standard, or wide tiers
    
    Args:
        width (int): Terminal width in characters
        
    Returns:
        str: Width tier - 'compact', 'standard', or 'wide'
    """
    if width <= 62:
        return 'compact'
    elif width <= 99:
        return 'standard'
    else:
        return 'wide'


def get_terminal_width_tier() -> str:
    """
    Get terminal width tier with edge case handling.
    
    Returns:
        str: Width tier - 'compact', 'standard', or 'wide'
    """
    # Handle non-interactive terminals (pipes, redirected output)
    if not sys.stdout.isatty():
        # Default to standard for non-interactive output
        return 'standard'
    
    # Get terminal width with fallback chain
    width = get_terminal_width()
    return classify_width(width)


def get_width_mode() -> str:
    """Determine current width mode based on settings and terminal"""
    global width_mode
    
    if width_mode in ['compact', 'standard', 'wide']:
        # Explicit mode set via CLI argument
        return width_mode
    elif width_mode == 'auto':
        # Auto-detect based on terminal width
        return get_terminal_width_tier()
    else:
        # Fallback to standard for unknown modes
        return 'standard'


def progress(label: str = "Processing", steps: int = 20, delay: float = 0.08) -> None:
    """Enhanced progress bar with cinematic styling"""
    print(f"\n[{label.upper()}]")
    print("+" + "-" * 52 + "+")
    
    chars = get_progress_chars()
    
    for i in range(steps + 1):
        filled = chars['filled'] * i
        empty = chars['empty'] * (steps - i)
        percent = int((i / steps) * 100)
        
        # Add scanning dots for effect
        dots = "..." if i % 3 == 0 else ".." if i % 3 == 1 else "."
        
        print(f"| [{filled}{empty}] {percent:3d}% {dots:<3} |", end="")
        print("\r", end="", flush=True)
        time.sleep(delay)
    
    print("\n+" + "-" * 52 + "+")
    time.sleep(0.2)


def show_access_granted() -> None:
    """Display ACCESS GRANTED box"""
    print(get_access_granted())
    time.sleep(1)


def show_warning() -> None:
    """Display WARNING box"""
    print(get_warning_box())
    time.sleep(1.5)


def ascii_banner() -> None:
    """Display the art banner (ASCII or Unicode based on mode)"""
    print(get_banner())




def random_line(options: List[str]) -> str:
    """Return a random line from options list"""
    return random.choice(options)


# Global state for discovered targets
discovered_targets: List[Tuple[str, str]] = []
infiltrated_targets: Set[str] = set()
system_status: Dict[str, Any] = {
    "online": True,
    "security_level": "MAXIMUM", 
    "connections": 3,
    "firewall": True,
    "stealth": True,
    "compromised_systems": 0,
    "credits": 0
}


def cmd_help() -> None:
    """Display available commands"""
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


def cmd_scan() -> None:
    """Scan for available targets"""
    global discovered_targets
    
    progress("Scanning network", 24, 0.12)
    
    # Fixed targets to match SCOPE.md demo exactly
    discovered_targets = [
        ("MAINFRAME-7", "low"),
        ("QUANTUM-DB", "high"), 
        ("SATELLITE-X", "medium")
    ]
    
    print(f"Found {len(discovered_targets)} targets:")
    for name, security in discovered_targets:
        print(f"- {name} (security: {security})")


def cmd_decrypt() -> None:
    """Decrypt intercepted data"""
    progress("Decrypting data", 26, 0.10)
    
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


def cmd_infiltrate(target: Optional[str]) -> None:
    """Infiltrate specified target"""
    if not target:
        print("Target required. Usage: infiltrate <target>")
        return
        
    target = target.upper()
    
    # Check if target was discovered
    target_names = [name for name, _ in discovered_targets]
    if target not in target_names:
        print("Target not found. Run 'scan' first.")
        return
    
    show_warning()
    print(f"Infiltrating {target}...")
    progress("Bypassing security", 28, 0.15)
    
    infiltrated_targets.add(target)
    show_access_granted()
    print("Root privileges obtained.")


def cmd_hack() -> None:
    """Execute hack sequence"""
    show_warning()
    print("Initiating hack sequence...")
    progress("Exploiting vulnerabilities", 30, 0.12)
    
    # Fixed values to match SCOPE.md demo exactly  
    systems = 5
    credits = 1337
    
    system_status["compromised_systems"] = systems
    system_status["credits"] = credits
    
    show_access_granted()
    print("HACK SUCCESSFUL")
    print(f"Systems compromised: {systems}")
    print(f"Credits earned: {credits}")


def cmd_trace(target: Optional[str]) -> None:
    """Trace target location"""
    if not target:
        print("Target required. Usage: trace <target>")
        return
        
    target = target.upper()
    
    print(f"Tracing {target}...")
    progress("Triangulating position", 25, 0.13)
    
    # Predefined locations for consistency
    locations = {
        "QUANTUM-DB": ("37.7749 deg N, 122.4194 deg W", "CyberCorp Industries"),
        "MAINFRAME-7": ("40.7128 deg N, 74.0060 deg W", "MegaCorp Systems"),
        "SATELLITE-X": ("51.5074 deg N, 0.1278 deg W", "SkyNet Communications"),
        "NEXUS-CORE": ("35.6762 deg N, 139.6503 deg E", "Tech Dynamics"),
        "CRYPTO-VAULT": ("52.5200 deg N, 13.4050 deg E", "SecureMax GmbH"),
        "DATA-CENTER": ("34.0522 deg N, 118.2437 deg W", "InfoTech Solutions")
    }
    
    if target in locations:
        coords, isp = locations[target]
        print(f"Location found: {coords}")
        print(f"ISP: {isp}")
    else:
        # Fallback for unknown targets
        lat = round(random.uniform(-90, 90), 4)
        lon = round(random.uniform(-180, 180), 4)
        isps = ["CyberCorp Industries", "TechMax Solutions", "DataFlow Systems"]
        print(f"Location found: {lat} deg N, {lon} deg W")
        print(f"ISP: {random_line(isps)}")


def cmd_countertrace() -> None:
    """Deploy countermeasures against traces"""
    print("Deploying countermeasures...")
    progress("Scrambling identity", 22, 0.11)
    show_access_granted()
    print("Trace blocked. Identity scrambled.")


def cmd_status() -> None:
    """Show system status"""
    status_map = {
        True: "ENABLED",
        False: "DISABLED"
    }
    
    print(f"System Status: {'ONLINE' if system_status['online'] else 'OFFLINE'}")
    print(f"Security Level: {system_status['security_level']}")
    print(f"Active Connections: {system_status['connections']}")
    print(f"Firewall: {status_map[system_status['firewall']]}")
    print(f"Stealth Mode: {'ON' if system_status['stealth'] else 'OFF'}")


def cmd_clear() -> None:
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


def cmd_exit() -> None:
    """Exit the terminal"""
    print("Connection terminated.")
    print("Stay anonymous, hacker.")
    sys.exit(0)


def parse_command(command_line: str) -> Tuple[Optional[str], List[str]]:
    """Parse command line and return command and arguments"""
    parts = command_line.strip().split()
    if not parts:
        return None, []
    return parts[0].lower(), parts[1:]


def execute_command(cmd: Optional[str], args: List[str]) -> bool:
    """Execute a command with given arguments. Returns True if command was valid, False otherwise"""
    if cmd is None:
        return False
    elif cmd == "help":
        cmd_help()
    elif cmd == "scan":
        cmd_scan()
    elif cmd == "decrypt":
        cmd_decrypt()
    elif cmd == "infiltrate":
        target = args[0] if args else None
        cmd_infiltrate(target)
    elif cmd == "hack":
        cmd_hack()
    elif cmd == "trace":
        target = args[0] if args else None
        cmd_trace(target)
    elif cmd in ["countertrace", "evade"]:
        cmd_countertrace()
    elif cmd == "status":
        cmd_status()
    elif cmd == "clear":
        cmd_clear()
    elif cmd == "exit":
        cmd_exit()
    else:
        print("Command not recognized. Type 'help' for available commands.")
        return False
    return True


def run_demo_script() -> None:
    """Run the deterministic demo script"""
    # Set deterministic seed
    random.seed(1337)
    
    ascii_banner()
    
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
        execute_command(cmd, args)


def interactive_mode() -> None:
    """Run interactive terminal mode with robust error handling"""
    ascii_banner()
    
    try:
        while True:
            try:
                command_line = input("\n> ")
                cmd, args = parse_command(command_line)
                if cmd:
                    execute_command(cmd, args)
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
    """Main entry point"""
    global unicode_mode, width_mode
    
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
    
    # Set global Unicode and width modes
    unicode_mode = args.unicode
    width_mode = args.width
    
    try:
        if args.script == "demo":
            run_demo_script()
        elif args.interactive:
            # Explicit interactive mode
            random.seed()
            interactive_mode()
        elif args.command:
            # Single command mode
            cmd, cmd_args = parse_command(" ".join(args.command))
            if cmd:
                # Set seed for consistent output in single command mode too
                random.seed(1337)
                ascii_banner()
                if not execute_command(cmd, cmd_args):
                    # Command was invalid - enter interactive mode
                    print("Entering interactive mode...")
                    random.seed()
                    interactive_mode()
            else:
                # Empty command - show banner and enter interactive mode
                ascii_banner()
                print("Empty command. Entering interactive mode...")
                random.seed()
                interactive_mode()
        else:
            # No arguments provided - show banner and exit cleanly
            ascii_banner()
            print("\nUse --help for options.")
            print("Examples:")
            print("  python masterhacker.py scan                # Run single command")
            print("  python masterhacker.py --interactive       # Interactive mode")
            print("  python masterhacker.py --script demo       # Demo mode")
    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()