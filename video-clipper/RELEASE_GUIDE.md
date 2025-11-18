# GitHub Release 创建指南

## ⚠️ 重要：避免乱码问题

创建GitHub Release时，如果标题包含中文，可能会出现乱码。请按照以下步骤操作：

## 📋 创建Release的标准流程

### 方法1：使用PowerShell脚本（推荐）

```powershell
cd video-clipper
.\create_release.ps1 -Version "v1.3.1" -ReleaseNotesFile "RELEASE_NOTES_v1.3.1.md" -ExeFile "dist\VideoClipper_v1.3.1.exe"
```

### 方法2：使用GitHub CLI（手动）

```powershell
# 1. 设置UTF-8编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 2. 从发布说明文件提取标题（第一行，去掉#号）
$title = (Get-Content "RELEASE_NOTES_v1.3.1.md" -Encoding UTF8 -First 1) -replace '^#\s*', ''

# 3. 创建Release（使用--title参数明确指定标题）
gh release create v1.3.1 `
    --title $title `
    --notes-file RELEASE_NOTES_v1.3.1.md `
    dist\VideoClipper_v1.3.1.exe
```

### 方法3：使用英文标题（最安全）

如果担心编码问题，可以使用英文标题：

```powershell
gh release create v1.3.1 `
    --title "VideoClipper v1.3.1" `
    --notes-file RELEASE_NOTES_v1.3.1.md `
    dist\VideoClipper_v1.3.1.exe
```

## 📝 发布说明文件格式

发布说明文件（`RELEASE_NOTES_v*.md`）的第一行应该是标题，格式如下：

```markdown
# 视频裁剪工具 v1.3.1 发布说明
```

脚本会自动提取这个标题作为Release标题。

## 🔧 修复已存在的乱码Release

如果Release标题已经出现乱码，可以使用以下命令修复：

```powershell
# 设置UTF-8编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 修复Release标题
gh release edit v1.3.1 --title "视频裁剪工具 v1.3.1"
```

## ✅ 检查清单

创建Release前，请确认：

- [ ] 版本号已更新到所有相关文件
- [ ] EXE文件已生成
- [ ] 发布说明文件已创建（UTF-8编码）
- [ ] 代码已提交并推送到GitHub
- [ ] Tag已创建并推送
- [ ] 使用正确的编码方式创建Release

## 🐛 常见问题

### 问题1：Release标题显示乱码

**原因**：PowerShell默认编码不是UTF-8

**解决方案**：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8
```

### 问题2：发布说明中的中文显示乱码

**原因**：文件编码不是UTF-8

**解决方案**：确保发布说明文件使用UTF-8编码保存

### 问题3：GitHub CLI无法识别中文

**解决方案**：使用`--title`参数明确指定标题，而不是让CLI自动从文件读取

---

**最后更新**: 2025-11-18

