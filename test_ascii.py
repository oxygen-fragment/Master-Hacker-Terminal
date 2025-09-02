#!/usr/bin/env python3
"""Test script to preview the ASCII art"""

# Import the constants from the main file
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from masterhacker import ASCII_BANNER, ACCESS_GRANTED, WARNING_BOX

def main():
    print("=== Testing ASCII Banner ===")
    print(ASCII_BANNER)
    
    print("\n=== Testing Access Granted Box ===")
    print(ACCESS_GRANTED)
    
    print("\n=== Testing Warning Box ===")
    print(WARNING_BOX)
    
    print("\n=== ASCII Art Test Complete ===")

if __name__ == "__main__":
    main()