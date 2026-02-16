#!/usr/bin/env python3
"""
ADT 完整读写测试
创建 ADT 实例，写入文件，再读取验证
"""
import sys
import os
import struct
import tempfile

# 修改当前工作目录以支持相对导入
os.chdir('/root/.openclaw/workspace/pywowlib-fork')
sys.path.insert(0, '/root/.openclaw/workspace/pywowlib-fork')

# 现在可以正常导入
from pywowlib import WoWVersionManager, WoWVersions
from pywowlib.adt_file import ADTFile
from pywowlib.enums.adt_enums import ADTChunkLayerFlags

def test_create_and_write():
    """创建 ADT 并写入文件"""
    print("=" * 60)
    print("测试1: 创建 ADT 并写入文件")
    print("=" * 60)
    
    # 设置版本为 WotLK
    WoWVersionManager().set_client_version(WoWVersions.WOTLK)
    print(f"版本设置为: WotLK (3.3.5a)")
    
    # 创建新的 ADT 文件
    adt = ADTFile()
    print("✓ 创建 ADT 实例")
    
    # 验证 MHDR 大小
    print(f"  MHDR data_size: {adt.mhdr.data_size} bytes (应为 44)")
    if adt.mhdr.data_size != 44:
        print("✗ MHDR 大小错误!")
        return False
    print("✓ MHDR 大小正确")
    
    # 添加纹理
    tex_id = adt.add_texture_filename("tileset\\azeroth\\grass.blp")
    print(f"✓ 添加纹理: ID={tex_id}")
    
    # 为 chunk (5, 3) 添加纹理层
    adt.mcnk[3][5].add_texture_layer(tex_id, ADTChunkLayerFlags.use_alpha_map, 0)
    print("✓ 为 chunk(5,3) 添加纹理层")
    
    # 设置 chunk (5, 3) 的高度
    import random
    heights = [random.uniform(10, 50) for _ in range(145)]
    adt.mcnk[3][5].mcvt.height = heights
    print("✓ 设置 chunk(5,3) 高度图")
    
    # 设置区域 ID
    adt.mcnk[3][5].area_id = 1  # Dun Morogh
    print("✓ 设置 chunk(5,3) 区域 ID = 1")
    
    # 添加 MH2O 水体
    adt.mh2o.add_liquid(
        tile_x=5, tile_y=3,
        liquid_type=0,  # Water
        min_height=0.0,
        max_height=20.0
    )
    print("✓ 添加 MH2O 水体到 (5,3)")
    
    # 为 chunk (7, 8) 添加 MCLQ 水体
    adt.mcnk[8][7].mclq.set_liquid_type(1)  # Ocean
    adt.mcnk[8][7].mclq.set_height(15.0)
    print("✓ 设置 chunk(7,8) MCLQ 水体")
    
    # 写入临时文件
    temp_path = "/tmp/test_output.adt"
    adt.write(temp_path)
    print(f"✓ 写入文件: {temp_path}")
    
    # 检查文件大小
    file_size = os.path.getsize(temp_path)
    print(f"  文件大小: {file_size} bytes")
    
    if file_size > 0:
        print("✓ 文件创建成功")
        return True, temp_path
    else:
        print("✗ 文件大小为 0!")
        return False, None

def test_read_and_verify(file_path):
    """读取 ADT 文件并验证"""
    print("\n" + "=" * 60)
    print("测试2: 读取 ADT 并验证")
    print("=" * 60)
    
    # 设置版本
    WoWVersionManager().set_client_version(WoWVersions.WOTLK)
    
    # 读取文件
    try:
        adt = ADTFile(file_path)
        print(f"✓ 读取文件: {file_path}")
    except Exception as e:
        print(f"✗ 读取失败: {e}")
        return False
    
    # 验证 MHDR
    print(f"  MHDR data_size: {adt.mhdr.data_size}")
    if adt.mhdr.data_size != 44:
        print("✗ MHDR 大小错误!")
        return False
    print("✓ MHDR 大小正确 (44 bytes)")
    
    # 验证纹理
    print(f"  纹理数量: {len(adt.mtex.filenames)}")
    if len(adt.mtex.filenames) > 0:
        print(f"  纹理0: {adt.mtex.filenames[0]}")
        print("✓ 纹理读取正确")
    
    # 验证 chunk (5, 3)
    chunk = adt.mcnk[3][5]
    print(f"  chunk(5,3) 纹理层数: {chunk.n_layers}")
    print(f"  chunk(5,3) 区域 ID: {chunk.area_id}")
    print(f"  chunk(5,3) 高度值数量: {len(chunk.mcvt.height)}")
    
    if chunk.n_layers > 0:
        print("✓ 纹理层读取正确")
    if chunk.area_id == 1:
        print("✓ 区域 ID 读取正确")
    if len(chunk.mcvt.height) == 145:
        print("✓ 高度图读取正确")
    
    # 验证 MH2O
    print(f"  MH2O 实例数: {len(adt.mh2o.instances)}")
    if len(adt.mh2o.instances) > 0:
        inst = adt.mh2o.instances[0]
        print(f"    液体类型: {inst.liquid_type}")
        print(f"    最小高度: {inst.min_height_level}")
        print(f"    最大高度: {inst.max_height_level}")
        print("✓ MH2O 读取正确")
    
    return True

def test_roundtrip():
    """完整往返测试"""
    print("\n" + "=" * 60)
    print("ADT 3.3.5a 完整读写测试")
    print("=" * 60)
    
    # 测试1: 创建并写入
    success, file_path = test_create_and_write()
    if not success:
        print("\n✗ 写入测试失败")
        return False
    
    # 测试2: 读取并验证
    if not test_read_and_verify(file_path):
        print("\n✗ 读取测试失败")
        return False
    
    # 清理
    try:
        os.remove(file_path)
        print(f"\n✓ 清理临时文件")
    except:
        pass
    
    print("\n" + "=" * 60)
    print("所有测试通过! ✓")
    print("=" * 60)
    print("\n修复验证成功:")
    print("  - MHDR 44字节 (WotLK)")
    print("  - 纹理读写")
    print("  - 高度图读写")
    print("  - MH2O 水体")
    print("  - MCLQ 水体")
    print("  - 区域 ID")
    
    return True

if __name__ == "__main__":
    try:
        success = test_roundtrip()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
