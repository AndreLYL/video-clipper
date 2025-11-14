"""
测试视频生成器
用于生成一个带有时间标记的测试视频，方便测试视频裁剪功能
"""
import numpy as np
from moviepy.editor import VideoClip, TextClip, CompositeVideoClip
from datetime import datetime, timedelta
import os


def make_frame(t):
    """生成每一帧的图像"""
    # 创建一个简单的渐变背景
    size = (640, 480)
    # 创建渐变色
    color_value = int(128 + 127 * np.sin(t / 5))
    frame = np.ones((size[1], size[0], 3), dtype=np.uint8) * color_value
    return frame


def create_test_video(output_path="test_video.mp4", duration=300, start_time_str="10:00:00"):
    """
    创建一个测试视频
    
    参数:
        output_path: 输出文件路径
        duration: 视频时长（秒）
        start_time_str: 视频起始UTC时间 (HH:MM:SS)
    """
    print(f"正在生成测试视频...")
    print(f"时长: {duration}秒 ({duration//60}分钟)")
    print(f"起始时间: {start_time_str}")
    
    # 解析起始时间
    start_time = datetime.strptime(start_time_str, "%H:%M:%S")
    
    # 创建基础视频
    video = VideoClip(make_frame, duration=duration)
    
    # 创建时间文本列表
    text_clips = []
    
    # 每5秒添加一个时间标记
    for t in range(0, duration, 5):
        current_time = start_time + timedelta(seconds=t)
        time_text = current_time.strftime("%H:%M:%S")
        
        # 创建文本
        txt_clip = TextClip(
            f"UTC: {time_text}\n相对时间: {t}秒",
            fontsize=40,
            color='white',
            bg_color='black',
            size=(400, 100),
            method='caption'
        )
        txt_clip = txt_clip.set_position('center').set_start(t).set_duration(5)
        text_clips.append(txt_clip)
    
    # 合成视频
    final_video = CompositeVideoClip([video] + text_clips)
    
    # 写入文件
    print("正在写入视频文件...")
    final_video.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio=False
    )
    
    print(f"测试视频已生成: {output_path}")
    print(f"\n建议的裁剪时间点:")
    
    # 生成一些建议的裁剪时间点
    test_times = [60, 120, 180, 240]
    for t in test_times:
        if t < duration:
            current_time = start_time + timedelta(seconds=t)
            print(f"  {current_time.strftime('%H:%M:%S')} (相对时间: {t}秒)")


if __name__ == "__main__":
    # 生成一个5分钟的测试视频，起始时间为10:00:00
    create_test_video(
        output_path="test_video.mp4",
        duration=300,  # 5分钟
        start_time_str="10:00:00"
    )
    
    # 创建对应的时间戳文件
    with open("test_timestamps.txt", "w", encoding="utf-8") as f:
        f.write("# 测试时间戳文件\n")
        f.write("# 视频起始时间: 10:00:00\n\n")
        f.write("10:01:00 第一个测试点\n")
        f.write("10:02:00 第二个测试点\n")
        f.write("10:03:00 第三个测试点\n")
        f.write("10:04:00 第四个测试点\n")
    
    print("\n测试时间戳文件已生成: test_timestamps.txt")

