@echo off
echo 正在打包视频裁剪工具为EXE文件...
echo.

REM 检查是否安装了依赖
echo 检查依赖...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    pip install -r requirements.txt
)

echo.
echo 开始打包...
pyinstaller --onefile --windowed --name="视频裁剪工具" --icon=NONE video_clipper.py

echo.
echo 打包完成！
echo EXE文件位于: dist\视频裁剪工具.exe
echo.
pause

