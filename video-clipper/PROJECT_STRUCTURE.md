# 视频剪辑工具项目结构

## 📁 目录说明

本项目已整理到 `video-clipper/` 文件夹下，与其他项目（如 `DressingStyle/`）分离。

## 📂 文件结构

```
video-clipper/
├── video_clipper.py          # 主程序文件
├── VideoClipper.spec         # PyInstaller配置文件
├── file_version_info.txt     # 版本信息文件
├── requirements.txt          # Python依赖
├── build.bat                 # 构建脚本
├── README.md                 # 项目说明
├── .gitignore                # Git忽略配置
│
├── dist/                     # 生成的EXE文件目录
│   └── VideoClipper_v1.3.0.exe
│
├── build/                    # PyInstaller构建临时文件
│
├── 文档/
│   ├── RELEASE_NOTES_*.md    # 发布说明
│   ├── CHANGELOG_*.md        # 更新日志
│   └── timestamp_example.txt # 时间戳文件示例
│
└── 测试文件/
    ├── test_*.py             # 测试脚本
    └── test_*.txt            # 测试数据
```

## 🔧 Git配置

- 根目录 `.gitignore`：通用配置，适用于所有子项目
- `video-clipper/.gitignore`：视频剪辑工具专用配置
  - 忽略 `build/` 和 `dist/*.exe`（文件过大）
  - 忽略临时测试文件
  - 忽略Python缓存文件

## 📝 使用说明

1. **开发环境**：
   ```bash
   cd video-clipper
   pip install -r requirements.txt
   python video_clipper.py
   ```

2. **构建EXE**：
   ```bash
   cd video-clipper
   pyinstaller VideoClipper.spec --clean
   ```

3. **发布**：
   - EXE文件通过GitHub Release发布
   - 不提交到Git仓库（文件过大）

## 🔗 相关链接

- GitHub仓库: https://github.com/AndreLYL/video-clipper
- 最新Release: https://github.com/AndreLYL/video-clipper/releases/tag/v1.3.0

