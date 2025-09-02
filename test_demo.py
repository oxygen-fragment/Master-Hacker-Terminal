#!/usr/bin/env python3
"""Test script to verify demo mode runs without freezing"""

import subprocess
import sys
import time
import os

def test_demo_modes():
    """Test all demo modes to ensure they don't freeze"""
    print("Testing demo modes for freezing issues...")
    
    test_cases = [
        ("ASCII demo", ["python", "masterhacker.py", "--unicode", "off", "--script", "demo"]),
        ("Unicode forced demo", ["python", "masterhacker.py", "--unicode", "on", "--script", "demo"]),
        ("Auto-detect demo", ["python", "masterhacker.py", "--unicode", "auto", "--script", "demo"]),
        ("Single command", ["python", "masterhacker.py", "--unicode", "off", "help"]),
    ]
    
    for test_name, cmd in test_cases:
        print(f"\n--- Testing {test_name} ---")
        try:
            # Run with timeout to detect freezing
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=30,  # 30 second timeout
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            if result.returncode == 0:
                print(f"✓ {test_name} completed successfully")
                print(f"  Output length: {len(result.stdout)} chars")
                if result.stderr:
                    print(f"  Stderr: {result.stderr}")
            else:
                print(f"✗ {test_name} failed with return code {result.returncode}")
                print(f"  Stdout: {result.stdout}")
                print(f"  Stderr: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"✗ {test_name} FROZE (timed out after 30s)")
        except Exception as e:
            print(f"✗ {test_name} error: {e}")
    
    print("\n--- Test Summary ---")
    print("If all tests show '✓ completed successfully', freezing issues are resolved.")

if __name__ == "__main__":
    test_demo_modes()