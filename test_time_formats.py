#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试多种时间格式解析功能
"""

import sys
import io
import re

# Windows控制台UTF-8编码修复
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def parse_flexible_time(time_str):
    """
    解析多种时间格式，返回秒数
    """
    time_str = time_str.strip()
    
    # 格式1: HH:MM:SS
    if re.match(r'^\d{1,2}:\d{2}:\d{2}$', time_str):
        parts = time_str.split(":")
        hours, minutes, seconds = map(int, parts)
        if not (0 <= hours <= 23):
            raise ValueError("小时必须在 0-23 之间")
        if not (0 <= minutes <= 59):
            raise ValueError("分钟必须在 0-59 之间")
        if not (0 <= seconds <= 59):
            raise ValueError("秒必须在 0-59 之间")
        return hours * 3600 + minutes * 60 + seconds
    
    # 格式2: YYYY-MM-DD HH:MM:SS
    match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})$', time_str)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        if not (0 <= hour <= 23):
            raise ValueError("小时必须在 0-23 之间")
        if not (0 <= minute <= 59):
            raise ValueError("分钟必须在 0-59 之间")
        if not (0 <= second <= 59):
            raise ValueError("秒必须在 0-59 之间")
        return hour * 3600 + minute * 60 + second
    
    # 格式3: YYYY年MM月DD日HH:MM:SS
    match = re.match(r'^(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}):(\d{2}):(\d{2})$', time_str)
    if match:
        year, month, day, hour, minute, second = map(int, match.groups())
        if not (0 <= hour <= 23):
            raise ValueError("小时必须在 0-23 之间")
        if not (0 <= minute <= 59):
            raise ValueError("分钟必须在 0-59 之间")
        if not (0 <= second <= 59):
            raise ValueError("秒必须在 0-59 之间")
        return hour * 3600 + minute * 60 + second
    
    # 格式4: HH点MM分SS秒
    match = re.match(r'^(\d{1,2})点(\d{1,2})分(\d{1,2})秒$', time_str)
    if match:
        hour, minute, second = map(int, match.groups())
        if not (0 <= hour <= 23):
            raise ValueError("小时必须在 0-23 之间")
        if not (0 <= minute <= 59):
            raise ValueError("分钟必须在 0-59 之间")
        if not (0 <= second <= 59):
            raise ValueError("秒必须在 0-59 之间")
        return hour * 3600 + minute * 60 + second
    
    raise ValueError(f"不支持的时间格式: {time_str}")

def seconds_to_time(seconds):
    """将秒数转换为HH:MM:SS格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def run_tests():
    """运行测试用例"""
    test_cases = [
        # 格式1: HH:MM:SS
        ("12:30:45", 45045, "HH:MM:SS"),
        ("00:00:00", 0, "HH:MM:SS - 零点"),
        ("23:59:59", 86399, "HH:MM:SS - 最大值"),
        
        # 格式2: YYYY-MM-DD HH:MM:SS
        ("2025-11-13 00:26:39", 1599, "YYYY-MM-DD HH:MM:SS"),
        ("2025-11-13 12:00:00", 43200, "YYYY-MM-DD HH:MM:SS - 中午"),
        
        # 格式3: YYYY年MM月DD日HH:MM:SS
        ("2025年11月13日00:26:50", 1610, "YYYY年MM月DD日HH:MM:SS"),
        ("2025年1月1日08:30:15", 30615, "YYYY年MM月DD日HH:MM:SS - 单数月日"),
        
        # 格式4: HH点MM分SS秒
        ("00点34分20秒", 2060, "HH点MM分SS秒"),
        ("12点0分0秒", 43200, "HH点MM分SS秒 - 整点"),
        ("23点59分59秒", 86399, "HH点MM分SS秒 - 最大值"),
    ]
    
    print("=" * 80)
    print("时间格式解析功能测试")
    print("=" * 80)
    print()
    
    passed = 0
    failed = 0
    
    for time_str, expected_seconds, description in test_cases:
        try:
            result = parse_flexible_time(time_str)
            if result == expected_seconds:
                print(f"✓ 通过: {description}")
                print(f"  输入: {time_str}")
                print(f"  结果: {result}秒 ({seconds_to_time(result)})")
                passed += 1
            else:
                print(f"✗ 失败: {description}")
                print(f"  输入: {time_str}")
                print(f"  期望: {expected_seconds}秒, 实际: {result}秒")
                failed += 1
        except Exception as e:
            print(f"✗ 异常: {description}")
            print(f"  输入: {time_str}")
            print(f"  错误: {str(e)}")
            failed += 1
        print()
    
    # 测试错误格式
    print("=" * 80)
    print("错误格式测试（应该抛出异常）")
    print("=" * 80)
    print()
    
    invalid_cases = [
        "25:00:00",  # 小时超范围
        "12:60:00",  # 分钟超范围
        "12:30:60",  # 秒超范围
        "invalid",   # 无效格式
        "12-30-45",  # 错误分隔符
    ]
    
    for time_str in invalid_cases:
        try:
            result = parse_flexible_time(time_str)
            print(f"✗ 失败: 应该抛出异常但没有 - {time_str}")
            failed += 1
        except ValueError as e:
            print(f"✓ 通过: 正确抛出异常 - {time_str}")
            print(f"  错误信息: {str(e)}")
            passed += 1
        print()
    
    # 总结
    print("=" * 80)
    print(f"测试完成: 通过 {passed}, 失败 {failed}")
    print("=" * 80)
    
    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)

