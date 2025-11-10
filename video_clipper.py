"""
视频裁剪软件
支持单点裁剪和批量裁剪模式
版本: 1.0.0
作者: andre.li
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta
import threading
from moviepy.editor import VideoFileClip
from pathlib import Path


class VideoClipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频裁剪工具 v1.0.0")
        self.root.geometry("900x750")
        self.root.minsize(850, 700)  # 设置最小窗口尺寸
        self.root.resizable(True, True)
        
        # 深色主题配色
        self.colors = {
            'bg': '#1a1a1a',           # 深色背景
            'card_bg': '#2d2d2d',      # 卡片背景
            'accent': '#4fd1c5',       # 青色强调色
            'accent_hover': '#38b2ac', # 悬停色
            'text': '#e2e8f0',         # 主文字
            'text_secondary': '#a0aec0',# 次要文字
            'border': '#4a5568',       # 边框色
            'success': '#48bb78',      # 成功绿色
            'warning': '#ed8936',      # 警告橙色
            'danger': '#f56565'        # 危险红色
        }
        
        # 设置窗口背景
        self.root.configure(bg=self.colors['bg'])
        
        # 变量
        self.source_video = tk.StringVar()
        self.target_directory = tk.StringVar()
        self.mode = tk.StringVar(value="single")
        self.video_start_time = tk.StringVar(value="00:00:00")
        self.clip_time = tk.StringVar(value="00:00:00")
        self.timestamp_file = tk.StringVar()
        self.before_seconds = tk.StringVar(value="40")  # 向前裁剪秒数
        self.after_seconds = tk.StringVar(value="20")   # 向后裁剪秒数
        
        self.create_widgets()
        
    def create_modern_card(self, parent, **kwargs):
        """创建现代化卡片容器"""
        card = tk.Frame(parent, 
                       bg=self.colors['card_bg'],
                       highlightbackground=self.colors['border'],
                       highlightthickness=1,
                       **kwargs)
        return card
    
    def create_widgets(self):
        # 顶部标题栏
        header = tk.Frame(self.root, bg=self.colors['bg'])
        header.pack(fill=tk.X, padx=15, pady=(8, 3))
        
        # 标题
        title_label = tk.Label(header, 
                              text="视频裁剪工具", 
                              font=("Microsoft YaHei UI", 14, "bold"), 
                              bg=self.colors['bg'], 
                              fg=self.colors['text'])
        title_label.pack(side=tk.LEFT)
        
        # 版本标签
        version_label = tk.Label(header,
                                text="v1.0.0",
                                font=("Microsoft YaHei UI", 8),
                                bg=self.colors['accent'],
                                fg='white',
                                padx=4, pady=1)
        version_label.pack(side=tk.LEFT, padx=5)
        
        # 作者信息
        author_label = tk.Label(header,
                               text="by andre.li",
                               font=("Microsoft YaHei UI", 8),
                               bg=self.colors['bg'],
                               fg=self.colors['text_secondary'])
        author_label.pack(side=tk.LEFT, padx=8)
        
        # 帮助按钮 - 右上角
        help_button = tk.Button(header, 
                               text="❓ 帮助", 
                               command=self.show_help,
                               bg=self.colors['card_bg'], 
                               fg=self.colors['text'], 
                               font=("Microsoft YaHei UI", 10),
                               relief=tk.FLAT,
                               cursor="hand2",
                               padx=10, 
                               pady=4)
        help_button.pack(side=tk.RIGHT)
        
        # 创建主容器 - 直接显示，不使用滚动条
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 8))
        
        # ===== 文件选择卡片 =====
        file_card = self.create_modern_card(main_frame, padx=12, pady=6)
        file_card.pack(fill=tk.X, pady=(0, 6))
        
        tk.Label(file_card, text="📁 文件选择", 
                font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor="w", pady=(0, 4))
        
        # 源视频 - 单行布局
        video_frame = tk.Frame(file_card, bg=self.colors['card_bg'])
        video_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(video_frame, text="源视频", 
                font=("Microsoft YaHei UI", 10),
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary'],
                width=8).pack(side=tk.LEFT, padx=(0,5))
        
        video_entry = tk.Entry(video_frame, textvariable=self.source_video,
                              font=("Microsoft YaHei UI", 10),
                              bg='#3a3a3a', fg=self.colors['text'],
                              relief=tk.FLAT, insertbackground=self.colors['accent'])
        video_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, ipadx=8)
        
        browse_btn = tk.Button(video_frame, text="浏览",
                              command=self.browse_source_video,
                              bg=self.colors['accent'], fg='white',
                              font=("Microsoft YaHei UI", 9, "bold"),
                              relief=tk.FLAT, cursor="hand2",
                              padx=15, pady=5)
        browse_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # 目标目录 - 单行布局
        target_frame = tk.Frame(file_card, bg=self.colors['card_bg'])
        target_frame.pack(fill=tk.X, pady=2)
        
        tk.Label(target_frame, text="保存目录", 
                font=("Microsoft YaHei UI", 10),
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary'],
                width=8).pack(side=tk.LEFT, padx=(0,5))
        
        target_entry = tk.Entry(target_frame, textvariable=self.target_directory,
                               font=("Microsoft YaHei UI", 10),
                               bg='#3a3a3a', fg=self.colors['text'],
                               relief=tk.FLAT, insertbackground=self.colors['accent'])
        target_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, ipadx=8)
        
        target_btn = tk.Button(target_frame, text="浏览",
                              command=self.browse_target_directory,
                              bg=self.colors['accent'], fg='white',
                              font=("Microsoft YaHei UI", 9, "bold"),
                              relief=tk.FLAT, cursor="hand2",
                              padx=15, pady=5)
        target_btn.pack(side=tk.RIGHT, padx=(8, 0))
        
        # ===== 裁剪模式卡片 =====
        mode_card = self.create_modern_card(main_frame, padx=12, pady=8)
        mode_card.pack(fill=tk.X, pady=(0, 6))
        
        tk.Label(mode_card, text="⚙️ 裁剪模式", 
                font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor="w", pady=(0, 6))
        
        # 模式选择按钮 - 横向平铺
        mode_btn_frame = tk.Frame(mode_card, bg=self.colors['card_bg'])
        mode_btn_frame.pack(fill=tk.X)
        
        tk.Radiobutton(mode_btn_frame, text="  单点裁剪", variable=self.mode, 
                      value="single", command=self.update_mode,
                      font=("Microsoft YaHei UI", 10),
                      bg=self.colors['card_bg'], fg=self.colors['text'],
                      selectcolor=self.colors['card_bg'],
                      activebackground=self.colors['card_bg'],
                      activeforeground=self.colors['accent'],
                      cursor="hand2").pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(mode_btn_frame, text="  批量裁剪", variable=self.mode, 
                      value="batch", command=self.update_mode,
                      font=("Microsoft YaHei UI", 10),
                      bg=self.colors['card_bg'], fg=self.colors['text'],
                      selectcolor=self.colors['card_bg'],
                      activebackground=self.colors['card_bg'],
                      activeforeground=self.colors['accent'],
                      cursor="hand2").pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(mode_btn_frame, text="  自动裁剪（预留功能）", variable=self.mode, 
                      value="auto", state="disabled",
                      font=("Microsoft YaHei UI", 10),
                      bg=self.colors['card_bg'], fg=self.colors['text_secondary'],
                      selectcolor=self.colors['card_bg']).pack(side=tk.LEFT)
        
        # ===== 裁剪参数卡片 =====
        self.params_card = self.create_modern_card(main_frame, padx=12, pady=8)
        self.params_card.pack(fill=tk.X, pady=(0, 6))
        
        tk.Label(self.params_card, text="🎬 裁剪参数", 
                font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor="w", pady=(0, 6))
        
        # 创建参数内容容器
        self.params_content = tk.Frame(self.params_card, bg=self.colors['card_bg'])
        self.params_content.pack(fill=tk.X)
        
        # 视频起始时间和裁剪时长配置 - 合并为一行
        start_time_frame = tk.Frame(self.params_content, bg=self.colors['card_bg'])
        start_time_frame.pack(fill=tk.X, pady=3)
        
        tk.Label(start_time_frame, text="视频起始时间 (UTC)", 
                font=("Microsoft YaHei UI", 10),
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor="w")
        
        start_time_input = tk.Frame(start_time_frame, bg=self.colors['card_bg'])
        start_time_input.pack(fill=tk.X, pady=(5, 0))
        
        # 起始时间输入框
        tk.Entry(start_time_input, textvariable=self.video_start_time, 
                width=12, font=("Consolas", 11),
                bg='#3a3a3a', fg=self.colors['accent'],
                relief=tk.FLAT, insertbackground=self.colors['accent'],
                justify='center').pack(side=tk.LEFT, ipady=5, ipadx=8)
        
        # 分隔线
        tk.Label(start_time_input, text="丨", 
                font=("Microsoft YaHei UI", 10),
                bg=self.colors['card_bg'],
                fg=self.colors['border']).pack(side=tk.LEFT, padx=15)
        
        # 向前裁剪
        tk.Label(start_time_input, text="向前", 
                font=("Microsoft YaHei UI", 9),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        tk.Entry(start_time_input, textvariable=self.before_seconds, 
                width=5, font=("Consolas", 11),
                bg='#3a3a3a', fg=self.colors['accent'],
                relief=tk.FLAT, insertbackground=self.colors['accent'],
                justify='center').pack(side=tk.LEFT, ipady=4, ipadx=5, padx=(5, 3))
        
        tk.Label(start_time_input, text="秒", 
                font=("Microsoft YaHei UI", 9),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT, padx=(0, 12))
        
        # 向后裁剪
        tk.Label(start_time_input, text="向后", 
                font=("Microsoft YaHei UI", 9),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        tk.Entry(start_time_input, textvariable=self.after_seconds, 
                width=5, font=("Consolas", 11),
                bg='#3a3a3a', fg=self.colors['accent'],
                relief=tk.FLAT, insertbackground=self.colors['accent'],
                justify='center').pack(side=tk.LEFT, ipady=4, ipadx=5, padx=(5, 3))
        
        tk.Label(start_time_input, text="秒", 
                font=("Microsoft YaHei UI", 9),
                bg=self.colors['card_bg'],
                fg=self.colors['text_secondary']).pack(side=tk.LEFT)
        
        # 单点裁剪时间
        self.clip_time_frame = tk.Frame(self.params_content, bg=self.colors['card_bg'])
        self.clip_time_frame.pack(fill=tk.X, pady=3)
        
        self.clip_time_label = tk.Label(self.clip_time_frame, text="裁剪时间点", 
                                        font=("Microsoft YaHei UI", 10),
                                        bg=self.colors['card_bg'], 
                                        fg=self.colors['text_secondary'])
        self.clip_time_label.pack(anchor="w")
        
        clip_time_input = tk.Frame(self.clip_time_frame, bg=self.colors['card_bg'])
        clip_time_input.pack(fill=tk.X, pady=(5, 0))
        
        self.clip_time_entry = tk.Entry(clip_time_input, textvariable=self.clip_time, 
                                        width=12, font=("Consolas", 11),
                                        bg='#3a3a3a', fg=self.colors['accent'],
                                        relief=tk.FLAT, insertbackground=self.colors['accent'],
                                        justify='center')
        self.clip_time_entry.pack(side=tk.LEFT, ipady=5, ipadx=8)
        
        # 批量裁剪文件选择
        self.timestamp_frame = tk.Frame(self.params_content, bg=self.colors['card_bg'])
        self.timestamp_frame.pack(fill=tk.X, pady=3)
        
        self.timestamp_file_label = tk.Label(self.timestamp_frame, text="时间戳文件", 
                                            font=("Microsoft YaHei UI", 10),
                                            bg=self.colors['card_bg'], 
                                            fg=self.colors['text_secondary'])
        self.timestamp_file_label.pack(anchor="w")
        
        timestamp_input_frame = tk.Frame(self.timestamp_frame, bg=self.colors['card_bg'])
        timestamp_input_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.timestamp_file_entry = tk.Entry(timestamp_input_frame, 
                                             textvariable=self.timestamp_file,
                                             font=("Microsoft YaHei UI", 10),
                                             bg='#3a3a3a', fg=self.colors['text'],
                                             relief=tk.FLAT, insertbackground=self.colors['accent'])
        self.timestamp_file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, ipadx=10)
        
        self.timestamp_file_button = tk.Button(timestamp_input_frame, text="选择文件", 
                                              command=self.browse_timestamp_file,
                                              bg=self.colors['accent'], fg='white',
                                              font=("Microsoft YaHei UI", 10, "bold"),
                                              relief=tk.FLAT, cursor="hand2",
                                              padx=20, pady=8)
        self.timestamp_file_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # ===== 操作按钮 =====
        button_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=6)
        
        # 开始裁剪按钮
        self.start_button = tk.Button(button_frame, 
                                     text="▶  开始裁剪", 
                                     command=self.start_clipping,
                                     bg=self.colors['accent'], 
                                     fg='white', 
                                     font=("Microsoft YaHei UI", 13, "bold"),
                                     relief=tk.FLAT,
                                     cursor="hand2",
                                     padx=25, 
                                     pady=10,
                                     borderwidth=0)
        self.start_button.pack(fill=tk.X, ipady=3)
        
        # 添加悬停效果
        def on_enter(e):
            self.start_button['bg'] = self.colors['accent_hover']
        def on_leave(e):
            self.start_button['bg'] = self.colors['accent']
        self.start_button.bind("<Enter>", on_enter)
        self.start_button.bind("<Leave>", on_leave)
        
        # 退出按钮 - 灰色
        exit_button = tk.Button(button_frame, 
                               text="退出程序", 
                               command=self.root.quit,
                               bg='#4a5568', 
                               fg=self.colors['text'], 
                               font=("Microsoft YaHei UI", 10),
                               relief=tk.FLAT,
                               cursor="hand2",
                               padx=20, 
                               pady=6)
        exit_button.pack(fill=tk.X, pady=(6, 0))
        
        # ===== 进度显示卡片 =====
        progress_card = self.create_modern_card(main_frame, padx=12, pady=8)
        progress_card.pack(fill=tk.X, pady=(0, 6))
        
        tk.Label(progress_card, text="📊 处理状态", 
                font=("Microsoft YaHei UI", 11, "bold"),
                bg=self.colors['card_bg'], 
                fg=self.colors['text']).pack(anchor="w", pady=(0, 6))
        
        self.progress_label = tk.Label(progress_card, text="就绪", 
                                       font=("Microsoft YaHei UI", 10),
                                       bg=self.colors['card_bg'],
                                       fg=self.colors['accent'])
        self.progress_label.pack(anchor="w", pady=(0, 6))
        
        # 自定义进度条样式
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Horizontal.TProgressbar",
                       troughcolor='#3a3a3a',
                       background=self.colors['accent'],
                       bordercolor=self.colors['card_bg'],
                       lightcolor=self.colors['accent'],
                       darkcolor=self.colors['accent'])
        
        self.progress_bar = ttk.Progressbar(progress_card, 
                                          mode='indeterminate',
                                          style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(fill=tk.X, pady=(0, 5), ipady=5)
        
        # 初始化界面
        self.update_mode()
    
    def browse_source_video(self):
        filename = filedialog.askopenfilename(
            title="选择源视频文件",
            filetypes=[("视频文件", "*.mp4 *.avi *.mov *.mkv *.flv"), ("所有文件", "*.*")]
        )
        if filename:
            self.source_video.set(filename)
    
    def browse_target_directory(self):
        directory = filedialog.askdirectory(title="选择目标目录")
        if directory:
            self.target_directory.set(directory)
    
    def browse_timestamp_file(self):
        filename = filedialog.askopenfilename(
            title="选择时间戳文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        if filename:
            self.timestamp_file.set(filename)
    
    def show_help(self):
        """显示帮助信息对话框"""
        help_window = tk.Toplevel(self.root)
        help_window.title("使用帮助")
        help_window.geometry("600x400")
        help_window.configure(bg=self.colors['bg'])
        help_window.resizable(False, False)
        
        # 标题
        tk.Label(help_window, text="💡 使用说明", 
                font=("Microsoft YaHei UI", 14, "bold"),
                bg=self.colors['bg'], 
                fg=self.colors['text']).pack(pady=(20, 10))
        
        # 说明内容
        help_card = self.create_modern_card(help_window, padx=20, pady=15)
        help_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        help_texts = [
            "基本功能",
            "• 裁剪时长: 可配置向前和向后裁剪的秒数",
            "• 默认: 时间点前40秒到后20秒(共60秒)",
            "• 输出文件名: 使用时间戳自动命名",
            "",
            "单点裁剪模式",
            "• 输入视频起始UTC时间",
            "• 配置向前/向后裁剪秒数",
            "• 输入想要裁剪的时间点",
            "• 时间格式: HH:MM:SS (例如: 12:30:45)",
            "",
            "批量裁剪模式",
            "• 输入视频起始UTC时间",
            "• 配置向前/向后裁剪秒数",
            "• 选择时间戳文本文件",
            "• 文件格式: 每行一个时间点",
            "  格式: HH:MM:SS 描述",
            "  示例: 12:30:45 第一个片段",
            "• 支持 # 开头的注释行",
            "",
            "注意事项",
            "• 裁剪时长必须是正整数",
            "• 确保视频时长足够进行裁剪",
            "• 裁剪时间不能超出视频范围",
            "• 处理过程中请勿关闭程序"
        ]
        
        for text in help_texts:
            if text and not text.startswith("•"):
                # 标题
                tk.Label(help_card, text=text, 
                        font=("Microsoft YaHei UI", 11, "bold"),
                        bg=self.colors['card_bg'], 
                        fg=self.colors['accent'],
                        anchor="w").pack(anchor="w", pady=(8, 2))
            else:
                # 内容
                tk.Label(help_card, text=text, 
                        font=("Microsoft YaHei UI", 10),
                        bg=self.colors['card_bg'], 
                        fg=self.colors['text_secondary'],
                        anchor="w").pack(anchor="w", pady=1)
        
        # 关闭按钮
        close_btn = tk.Button(help_window, text="关闭", 
                             command=help_window.destroy,
                             bg=self.colors['accent'], 
                             fg='white',
                             font=("Microsoft YaHei UI", 10, "bold"),
                             relief=tk.FLAT, cursor="hand2",
                             padx=30, pady=8)
        close_btn.pack(pady=(0, 20))
    
    def update_mode(self):
        mode = self.mode.get()
        
        if mode == "single":
            # 显示单点裁剪控件
            self.clip_time_frame.pack(fill=tk.X, pady=8)
            # 隐藏批量裁剪控件
            self.timestamp_frame.pack_forget()
        elif mode == "batch":
            # 隐藏单点裁剪控件
            self.clip_time_frame.pack_forget()
            # 显示批量裁剪控件
            self.timestamp_frame.pack(fill=tk.X, pady=8)
    
    def parse_time(self, time_str):
        """将HH:MM:SS格式转换为秒数"""
        try:
            parts = time_str.strip().split(":")
            if len(parts) != 3:
                raise ValueError("时间格式必须为 HH:MM:SS")
            
            hours, minutes, seconds = map(int, parts)
            
            # 验证时间范围
            if not (0 <= hours <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minutes <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            if not (0 <= seconds <= 59):
                raise ValueError("秒必须在 0-59 之间")
            
            return hours * 3600 + minutes * 60 + seconds
        except ValueError as e:
            if "invalid literal" in str(e):
                raise ValueError(f"时间格式错误: {time_str}")
            raise ValueError(f"时间格式错误 ({time_str}): {str(e)}")
        except:
            raise ValueError(f"时间格式错误: {time_str}")
    
    def seconds_to_time(self, seconds):
        """将秒数转换为HH:MM:SS格式"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    
    def get_video_duration(self, video_path):
        """获取视频时长（秒）"""
        video = None
        try:
            video = VideoFileClip(video_path)
            duration = video.duration
            return duration
        finally:
            if video is not None:
                video.close()
    
    def clip_video(self, video_path, start_time, end_time, output_path):
        """裁剪视频片段"""
        video = None
        clip = None
        try:
            video = VideoFileClip(video_path)
            video_duration = video.duration
            
            # 详细的时间范围检查
            if start_time < 0:
                raise ValueError(f"裁剪起始时间不能为负数（当前: {start_time:.1f}秒）")
            
            if start_time >= video_duration:
                raise ValueError(
                    f"裁剪起始时间超出视频范围\n"
                    f"视频总时长: {self.seconds_to_time(video_duration)} ({video_duration:.1f}秒)\n"
                    f"裁剪起始点: {self.seconds_to_time(start_time)} ({start_time:.1f}秒)"
                )
            
            if end_time > video_duration:
                raise ValueError(
                    f"裁剪结束时间超出视频范围\n"
                    f"视频总时长: {self.seconds_to_time(video_duration)} ({video_duration:.1f}秒)\n"
                    f"裁剪结束点: {self.seconds_to_time(end_time)} ({end_time:.1f}秒)\n"
                    f"建议: 选择更早的时间点，或视频长度需要至少 {self.seconds_to_time(end_time)}"
                )
            
            if start_time >= end_time:
                raise ValueError(
                    f"裁剪起始时间必须早于结束时间\n"
                    f"起始: {self.seconds_to_time(start_time)}\n"
                    f"结束: {self.seconds_to_time(end_time)}"
                )
            
            # 裁剪视频
            clip = video.subclip(start_time, end_time)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac", 
                               logger=None, verbose=False)
            
        finally:
            # 确保资源被释放
            if clip is not None:
                clip.close()
            if video is not None:
                video.close()
    
    def update_progress(self, text):
        """线程安全地更新进度标签"""
        self.root.after(0, lambda: self.progress_label.config(text=text))
    
    def process_single_clip(self):
        """处理单点裁剪"""
        video_path = self.source_video.get()
        target_dir = self.target_directory.get()
        video_start = self.video_start_time.get()
        clip_time_str = self.clip_time.get()
        
        # 验证输入
        if not video_path or not os.path.exists(video_path):
            self.root.after(0, lambda: messagebox.showerror("错误", "请选择有效的源视频文件"))
            return
        
        if not target_dir:
            self.root.after(0, lambda: messagebox.showerror("错误", "请选择目标目录"))
            return
        
        # 创建目标目录
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # 解析时间
            video_start_seconds = self.parse_time(video_start)
            clip_time_seconds = self.parse_time(clip_time_str)
            
            # 获取用户配置的裁剪时长
            try:
                before_sec = int(self.before_seconds.get())
                after_sec = int(self.after_seconds.get())
                if before_sec < 0 or after_sec < 0:
                    raise ValueError("裁剪时长不能为负数")
            except ValueError:
                raise ValueError("裁剪时长必须是正整数")
            
            # 计算相对于视频开始的秒数
            relative_seconds = clip_time_seconds - video_start_seconds
            
            if relative_seconds < 0:
                raise ValueError("裁剪时间点早于视频起始时间")
            
            # 计算裁剪的起止时间(使用用户配置的时长)
            start_time = relative_seconds - before_sec
            end_time = relative_seconds + after_sec
            
            # 预先检查视频时长
            self.update_progress("正在检查视频...")
            self.root.after(0, lambda: self.progress_bar.start())
            
            video_duration = self.get_video_duration(video_path)
            
            # 验证裁剪范围
            if start_time < 0:
                raise ValueError(
                    f"裁剪时间点太早！\n\n"
                    f"裁剪时间点: {clip_time_str}\n"
                    f"需要前{before_sec}秒，但视频从 {video_start} 开始\n"
                    f"建议: 选择 {self.seconds_to_time(video_start_seconds + before_sec)} 之后的时间点"
                )
            
            if end_time > video_duration:
                raise ValueError(
                    f"裁剪时间点太晚！\n\n"
                    f"视频总时长: {self.seconds_to_time(video_duration)}\n"
                    f"裁剪时间点: {clip_time_str}\n"
                    f"需要后{after_sec}秒，但视频只到 {self.seconds_to_time(video_start_seconds + video_duration)}\n"
                    f"建议: 选择 {self.seconds_to_time(video_start_seconds + video_duration - after_sec)} 之前的时间点"
                )
            
            # 生成输出文件名
            output_filename = f"{clip_time_str.replace(':', '-')}.mp4"
            output_path = os.path.join(target_dir, output_filename)
            
            self.update_progress(f"正在裁剪: {clip_time_str}")
            self.root.after(0, lambda: self.progress_bar.start())
            
            # 裁剪视频
            self.clip_video(video_path, start_time, end_time, output_path)
            
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress("裁剪完成!")
            self.root.after(0, lambda: messagebox.showinfo("成功", f"视频已成功裁剪并保存到:\n{output_path}"))
            
        except ValueError as e:
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress("就绪")
            self.root.after(0, lambda: messagebox.showerror("错误", str(e)))
        except Exception as e:
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress("就绪")
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("错误", f"裁剪失败: {error_msg}"))
    
    def process_batch_clip(self):
        """处理批量裁剪"""
        video_path = self.source_video.get()
        target_dir = self.target_directory.get()
        video_start = self.video_start_time.get()
        timestamp_file = self.timestamp_file.get()
        
        # 验证输入
        if not video_path or not os.path.exists(video_path):
            self.root.after(0, lambda: messagebox.showerror("错误", "请选择有效的源视频文件"))
            return
        
        if not target_dir:
            self.root.after(0, lambda: messagebox.showerror("错误", "请选择目标目录"))
            return
        
        if not timestamp_file or not os.path.exists(timestamp_file):
            self.root.after(0, lambda: messagebox.showerror("错误", "请选择有效的时间戳文件"))
            return
        
        # 创建目标目录
        Path(target_dir).mkdir(parents=True, exist_ok=True)
        
        try:
            # 获取用户配置的裁剪时长
            try:
                before_sec = int(self.before_seconds.get())
                after_sec = int(self.after_seconds.get())
                if before_sec < 0 or after_sec < 0:
                    raise ValueError("裁剪时长不能为负数")
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("错误", "裁剪时长必须是正整数"))
                return
            
            # 解析视频起始时间
            video_start_seconds = self.parse_time(video_start)
            
            # 读取时间戳文件
            with open(timestamp_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            timestamps = []
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith('#'):  # 支持空行和注释
                    continue
                # 解析格式: HH:MM:SS 描述
                parts = line.split(maxsplit=1)
                if len(parts) >= 1:
                    time_str = parts[0]
                    description = parts[1] if len(parts) > 1 else ""
                    timestamps.append((time_str, description, line_num))
            
            if not timestamps:
                self.root.after(0, lambda: messagebox.showerror("错误", "时间戳文件中没有有效的时间点"))
                return
            
            # 预先检查视频时长
            self.update_progress("正在检查视频时长...")
            self.root.after(0, lambda: self.progress_bar.start())
            video_duration = self.get_video_duration(video_path)
            
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress(f"视频时长: {self.seconds_to_time(video_duration)}, 共{len(timestamps)}个裁剪点")
            
            success_count = 0
            failed_items = []
            
            for i, (time_str, description, line_num) in enumerate(timestamps):
                try:
                    # 解析时间
                    clip_time_seconds = self.parse_time(time_str)
                    
                    # 计算相对于视频开始的秒数
                    relative_seconds = clip_time_seconds - video_start_seconds
                    
                    if relative_seconds < 0:
                        failed_items.append(f"第{line_num}行: {time_str} - 时间点早于视频起始时间")
                        continue
                    
                    # 计算裁剪的起止时间(使用用户配置的时长)
                    start_time = relative_seconds - before_sec
                    end_time = relative_seconds + after_sec
                    
                    # 检查时间范围
                    if start_time < 0:
                        failed_items.append(f"第{line_num}行: {time_str} - 时间点太早（需要前{before_sec}秒）")
                        continue
                    
                    if end_time > video_duration:
                        failed_items.append(f"第{line_num}行: {time_str} - 时间点太晚（需要后{after_sec}秒，视频时长{self.seconds_to_time(video_duration)}）")
                        continue
                    
                    # 生成输出文件名
                    safe_desc = "".join(c for c in description if c.isalnum() or c in (' ', '-', '_')).strip()
                    if safe_desc:
                        output_filename = f"{time_str.replace(':', '-')}_{safe_desc}.mp4"
                    else:
                        output_filename = f"{time_str.replace(':', '-')}.mp4"
                    output_path = os.path.join(target_dir, output_filename)
                    
                    self.update_progress(f"正在裁剪 ({i+1}/{len(timestamps)}): {time_str}")
                    
                    # 裁剪视频
                    self.clip_video(video_path, start_time, end_time, output_path)
                    success_count += 1
                    
                except Exception as e:
                    error_msg = f"第{line_num}行: {time_str} - {str(e)}"
                    print(f"裁剪失败: {error_msg}")
                    failed_items.append(error_msg)
                    continue
            
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress("批量裁剪完成!")
            
            # 显示结果
            result_msg = f"批量裁剪完成!\n成功: {success_count}/{len(timestamps)}\n保存位置: {target_dir}"
            if failed_items:
                result_msg += f"\n\n失败项目 ({len(failed_items)}):\n" + "\n".join(failed_items[:5])
                if len(failed_items) > 5:
                    result_msg += f"\n... 还有 {len(failed_items) - 5} 个失败项"
            
            self.root.after(0, lambda: messagebox.showinfo("批量裁剪结果", result_msg))
            
        except Exception as e:
            self.root.after(0, lambda: self.progress_bar.stop())
            self.update_progress("就绪")
            error_msg = str(e)
            self.root.after(0, lambda: messagebox.showerror("错误", f"批量裁剪失败: {error_msg}"))
    
    def start_clipping(self):
        """开始裁剪"""
        mode = self.mode.get()
        
        # 在新线程中执行，避免阻塞UI
        if mode == "single":
            thread = threading.Thread(target=self.process_single_clip)
        elif mode == "batch":
            thread = threading.Thread(target=self.process_batch_clip)
        else:
            messagebox.showinfo("提示", "该功能暂未实现")
            return
        
        thread.daemon = True
        thread.start()


def main():
    root = tk.Tk()
    app = VideoClipperApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

