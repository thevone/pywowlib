# PyWoWLib ADT 3.3.5a 修复进展

## 已完成

### 1. MHDR 修复 ✅
- **问题**: MHDR 数据大小固定为 54 字节，但 3.3.5a 只需要 44 字节
- **修复**: 
  - 添加 `data_size_wotlk = 44` 和 `data_size_cata_plus = 54`
  - 添加 `_set_data_size()` 方法根据版本动态设置
  - 更新 `read()` 和 `write()` 方法处理版本差异

### 2. 代码提交 ✅
- 已提交到本地仓库
- 包含测试脚本 `test_adt_335.py`

## 待修复

### 1. MH2O 完整实现 ⚠️
- **当前状态**: 只有占位符实现
- **需要**: 完整实现 WotLK 引入的 MH2O 水体块
- **参考**: wowdev.wiki ADT/v18 规范

### 2. MCNK 版本检测 ⚠️
- **问题**: 使用 `WoWVersionManager` 判断，但 3.3.5a 支持不完整
- **需要**: 验证 MCNK 结构在 3.3.5a 下的正确性

### 3. 测试验证 ⚠️
- **需要**: 使用真实的 3.3.5a ADT 文件测试读写

## 使用方法

```python
from pywowlib import WoWVersionManager, WoWVersions
from pywowlib.adt_file import ADTFile

# 设置版本为 WotLK
WoWVersionManager().set_client_version(WoWVersions.WOTLK)

# 创建/读取 ADT 文件
adt = ADTFile("path/to/adt.adt")

# 修改...

# 保存
adt.write("path/to/output.adt")
```

## 提交到 GitHub

由于需要身份验证，请使用以下方式之一：

### 方式1: GitHub Token
```bash
git remote set-url origin https://YOUR_TOKEN@github.com/thevone/pywowlib.git
git push origin master
```

### 方式2: 手动上传
1. 下载修改后的文件
2. 上传到 GitHub 仓库

## 参考
- wowdev.wiki ADT/v18 规范
- 已整理的 wow335_formats.md 文档
