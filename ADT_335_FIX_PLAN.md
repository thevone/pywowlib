# ADT 3.3.5a 修复计划

## 发现的问题

### 1. MHDR 数据大小不正确
- **当前**: 54 字节（包含 mamp_value）
- **3.3.5a 应该是**: 44 字节（没有 mamp_value 和填充）

### 2. MCNK 结构版本检测问题
- 代码使用 `WoWVersionManager().client_version >= WoWVersions.MOP` 判断
- 但 3.3.5a 版本检测可能不准确
- 高分辨率孔洞 (hole_high_res) 是 MOP+ 特性，3.3.5a 使用低分辨率 (holes_low_res)

### 3. MH2O 水体块未完整实现
- 当前只有占位符实现
- 3.3.5a 引入 MH2O 替代 MCLQ，需要完整支持

### 4. 缺少 3.3.5a 特定测试
- 没有针对 3.3.5a 的测试用例
- 无法验证读写正确性

## 修复步骤

### Phase 1: MHDR 修复
- [ ] 根据版本调整 MHDR 数据大小
- [ ] 3.3.5a: 44 字节，Cata+: 54 字节

### Phase 2: MCNK 修复
- [ ] 修复版本检测逻辑
- [ ] 确保 3.3.5a 使用正确的偏移量格式
- [ ] 验证 MCCV (顶点颜色) 支持

### Phase 3: MH2O 完整实现
- [ ] 实现 SMLiquidChunk 结构
- [ ] 实现 SMLiquidInstance 结构
- [ ] 支持多种液体顶点格式

### Phase 4: 测试
- [ ] 创建 3.3.5a ADT 测试文件
- [ ] 验证读取正确性
- [ ] 验证写入正确性

## 参考文档
- wowdev.wiki ADT/v18 规范
- 已整理的 wow335_formats.md
