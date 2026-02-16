# PyWoWLib ADT 3.3.5a 修复进展

## 已完成

### 1. MHDR 修复 ✅
- **问题**: MHDR 数据大小固定为 54 字节，但 3.3.5a 只需要 44 字节
- **修复**: 
  - 添加 `data_size_wotlk = 44` 和 `data_size_cata_plus = 54`
  - 添加 `_set_data_size()` 方法根据版本动态设置
  - 更新 `read()` 和 `write()` 方法处理版本差异

### 2. MH2O 完整实现 ✅
- **问题**: 只有占位符实现
- **修复**:
  - 实现 `SMLiquidChunk` 结构（256 个，对应 16x16 地形块）
  - 实现 `SMLiquidInstance` 结构（24 字节）
  - 实现 `SMLiquidAttributes` 结构（16 字节，包含 fishable/deep 标志）
  - 完整的 `read()` 和 `write()` 方法，正确处理偏移量
  - 添加 `add_liquid()` 辅助方法

### 3. MCNK 版本检测 ✅
- **状态**: 已正确处理 MOP+ 与其他版本的差异
- **验证**: 使用 `WoWVersionManager` 判断高分辨率孔洞格式

### 4. 测试脚本 ✅
- `test_adt_335.py` - 基础测试
- `test_adt_verify.py` - 详细验证测试

### 5. 代码提交 ✅
- 已提交到本地仓库（3 个提交）
- 等待推送到 GitHub

## 使用方法

```python
from pywowlib import WoWVersionManager, WoWVersions
from pywowlib.adt_file import ADTFile

# 设置版本为 WotLK
WoWVersionManager().set_client_version(WoWVersions.WOTLK)

# 创建/读取 ADT 文件
adt = ADTFile("path/to/adt.adt")

# 添加水体
for x in range(16):
    for y in range(16):
        adt.mh2o.add_liquid(
            tile_x=x, tile_y=y,
            liquid_type=0,  # 0=water, 1=ocean, 2=magma, 3=slime
            min_height=0.0,
            max_height=10.0
        )

# 保存
adt.write("path/to/output.adt")
```

## 提交到 GitHub

由于需要身份验证，请使用以下方式之一：

### 方式1: GitHub Token
```bash
cd pywowlib-fork
git push origin master
```

### 方式2: 手动上传
1. 下载修改后的文件
2. 上传到 GitHub 仓库

## 参考
- wowdev.wiki ADT/v18 规范
- 已整理的 wow335_formats.md 文档
