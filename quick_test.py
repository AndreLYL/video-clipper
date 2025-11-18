"""
快速测试脚本 - 测试视频裁剪功能的核心逻辑
"""
import sys
import os
import io

# 设置标准输出为UTF-8编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

from video_clipper import VideoClipperApp
import tkinter as tk


def test_time_parsing():
    """测试时间解析功能"""
    print("测试时间解析功能...")
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    app = VideoClipperApp(root)
    
    test_cases = [
        ("10:00:00", 36000),
        ("00:00:00", 0),
        ("23:59:59", 86399),
        ("01:30:45", 5445),
    ]
    
    all_passed = True
    for time_str, expected_seconds in test_cases:
        try:
            result = app.parse_time(time_str)
            if result == expected_seconds:
                print(f"  ✓ {time_str} -> {result}秒 (正确)")
            else:
                print(f"  ✗ {time_str} -> {result}秒 (期望: {expected_seconds})")
                all_passed = False
        except Exception as e:
            print(f"  ✗ {time_str} 解析失败: {e}")
            all_passed = False
    
    # 测试错误格式
    error_cases = ["25:00:00", "12:60:00", "12:30:60", "12:30", "invalid"]
    print("\n测试错误格式处理...")
    for time_str in error_cases:
        try:
            result = app.parse_time(time_str)
            print(f"  ✗ {time_str} 应该抛出错误但没有")
            all_passed = False
        except ValueError:
            print(f"  ✓ {time_str} 正确抛出错误")
    
    root.destroy()
    return all_passed


def test_seconds_conversion():
    """测试秒数转换为时间格式"""
    print("\n测试秒数转换功能...")
    root = tk.Tk()
    root.withdraw()
    
    app = VideoClipperApp(root)
    
    test_cases = [
        (36000, "10:00:00"),
        (0, "00:00:00"),
        (86399, "23:59:59"),
        (5445, "01:30:45"),
        (3661, "01:01:01"),
    ]
    
    all_passed = True
    for seconds, expected_time in test_cases:
        result = app.seconds_to_time(seconds)
        if result == expected_time:
            print(f"  ✓ {seconds}秒 -> {result} (正确)")
        else:
            print(f"  ✗ {seconds}秒 -> {result} (期望: {expected_time})")
            all_passed = False
    
    root.destroy()
    return all_passed


def test_clip_time_calculation():
    """测试裁剪时间计算"""
    print("\n测试裁剪时间计算...")
    root = tk.Tk()
    root.withdraw()
    
    app = VideoClipperApp(root)
    
    # 测试案例：视频起始时间10:00:00，裁剪时间点10:05:30
    video_start = "10:00:00"
    clip_time = "10:05:30"
    
    video_start_seconds = app.parse_time(video_start)
    clip_time_seconds = app.parse_time(clip_time)
    relative_seconds = clip_time_seconds - video_start_seconds
    
    start_time = relative_seconds - 40  # 前40秒
    end_time = relative_seconds + 20    # 后20秒
    
    expected_start = 290  # 330 - 40
    expected_end = 350    # 330 + 20
    expected_duration = 60
    
    print(f"  视频起始时间: {video_start}")
    print(f"  裁剪时间点: {clip_time}")
    print(f"  相对秒数: {relative_seconds}秒")
    print(f"  裁剪起点: {start_time}秒 (期望: {expected_start})")
    print(f"  裁剪终点: {end_time}秒 (期望: {expected_end})")
    print(f"  裁剪时长: {end_time - start_time}秒 (期望: {expected_duration})")
    
    all_passed = True
    if start_time == expected_start and end_time == expected_end:
        print(f"  ✓ 裁剪时间计算正确")
    else:
        print(f"  ✗ 裁剪时间计算错误")
        all_passed = False
    
    root.destroy()
    return all_passed


def main():
    """运行所有测试"""
    print("=" * 60)
    print("视频裁剪工具 - 功能测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("时间解析", test_time_parsing()))
    results.append(("秒数转换", test_seconds_conversion()))
    results.append(("裁剪时间计算", test_clip_time_calculation()))
    
    # 显示结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("所有测试通过！✓")
    else:
        print("部分测试失败！✗")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

