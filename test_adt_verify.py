#!/usr/bin/env python3
"""
ADT 3.3.5a 功能验证脚本
验证修复后的功能是否正常工作
"""
import sys
import os
import struct

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock version manager
class MockVersionManager:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client_version = 2  # WOTLK
        return cls._instance
    def set_client_version(self, version):
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

# Patch modules before importing
import file_formats.adt_chunks as adt_chunks
adt_chunks.WoWVersionManager = MockVersionManager
adt_chunks.WoWVersions = WoWVersions

from file_formats.adt_chunks import MHDR, MH2O, SMLiquidChunk, SMLiquidInstance

def test_mhdr_wotlk():
    """Test MHDR for WotLK"""
    print("Testing MHDR for WoW 3.3.5a...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    expected_size = 44
    actual_size = mhdr.data_size
    
    print(f"  Expected: {expected_size}, Actual: {actual_size}")
    
    if actual_size == expected_size:
        print("  ✓ MHDR size correct for WotLK")
        return True
    else:
        print(f"  ✗ FAILED!")
        return False

def test_mhdr_cata():
    """Test MHDR for Cata+"""
    print("\nTesting MHDR for WoW Cata+...")
    
    # Change version to Cata
    MockVersionManager().client_version = WoWVersions.CATA
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    expected_size = 54
    actual_size = mhdr.data_size
    
    print(f"  Expected: {expected_size}, Actual: {actual_size}")
    
    # Reset to WotLK
    MockVersionManager().client_version = WoWVersions.WOTLK
    
    if actual_size == expected_size:
        print("  ✓ MHDR size correct for Cata+")
        return True
    else:
        print(f"  ✗ FAILED!")
        return False

def test_mh2o_structure():
    """Test MH2O structure"""
    print("\nTesting MH2O structure...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mh2o = MH2O(adt)
    
    # Check chunks array
    if len(mh2o.chunks) == 256:
        print("  ✓ MH2O has 256 chunks")
    else:
        print(f"  ✗ MH2O chunk count wrong: {len(mh2o.chunks)}")
        return False
    
    # Check SMLiquidChunk size
    if SMLiquidChunk.size == 12:
        print("  ✓ SMLiquidChunk size correct (12 bytes)")
    else:
        print(f"  ✗ SMLiquidChunk size wrong: {SMLiquidChunk.size}")
        return False
    
    # Check SMLiquidInstance size
    if SMLiquidInstance.size == 24:
        print("  ✓ SMLiquidInstance size correct (24 bytes)")
    else:
        print(f"  ✗ SMLiquidInstance size wrong: {SMLiquidInstance.size}")
        return False
    
    return True

def test_mh2o_add_liquid():
    """Test adding liquid to MH2O"""
    print("\nTesting MH2O add_liquid...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mh2o = MH2O(adt)
    
    # Add liquid to tile (5, 3)
    instance_idx = mh2o.add_liquid(
        tile_x=5, tile_y=3,
        liquid_type=0,  # Water
        min_height=0.0,
        max_height=10.0,
        width=8, height=8
    )
    
    chunk_idx = 3 * 16 + 5  # y * 16 + x
    
    if mh2o.chunks[chunk_idx].layer_count == 1:
        print("  ✓ Liquid added to correct chunk")
    else:
        print(f"  ✗ Chunk layer count wrong: {mh2o.chunks[chunk_idx].layer_count}")
        return False
    
    if len(mh2o.instances) == 1:
        print("  ✓ Instance added to list")
    else:
        print(f"  ✗ Instance count wrong: {len(mh2o.instances)}")
        return False
    
    if mh2o.instances[0].liquid_type == 0:
        print("  ✓ Liquid type correct (water)")
    else:
        print(f"  ✗ Liquid type wrong: {mh2o.instances[0].liquid_type}")
        return False
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("PyWoWLib ADT 3.3.5a Verification Suite")
    print("=" * 60)
    
    results = []
    results.append(("MHDR WotLK", test_mhdr_wotlk()))
    results.append(("MHDR Cata+", test_mhdr_cata()))
    results.append(("MH2O Structure", test_mh2o_structure()))
    results.append(("MH2O Add Liquid", test_mh2o_add_liquid()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("=" * 60)
    
    if all_passed:
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print("Some tests failed!")
        sys.exit(1)
