#!/usr/bin/env python3
"""
Test script for WoW 3.3.5a ADT support
Run from project root: python3 test_adt_335.py
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Direct imports from modules
from io_utils.types import singleton

@singleton
class WoWVersionManager:
    def __init__(self):
        self.client_version = 0
    def set_client_version(self, version: int):
        self.client_version = version

class WoWVersions:
    CLASSIC = 0
    TBC = 1
    WOTLK = 2
    CATA = 3
    MOP = 4
    WOD = 5
    LEGION = 6
    BFA = 7
    NEW_CLASSIC = 8

# Now test MHDR
from file_formats.adt_chunks import MHDR

def test_mhdr_wotlk():
    """Test MHDR for WotLK (3.3.5a)"""
    print("Testing MHDR for WoW 3.3.5a...")
    
    # Set version to WotLK
    WoWVersionManager().set_client_version(WoWVersions.WOTLK)
    
    # Create a mock ADT object
    class MockADT:
        def _register_mobile_chunk(self, chunk):
            pass
        def _register_offset(self, ofs):
            pass
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    # Check MHDR data size
    expected_size = 44  # WotLK MHDR size
    actual_size = mhdr.data_size
    
    print(f"  Expected MHDR size: {expected_size}")
    print(f"  Actual MHDR size: {actual_size}")
    
    if actual_size == expected_size:
        print("  ✓ MHDR size correct for WotLK")
        return True
    else:
        print(f"  ✗ MHDR size incorrect! Expected {expected_size}, got {actual_size}")
        return False

def test_mhdr_cata():
    """Test MHDR for Cata+"""
    print("\nTesting MHDR for WoW Cata+...")
    
    # Set version to Cata
    WoWVersionManager().set_client_version(WoWVersions.CATA)
    
    # Create a mock ADT object
    class MockADT:
        def _register_mobile_chunk(self, chunk):
            pass
        def _register_offset(self, ofs):
            pass
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    # Check MHDR data size
    expected_size = 54  # Cata+ MHDR size
    actual_size = mhdr.data_size
    
    print(f"  Expected MHDR size: {expected_size}")
    print(f"  Actual MHDR size: {actual_size}")
    
    if actual_size == expected_size:
        print("  ✓ MHDR size correct for Cata+")
        return True
    else:
        print(f"  ✗ MHDR size incorrect! Expected {expected_size}, got {actual_size}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("PyWoWLib ADT 3.3.5a Test Suite")
    print("=" * 50)
    
    results = []
    results.append(("MHDR WotLK", test_mhdr_wotlk()))
    results.append(("MHDR Cata+", test_mhdr_cata()))
    
    print("\n" + "=" * 50)
    print("Test Results:")
    print("=" * 50)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("=" * 50)
    if all_passed:
        print("All tests passed!")
    else:
        print("Some tests failed!")
        sys.exit(1)
