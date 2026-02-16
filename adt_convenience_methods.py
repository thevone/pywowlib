#!/usr/bin/env python3
"""
ADT 3.3.5a 便利方法示例
这些可以添加到 adt_file.py 的 ADTFile 类中
"""

# Convenience methods for 3.3.5a

def get_chunk(self, x, y):
    """Get MCNK chunk at coordinates (0-15, 0-15)"""
    return self.mcnk[y][x]

def set_chunk_height(self, x, y, height_map):
    """Set height map for chunk at (x, y)
    
    Args:
        x, y: Chunk coordinates (0-15)
        height_map: List of 145 float values (9x9 + 8x8)
    """
    chunk = self.get_chunk(x, y)
    if len(height_map) != 145:
        raise ValueError("Height map must have 145 values")
    chunk.mcvt.height = list(height_map)

def add_texture_to_chunk(self, x, y, texture_path, flags=0, effect_id=0):
    """Add texture layer to chunk
    
    Args:
        x, y: Chunk coordinates (0-15)
        texture_path: Path to texture (e.g., "tileset\\azeroth\\grass.blp")
        flags: Layer flags
        effect_id: Effect ID
    
    Returns:
        Layer index
    """
    # Add texture to global list if not exists
    tex_id = self.add_texture_filename(texture_path)
    
    # Add layer to chunk
    chunk = self.get_chunk(x, y)
    chunk.add_texture_layer(tex_id, flags, effect_id)
    
    return chunk.n_layers - 1

def set_chunk_liquid_mh2o(self, x, y, liquid_type, min_height, max_height):
    """Set MH2O liquid for chunk (WotLK+ method)
    
    Args:
        x, y: Chunk coordinates (0-15)
        liquid_type: 0=water, 1=ocean, 2=magma, 3=slime
        min_height: Minimum liquid height
        max_height: Maximum liquid height
    """
    self.mh2o.add_liquid(x, y, liquid_type, min_height, max_height)

def set_chunk_liquid_mclq(self, x, y, liquid_type, height):
    """Set MCLQ liquid for chunk (legacy method)
    
    Args:
        x, y: Chunk coordinates (0-15)
        liquid_type: 0=water, 1=ocean, 2=magma, 3=slime
        height: Uniform liquid height
    """
    chunk = self.get_chunk(x, y)
    chunk.mclq.set_liquid_type(liquid_type)
    chunk.mclq.set_height(height)

def set_chunk_area_id(self, x, y, area_id):
    """Set area ID for chunk
    
    Args:
        x, y: Chunk coordinates (0-15)
        area_id: Area ID from AreaTable.dbc
    """
    chunk = self.get_chunk(x, y)
    chunk.area_id = area_id

def get_chunk_area_id(self, x, y):
    """Get area ID for chunk"""
    return self.get_chunk(x, y).area_id

# Example usage:
"""
from pywowlib import WoWVersionManager, WoWVersions
from pywowlib.adt_file import ADTFile

# Set version
WoWVersionManager().set_client_version(WoWVersions.WOTLK)

# Create new ADT
adt = ADTFile()

# Set height for chunk (5, 3)
import random
heights = [random.uniform(0, 100) for _ in range(145)]
adt.set_chunk_height(5, 3, heights)

# Add texture to chunk
adt.add_texture_to_chunk(5, 3, "tileset\\azeroth\\grass.blp")
adt.add_texture_to_chunk(5, 3, "tileset\\azeroth\\dirt.blp")

# Set liquid
adt.set_chunk_liquid_mh2o(5, 3, liquid_type=0, min_height=0, max_height=10)

# Set area ID
adt.set_chunk_area_id(5, 3, 1)  # Dun Morogh

# Save
adt.write("output.adt")
"""
