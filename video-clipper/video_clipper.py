"""
视频裁剪软件
支持单点裁剪和批量裁剪模式
版本: 1.3.0
作者: andre.li
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from datetime import datetime, timedelta
import threading
from moviepy.editor import VideoFileClip
from pathlib import Path
import base64
from io import BytesIO
from PIL import Image


class VideoClipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("视频裁剪工具 v1.3.0")
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
                                text="v1.3.0",
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
            "• 时间格式: HH:MM:SS",
            "  例: 12:30:45",
            "",
            "批量裁剪模式",
            "• 输入视频起始UTC时间",
            "• 配置向前/向后裁剪秒数",
            "• 选择时间戳文本文件",
            "• 文件格式: 每行一个时间点",
            "• 支持多种时间格式:",
            "  - HH:MM:SS 或 HH:MM",
            "    例: 12:30:45 或 12:37",
            "  - YYYY-MM-DD HH:MM:SS 或 YYYY-MM-DD HH:MM",
            "    例: 2025-11-13 00:26:39",
            "  - YYYY年MM月DD日HH:MM:SS 或 YYYY年MM月DD日HH:MM",
            "    例: 2025年11月13日00:26:50",
            "  - HH点MM分SS秒 或 HH点MM分",
            "    例: 00点34分20秒 或 12点37分",
            "• 缺少秒数时: 自动使用'向前裁剪秒数'",
            "  例: 12:37 + 向前40秒 = 12:37:40",
            "• 时间和描述: 可以有无空格分隔",
            "  例: 2025-11-18 15:37:15 描述",
            "  或: 2025-11-18 15:37:15描述",
            "• 兼容性: 自动识别中文标点符号（如：、－等）",
            "• 支持 # 开头的注释行和空行",
            "",
            "注意事项",
            "• 裁剪时长必须是正整数",
            "• 缺少秒数时将使用'向前裁剪秒数'作为默认值",
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
    
    def parse_flexible_time(self, time_str):
        """
        解析多种时间格式，返回秒数
        支持的格式:
        - HH:MM:SS (例如: 12:30:45)
        - HH:MM (例如: 12:30, 默认秒数为用户配置的"向前"秒数)
        - YYYY-MM-DD HH:MM:SS (例如: 2025-11-13 00:26:39)
        - YYYY-MM-DD HH:MM (默认秒数为用户配置的"向前"秒数)
        - YYYY年MM月DD日HH:MM:SS (例如: 2025年11月13日00:26:50)
        - YYYY年MM月DD日HH:MM (默认秒数为用户配置的"向前"秒数)
        - HH点MM分SS秒 (例如: 00点34分20秒)
        - HH点MM分 (默认秒数为用户配置的"向前"秒数)
        - 支持中文标点符号（自动转换为英文）
        
        注意: 如果缺少秒数，将使用用户配置的"向前裁剪秒数"作为默认秒数
        例如: 12:37 + 向前40秒 = 12:37:40
        """
        import re
        from datetime import datetime
        
        time_str = time_str.strip()
        
        # 预处理：将中文标点符号替换为英文标点符号
        # 中文冒号 → 英文冒号
        time_str = time_str.replace('：', ':')
        # 全角数字 → 半角数字（如果有的话）
        time_str = time_str.replace('０', '0').replace('１', '1').replace('２', '2')
        time_str = time_str.replace('３', '3').replace('４', '4').replace('５', '5')
        time_str = time_str.replace('６', '6').replace('７', '7').replace('８', '8')
        time_str = time_str.replace('９', '9')
        # 中文破折号 → 英文减号
        time_str = time_str.replace('－', '-').replace('—', '-')
        
        # 获取用户配置的向前裁剪秒数（用作缺少秒数时的默认值）
        try:
            default_seconds = int(self.before_seconds.get())
        except:
            default_seconds = 40  # 如果获取失败，使用默认值40秒
        
        # 格式1: HH:MM:SS
        if re.match(r'^\d{1,2}:\d{2}:\d{2}$', time_str):
            return self.parse_time(time_str)
        
        # 格式1.5: HH:MM (缺少秒，使用默认秒数)
        match = re.match(r'^(\d{1,2}):(\d{2})$', time_str)
        if match:
            hour, minute = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            # 使用默认秒数
            return hour * 3600 + minute * 60 + default_seconds
        
        # 格式2: YYYY-MM-DD HH:MM:SS
        match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2}):(\d{2})$', time_str)
        if match:
            year, month, day, hour, minute, second = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            if not (0 <= second <= 59):
                raise ValueError("秒必须在 0-59 之间")
            return hour * 3600 + minute * 60 + second
        
        # 格式2.5: YYYY-MM-DD HH:MM (缺少秒，使用默认秒数)
        match = re.match(r'^(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{2})$', time_str)
        if match:
            year, month, day, hour, minute = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            # 使用默认秒数
            return hour * 3600 + minute * 60 + default_seconds
        
        # 格式3: YYYY年MM月DD日HH:MM:SS
        match = re.match(r'^(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}):(\d{2}):(\d{2})$', time_str)
        if match:
            year, month, day, hour, minute, second = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            if not (0 <= second <= 59):
                raise ValueError("秒必须在 0-59 之间")
            return hour * 3600 + minute * 60 + second
        
        # 格式3.5: YYYY年MM月DD日HH:MM (缺少秒，使用默认秒数)
        match = re.match(r'^(\d{4})年(\d{1,2})月(\d{1,2})日(\d{1,2}):(\d{2})$', time_str)
        if match:
            year, month, day, hour, minute = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            # 使用默认秒数
            return hour * 3600 + minute * 60 + default_seconds
        
        # 格式4: HH点MM分SS秒
        match = re.match(r'^(\d{1,2})点(\d{1,2})分(\d{1,2})秒$', time_str)
        if match:
            hour, minute, second = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            if not (0 <= second <= 59):
                raise ValueError("秒必须在 0-59 之间")
            return hour * 3600 + minute * 60 + second
        
        # 格式4.5: HH点MM分 (缺少秒，使用默认秒数)
        match = re.match(r'^(\d{1,2})点(\d{1,2})分$', time_str)
        if match:
            hour, minute = map(int, match.groups())
            # 验证时间范围
            if not (0 <= hour <= 23):
                raise ValueError("小时必须在 0-23 之间")
            if not (0 <= minute <= 59):
                raise ValueError("分钟必须在 0-59 之间")
            # 使用默认秒数
            return hour * 3600 + minute * 60 + default_seconds
        
        # 如果没有匹配任何格式
        raise ValueError(
            f"不支持的时间格式: {time_str}\n"
            f"支持的格式:\n"
            f"  • HH:MM:SS (例如: 12:30:45)\n"
            f"  • HH:MM (例如: 12:30, 默认秒数为{default_seconds})\n"
            f"  • YYYY-MM-DD HH:MM:SS (例如: 2025-11-13 00:26:39)\n"
            f"  • YYYY-MM-DD HH:MM (默认秒数为{default_seconds})\n"
            f"  • YYYY年MM月DD日HH:MM:SS (例如: 2025年11月13日00:26:50)\n"
            f"  • YYYY年MM月DD日HH:MM (默认秒数为{default_seconds})\n"
            f"  • HH点MM分SS秒 (例如: 00点34分20秒)\n"
            f"  • HH点MM分 (默认秒数为{default_seconds})\n"
            f"  • 支持中文标点符号（如：、－等）"
        )
    
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
    
    def extract_frame_as_base64(self, video_path, time_seconds):
        """
        提取视频指定时间的帧并转换为base64编码（原始尺寸，不压缩）
        
        Args:
            video_path: 视频文件路径
            time_seconds: 提取帧的时间（秒）
        
        Returns:
            base64编码的图像字符串
        """
        video = None
        try:
            video = VideoFileClip(video_path)
            # 确保时间在有效范围内
            time_seconds = max(0, min(time_seconds, video.duration - 0.1))
            
            # 提取帧
            frame = video.get_frame(time_seconds)
            
            # 转换为PIL图像（保持原始尺寸）
            img = Image.fromarray(frame)
            
            # 转换为base64（高质量，不压缩）
            buffer = BytesIO()
            img.save(buffer, format='JPEG', quality=95)
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return img_base64
        except Exception as e:
            # 如果提取失败，返回None
            return None
        finally:
            if video is not None:
                video.close()
    
    def generate_html_report(self, results, output_dir):
        """
        生成批量裁剪的HTML报告
        
        Args:
            results: 裁剪结果列表，每个元素包含：
                    {
                        'time_str': 时间字符串,
                        'description': 描述,
                        'status': 'success' or 'failed',
                        'output_path': 输出文件路径（成功时）,
                        'error': 错误信息（失败时）,
                        'first_frame': 首帧base64（成功时）,
                        'last_frame': 尾帧base64（成功时）
                    }
            output_dir: 报告输出目录
        
        Returns:
            HTML报告文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(output_dir, f"裁剪报告_{timestamp}.html")
        
        # 统计信息
        total = len(results)
        success = sum(1 for r in results if r['status'] == 'success')
        failed = total - success
        
        # HTML模板
        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>视频裁剪报告</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Microsoft YaHei UI', 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}
        
        .header .time {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: flex;
            justify-content: space-around;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            min-width: 150px;
        }}
        
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card.total .number {{ color: #667eea; }}
        .stat-card.success .number {{ color: #10b981; }}
        .stat-card.failed .number {{ color: #ef4444; }}
        
        .stat-card .label {{
            color: #6b7280;
            font-size: 1em;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .result-item {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 25px;
            transition: all 0.3s ease;
        }}
        
        .result-item:hover {{
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }}
        
        .result-item.success {{
            border-left: 5px solid #10b981;
        }}
        
        .result-item.failed {{
            border-left: 5px solid #ef4444;
        }}
        
        .result-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        
        .result-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #1f2937;
        }}
        
        .status-badge {{
            padding: 6px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }}
        
        .status-badge.success {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .status-badge.failed {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .result-info {{
            margin-bottom: 20px;
        }}
        
        .info-row {{
            display: flex;
            padding: 8px 0;
            border-bottom: 1px dashed #e5e7eb;
        }}
        
        .info-row:last-child {{
            border-bottom: none;
        }}
        
        .info-label {{
            font-weight: bold;
            color: #6b7280;
            min-width: 100px;
        }}
        
        .info-value {{
            color: #1f2937;
            flex: 1;
        }}
        
        .frames-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }}
        
        .frame-box {{
            background: #f9fafb;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        
        .frame-box h4 {{
            color: #6b7280;
            margin-bottom: 10px;
            font-size: 1em;
        }}
        
        .frame-box img {{
            max-width: 100%;
            border-radius: 6px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            cursor: pointer;
            transition: transform 0.2s ease;
        }}
        
        .frame-box img:hover {{
            transform: scale(1.02);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
        
        .error-message {{
            background: #fef2f2;
            border: 1px solid #fecaca;
            border-radius: 8px;
            padding: 15px;
            color: #991b1b;
            margin-top: 10px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            background: #f9fafb;
            color: #6b7280;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .frames-container {{
                grid-template-columns: 1fr;
            }}
            
            .summary {{
                flex-direction: column;
                gap: 15px;
            }}
        }}
        
        /* 图片放大模态框样式 */
        .modal {{
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.95);
            animation: fadeIn 0.3s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .modal-content {{
            position: relative;
            margin: auto;
            padding: 0;
            width: 90%;
            max-width: 1200px;
            top: 50%;
            transform: translateY(-50%);
            animation: zoomIn 0.3s ease;
        }}
        
        @keyframes zoomIn {{
            from {{ transform: translateY(-50%) scale(0.8); }}
            to {{ transform: translateY(-50%) scale(1); }}
        }}
        
        .modal-content img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.5);
        }}
        
        .close-modal {{
            position: absolute;
            top: 20px;
            right: 35px;
            color: #f1f1f1;
            font-size: 50px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            z-index: 10000;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
        }}
        
        .close-modal:hover,
        .close-modal:focus {{
            color: #bbb;
        }}
        
        .modal-caption {{
            text-align: center;
            color: #f1f1f1;
            padding: 20px;
            font-size: 1.2em;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.8);
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📹 视频裁剪报告</h1>
            <div class="time">生成时间: {datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")}</div>
        </div>
        
        <div class="summary">
            <div class="stat-card total">
                <div class="number">{total}</div>
                <div class="label">总计</div>
            </div>
            <div class="stat-card success">
                <div class="number">{success}</div>
                <div class="label">成功</div>
            </div>
            <div class="stat-card failed">
                <div class="number">{failed}</div>
                <div class="label">失败</div>
            </div>
        </div>
        
        <div class="content">
"""
        
        # 添加每个结果
        for idx, result in enumerate(results, 1):
            status_class = result['status']
            status_text = '✓ 成功' if status_class == 'success' else '✗ 失败'
            
            html_content += f"""
            <div class="result-item {status_class}">
                <div class="result-header">
                    <div class="result-title">片段 #{idx}</div>
                    <div class="status-badge {status_class}">{status_text}</div>
                </div>
                
                <div class="result-info">
                    <div class="info-row">
                        <div class="info-label">时间点:</div>
                        <div class="info-value">{result['time_str']}</div>
                    </div>
"""
            
            if result.get('description'):
                html_content += f"""
                    <div class="info-row">
                        <div class="info-label">描述:</div>
                        <div class="info-value">{result['description']}</div>
                    </div>
"""
            
            if status_class == 'success':
                output_filename = os.path.basename(result['output_path'])
                html_content += f"""
                    <div class="info-row">
                        <div class="info-label">输出文件:</div>
                        <div class="info-value">{output_filename}</div>
                    </div>
                </div>
"""
                
                # 添加首尾帧图像
                if result.get('first_frame') and result.get('last_frame'):
                    html_content += f"""
                <div class="frames-container">
                    <div class="frame-box">
                        <h4>🎬 首帧</h4>
                        <img src="data:image/jpeg;base64,{result['first_frame']}" alt="首帧">
                    </div>
                    <div class="frame-box">
                        <h4>🎞️ 尾帧</h4>
                        <img src="data:image/jpeg;base64,{result['last_frame']}" alt="尾帧">
                    </div>
                </div>
"""
            else:
                html_content += f"""
                </div>
                <div class="error-message">
                    <strong>错误信息:</strong> {result.get('error', '未知错误')}
                </div>
"""
            
            html_content += """
            </div>
"""
        
        # 添加页脚
        html_content += f"""
        </div>
        
        <div class="footer">
            视频裁剪工具 v1.3.0 | 作者: andre.li | {datetime.now().year}
        </div>
    </div>
    
    <!-- 图片放大模态框 -->
    <div id="imageModal" class="modal">
        <span class="close-modal">&times;</span>
        <div class="modal-content">
            <img id="modalImage" src="" alt="放大图像">
            <div class="modal-caption" id="modalCaption"></div>
        </div>
    </div>
    
    <script>
        // 图片放大功能
        const modal = document.getElementById('imageModal');
        const modalImg = document.getElementById('modalImage');
        const modalCaption = document.getElementById('modalCaption');
        const closeBtn = document.querySelector('.close-modal');
        
        // 为所有图片添加点击事件
        document.querySelectorAll('.frame-box img').forEach(img => {{
            img.addEventListener('click', function() {{
                modal.style.display = 'block';
                modalImg.src = this.src;
                
                // 获取图片标题（首帧或尾帧）
                const frameTitle = this.closest('.frame-box').querySelector('h4').textContent;
                
                // 获取片段信息
                const resultItem = this.closest('.result-item');
                const segmentTitle = resultItem.querySelector('.result-title').textContent;
                const timeInfo = resultItem.querySelector('.info-value').textContent;
                
                modalCaption.textContent = `${{segmentTitle}} - ${{timeInfo}} - ${{frameTitle}}`;
            }});
        }});
        
        // 点击关闭按钮
        closeBtn.addEventListener('click', function() {{
            modal.style.display = 'none';
        }});
        
        // 点击模态框背景关闭
        modal.addEventListener('click', function(e) {{
            if (e.target === modal) {{
                modal.style.display = 'none';
            }}
        }});
        
        // ESC键关闭
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'Escape' && modal.style.display === 'block') {{
                modal.style.display = 'none';
            }}
        }});
    </script>
</body>
</html>
"""
        
        # 写入文件
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_path
    
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
                
                # 智能解析时间格式
                # 支持多种格式，支持时间和描述之间有无空格
                import re
                
                # 尝试匹配不同的时间格式
                time_str = None
                description = ""
                
                # 格式1: YYYY-MM-DD HH:MM:SS 描述（\s*匹配0个或多个空格）
                match = re.match(r'^(\d{4}-\d{1,2}-\d{1,2}\s+\d{1,2}:\d{2}:\d{2})\s*(.*)$', line)
                if match:
                    time_str = match.group(1)
                    description = match.group(2)
                else:
                    # 格式2: YYYY年MM月DD日HH:MM:SS 描述（\s*匹配0个或多个空格）
                    match = re.match(r'^(\d{4}年\d{1,2}月\d{1,2}日\d{1,2}:\d{2}:\d{2})\s*(.*)$', line)
                    if match:
                        time_str = match.group(1)
                        description = match.group(2)
                    else:
                        # 格式3: HH点MM分SS秒 描述（\s*匹配0个或多个空格）
                        match = re.match(r'^(\d{1,2}点\d{1,2}分\d{1,2}秒)\s*(.*)$', line)
                        if match:
                            time_str = match.group(1)
                            description = match.group(2)
                        else:
                            # 格式4: HH:MM:SS 描述（\s*匹配0个或多个空格）
                            match = re.match(r'^(\d{1,2}:\d{2}:\d{2})\s*(.*)$', line)
                            if match:
                                time_str = match.group(1)
                                description = match.group(2)
                            else:
                                # 格式5: HH:MM 描述（\s*匹配0个或多个空格，自动补全秒数）
                                match = re.match(r'^(\d{1,2}:\d{2})\s*(.*)$', line)
                                if match:
                                    time_str = match.group(1)
                                    description = match.group(2)
                
                if time_str:
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
            results = []  # 用于生成HTML报告的结果列表
            
            for i, (time_str, description, line_num) in enumerate(timestamps):
                try:
                    # 解析时间（支持多种格式）
                    clip_time_seconds = self.parse_flexible_time(time_str)
                    
                    # 计算相对于视频开始的秒数
                    relative_seconds = clip_time_seconds - video_start_seconds
                    
                    if relative_seconds < 0:
                        error_msg = f"时间点早于视频起始时间"
                        failed_items.append(f"第{line_num}行: {time_str} - {error_msg}")
                        results.append({
                            'time_str': time_str,
                            'description': description,
                            'status': 'failed',
                            'error': error_msg
                        })
                        continue
                    
                    # 计算裁剪的起止时间(使用用户配置的时长)
                    start_time = relative_seconds - before_sec
                    end_time = relative_seconds + after_sec
                    
                    # 检查时间范围
                    if start_time < 0:
                        error_msg = f"时间点太早（需要前{before_sec}秒）"
                        failed_items.append(f"第{line_num}行: {time_str} - {error_msg}")
                        results.append({
                            'time_str': time_str,
                            'description': description,
                            'status': 'failed',
                            'error': error_msg
                        })
                        continue
                    
                    if end_time > video_duration:
                        error_msg = f"时间点太晚（需要后{after_sec}秒，视频时长{self.seconds_to_time(video_duration)}）"
                        failed_items.append(f"第{line_num}行: {time_str} - {error_msg}")
                        results.append({
                            'time_str': time_str,
                            'description': description,
                            'status': 'failed',
                            'error': error_msg
                        })
                        continue
                    
                    # 生成输出文件名
                    safe_desc = "".join(c for c in description if c.isalnum() or c in (' ', '-', '_')).strip()
                    if safe_desc:
                        output_filename = f"{time_str.replace(':', '-').replace(' ', '_').replace('年', '').replace('月', '').replace('日', '').replace('点', '').replace('分', '').replace('秒', '')}_{safe_desc}.mp4"
                    else:
                        output_filename = f"{time_str.replace(':', '-').replace(' ', '_').replace('年', '').replace('月', '').replace('日', '').replace('点', '').replace('分', '').replace('秒', '')}.mp4"
                    output_path = os.path.join(target_dir, output_filename)
                    
                    self.update_progress(f"正在裁剪 ({i+1}/{len(timestamps)}): {time_str}")
                    
                    # 裁剪视频
                    self.clip_video(video_path, start_time, end_time, output_path)
                    
                    # 提取首尾帧
                    self.update_progress(f"正在提取帧 ({i+1}/{len(timestamps)}): {time_str}")
                    first_frame = self.extract_frame_as_base64(output_path, 0.1)
                    
                    # 获取裁剪后的视频时长
                    clip_duration = end_time - start_time
                    last_frame = self.extract_frame_as_base64(output_path, clip_duration - 0.1)
                    
                    # 记录成功结果
                    results.append({
                        'time_str': time_str,
                        'description': description,
                        'status': 'success',
                        'output_path': output_path,
                        'first_frame': first_frame,
                        'last_frame': last_frame
                    })
                    
                    success_count += 1
                    
                except Exception as e:
                    error_msg = str(e)
                    print(f"裁剪失败: 第{line_num}行: {time_str} - {error_msg}")
                    failed_items.append(f"第{line_num}行: {time_str} - {error_msg}")
                    results.append({
                        'time_str': time_str,
                        'description': description,
                        'status': 'failed',
                        'error': error_msg
                    })
                    continue
            
            self.root.after(0, lambda: self.progress_bar.stop())
            
            # 生成HTML报告
            self.update_progress("正在生成报告...")
            try:
                report_path = self.generate_html_report(results, target_dir)
                self.update_progress("批量裁剪完成!")
                
                # 显示结果
                result_msg = f"批量裁剪完成!\n\n成功: {success_count}/{len(timestamps)}\n保存位置: {target_dir}\n\nHTML报告已生成:\n{os.path.basename(report_path)}"
                if failed_items:
                    result_msg += f"\n\n失败项目 ({len(failed_items)}):\n" + "\n".join(failed_items[:3])
                    if len(failed_items) > 3:
                        result_msg += f"\n... 还有 {len(failed_items) - 3} 个失败项"
                
                self.root.after(0, lambda: messagebox.showinfo("批量裁剪结果", result_msg))
                
                # 询问是否打开报告
                def ask_open_report():
                    if messagebox.askyesno("打开报告", "是否在浏览器中打开HTML报告？"):
                        import webbrowser
                        webbrowser.open(report_path)
                
                self.root.after(100, ask_open_report)
                
            except Exception as e:
                print(f"生成报告失败: {str(e)}")
                self.update_progress("批量裁剪完成!")
                result_msg = f"批量裁剪完成!\n\n成功: {success_count}/{len(timestamps)}\n保存位置: {target_dir}\n\n注意: HTML报告生成失败"
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

