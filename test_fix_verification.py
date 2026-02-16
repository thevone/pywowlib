#!/usr/bin/env python3
"""
ADT 3.3.5a 修复验证测试
创建最小化 ADT 文件并验证读写正确性
"""
import sys
import os
import struct
import tempfile

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock version manager before importing
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

# Patch before import
import file_formats.adt_chunks as adt_chunks
adt_chunks.WoWVersionManager = MockVersionManager
adt_chunks.WoWVersions = WoWVersions

from file_formats.adt_chunks import (
    MVER, MHDR, MH2O, MCLQ, MCNK, MCVT, MCLY, MCAL,
    SMLiquidChunk, SMLiquidInstance, SMLiquidAttributes,
    MCLQVertex, MCLQAttributes
)
from file_formats.wow_common_types import ChunkHeader
from io import BytesIO

def test_mver():
    """Test MVER chunk"""
    print("Testing MVER...")
    mver = MVER()
    
    # Write
    buf = BytesIO()
    mver.write(buf)
    
    # Read back
    buf.seek(0)
    mver2 = MVER()
    mver2.read(buf)
    
    if mver2.version == 18:
        print("  ✓ MVER read/write correct (version 18)")
        return True
    else:
        print(f"  ✗ MVER failed: version={mver2.version}")
        return False

def test_mhdr_wotlk():
    """Test MHDR for WotLK"""
    print("\nTesting MHDR (WotLK 3.3.5a)...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    MockVersionManager().client_version = WoWVersions.WOTLK
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    # Check size
    if mhdr.data_size != 44:
        print(f"  ✗ MHDR size wrong: {mhdr.data_size} (expected 44)")
        return False
    
    # Write and check size
    buf = BytesIO()
    mhdr.write(buf)
    written_size = buf.tell() - 8  # minus chunk header
    
    if written_size == 44:
        print("  ✓ MHDR size correct (44 bytes for WotLK)")
    else:
        print(f"  ✗ MHDR written size wrong: {written_size}")
        return False
    
    # Read back
    buf.seek(0)
    mhdr2 = MHDR(adt)
    mhdr2.read(buf)
    
    print("  ✓ MHDR read/write successful")
    return True

def test_mhdr_cata():
    """Test MHDR for Cata+"""
    print("\nTesting MHDR (Cata+)...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    MockVersionManager().client_version = WoWVersions.CATA
    
    adt = MockADT()
    mhdr = MHDR(adt)
    
    if mhdr.data_size != 54:
        print(f"  ✗ MHDR size wrong: {mhdr.data_size} (expected 54)")
        MockVersionManager().client_version = WoWVersions.WOTLK
        return False
    
    buf = BytesIO()
    mhdr.write(buf)
    written_size = buf.tell() - 8
    
    if written_size == 54:
        print("  ✓ MHDR size correct (54 bytes for Cata+)")
    else:
        print(f"  ✗ MHDR written size wrong: {written_size}")
        MockVersionManager().client_version = WoWVersions.WOTLK
        return False
    
    MockVersionManager().client_version = WoWVersions.WOTLK
    return True

def test_mh2o():
    """Test MH2O chunk"""
    print("\nTesting MH2O...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mh2o = MH2O(adt)
    
    # Check structure
    if len(mh2o.chunks) != 256:
        print(f"  ✗ MH2O chunk count wrong: {len(mh2o.chunks)}")
        return False
    print("  ✓ MH2O has 256 chunks")
    
    # Add liquid
    mh2o.add_liquid(5, 3, liquid_type=0, min_height=0.0, max_height=10.0)
    
    chunk_idx = 3 * 16 + 5
    if mh2o.chunks[chunk_idx].layer_count != 1:
        print(f"  ✗ Layer count wrong")
        return False
    print("  ✓ add_liquid() works")
    
    if len(mh2o.instances) != 1:
        print(f"  ✗ Instance count wrong")
        return False
    print("  ✓ Instance added correctly")
    
    # Write test
    buf = BytesIO()
    mh2o.set_address(0)
    mh2o.write(buf)
    
    expected_size = 256 * 12 + 24 + 0  # chunks + 1 instance + 0 attributes
    if mh2o.header.size == expected_size:
        print(f"  ✓ MH2O write size correct ({expected_size} bytes)")
    else:
        print(f"  ✗ MH2O size wrong: {mh2o.header.size}")
        return False
    
    return True

def test_mclq():
    """Test MCLQ chunk"""
    print("\nTesting MCLQ...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
        def _register_offset(self, ofs): pass
    
    adt = MockADT()
    mclq = MCLQ(adt)
    
    # Set properties
    mclq.set_liquid_type(0)  # Water
    mclq.set_height(5.0)
    mclq.set_tile_attribute(3, 4, fishable=True, deep=False)
    
    # Check vertices
    if len(mclq.vertices) != 9:
        print(f"  ✗ Vertex rows wrong: {len(mclq.vertices)}")
        return False
    if len(mclq.vertices[0]) != 9:
        print(f"  ✗ Vertex cols wrong: {len(mclq.vertices[0])}")
        return False
    print("  ✓ MCLQ has 9x9 vertices")
    
    # Check height set
    if mclq.vertices[0][0].liquid_height == 5.0:
        print("  ✓ set_height() works")
    else:
        print(f"  ✗ Height not set: {mclq.vertices[0][0].liquid_height}")
        return False
    
    # Write test
    buf = BytesIO()
    mclq.set_address(0)
    mclq.write(buf)
    
    expected_size = 81 * 8 + 16  # 9*9*8 + 16 = 656
    if mclq.header.size == expected_size:
        print(f"  ✓ MCLQ write size correct ({expected_size} bytes)")
    else:
        print(f"  ✗ MCLQ size wrong: {mclq.header.size}")
        return False
    
    return True

def test_mcvt():
    """Test MCVT (height map)"""
    print("\nTesting MCVT...")
    
    class MockADT:
        def _register_mobile_chunk(self, chunk): pass
    
    adt = MockADT()
    mcvt = MCVT(adt)
    
    # Check size
    if len(mcvt.height) != 145:
        print(f"  ✗ Height count wrong: {len(mcvt.height)}")
        return False
    print("  ✓ MCVT has 145 height values")
    
    # Set height
    mcvt.height = [float(i) for i in range(145)]
    
    # Write
    buf = BytesIO()
    mcvt.set_address(0)
    mcvt.write(buf)
    
    # Read back
    buf.seek(0)
    mcvt2 = MCVT(adt)
    mcvt2.set_address(0)
    mcvt2.read(buf)
    
    if mcvt2.height[0] == 0.0 and mcvt2.height[144] == 144.0:
        print("  ✓ MCVT read/write correct")
        return True
    else:
        print(f"  ✗ MCVT values wrong")
        return False

def test_struct_sizes():
    """Verify struct sizes match WoW 3.3.5a spec"""
    print("\nTesting struct sizes...")
    
    sizes = {
        'SMLiquidChunk': (SMLiquidChunk.size, 12),
        'SMLiquidInstance': (SMLiquidInstance.size, 24),
        'SMLiquidAttributes': (SMLiquidAttributes.size, 16),
        'MCLQVertex': (MCLQVertex.size, 8),
        'MCLQAttributes': (MCLQAttributes.size, 8),
    }
    
    all_correct = True
    for name, (actual, expected) in sizes.items():
        if actual == expected:
            print(f"  ✓ {name}: {actual} bytes")
        else:
            print(f"  ✗ {name}: {actual} bytes (expected {expected})")
            all_correct = False
    
    return all_correct

if __name__ == "__main__":
    print("=" * 60)
    print("PyWoWLib ADT 3.3.5a Fix Verification")
    print("=" * 60)
    
    results = []
    results.append(("MVER", test_mver()))
    results.append(("MHDR WotLK", test_mhdr_wotlk()))
    results.append(("MHDR Cata+", test_mhdr_cata()))
    results.append(("MH2O", test_mh2o()))
    results.append(("MCLQ", test_mclq()))
    results.append(("MCVT", test_mcvt()))
    results.append(("Struct Sizes", test_struct_sizes()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    print("=" * 60)
    
    if all_passed:
        print("All tests PASSED! ✓")
        print("\nFixes are working correctly for WoW 3.3.5a")
        sys.exit(0)
    else:
        print("Some tests FAILED!")
        sys.exit(1)
