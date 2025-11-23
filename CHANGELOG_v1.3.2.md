# 更新日志 v1.3.2

## 🔒 稳定性增强

### 自动修复不可读视频
- **问题**: 部分 H.264/H.265 录制的视频在 MoviePy 中无法解析 duration
- **方案**: 新增 `ensure_video_readable()`，必要时自动调用 FFmpeg `-fflags +genpts -c copy` 重封装
- **结果**: 用户无需手动预处理即可继续裁剪流程

### 临时目录治理
- 所有自动生成的临时目录集中登记
- `cleanup_temp_dirs()` 在单次或批量任务结束后统一清理

## 🛠️ 工程改进

- `VideoClipper.spec`、`file_version_info.txt`、UI 标签等全部更新为 v1.3.2
- README / PROJECT_STRUCTURE / RELEASE_GUIDE / Release Notes 同步版本号与下载链接

## 📦 构建与发布

- 默认构建输出 `dist/VideoClipper_v1.3.2.exe`
- Release 说明与脚本示例指向 v1.3.2

---

**发布日期**: 2025-11-19  
**作者**: andre.li


