import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from yt_dlp import YoutubeDL
import os

# https://www.youtube.com/watch?v=5gyDP0naR8Y 做测试用的最短的影片
class VideoDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("视频下载器 (yt-dlp)")

        # 输入框
        self.url_text = tk.Text(root, height=5, width=50)
        self.url_text.pack(pady=10)

        # 分辨率选择
        self.resolution_var = tk.StringVar()
        self.resolution_var.set("最高清晰度")
        self.resolution_menu = tk.OptionMenu(root, self.resolution_var, "最高清晰度", "1080p", "720p", "480p")
        self.resolution_menu.pack(pady=5)

        # 音频提取选项
        self.audio_var = tk.IntVar()
        self.audio_checkbox = tk.Checkbutton(root, text="提取音频为 MP3", variable=self.audio_var)
        self.audio_checkbox.pack(pady=5)

        # 目录选择
        self.download_dir = tk.StringVar()
        self.download_dir.set("默认目录")
        self.dir_button = tk.Button(root, text="选择目录", command=self.choose_directory)
        self.dir_button.pack(pady=5)

        # 下载按钮
        self.download_button = tk.Button(root, text="开始下载", command=self.start_download)
        self.download_button.pack(pady=10)

        # 下载进度条
        self.progress = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
        self.progress.pack(pady=10)

    def choose_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.download_dir.set(directory)

    def start_download(self):
        urls = self.url_text.get("1.0", tk.END).splitlines()
        resolution = self.resolution_var.get()
        audio = self.audio_var.get()
        dir_path = self.download_dir.get() if self.download_dir.get() != "默认目录" else os.path.expanduser("~/Downloads")

        for url in urls:
            if url.strip() == "":
                continue
            threading.Thread(target=self.download_video, args=(url, resolution, audio, dir_path)).start()

    def download_video(self, url, resolution, audio, dir_path):
        ydl_opts = {
            'outtmpl': os.path.join(dir_path, '%(title)s.%(ext)s'),
            'progress_hooks': [self.update_progress],
            # 新增浏览器模拟参数
            'http_headers': {
                'Accept-Language': 'en-US,en;q=0.9',
            },
            # 添加cookies支持（需要用户提供cookies.txt）
            # 'cookiefile': 'cookies.txt',
            # 添加错误处理参数
            'retries': 3,
            'ignoreerrors': False,
            'throttledratelimit': 500000,
        }

        # 处理分辨率
        if resolution != "最高清晰度":
            ydl_opts['format'] = f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]'

        # 处理音频提取
        if audio:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("下载完成", f"视频已下载到：{dir_path}")
        except Exception as e:
            messagebox.showerror("错误", f"下载失败：{str(e)}")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
            if total_bytes:
                downloaded_bytes = d['downloaded_bytes']
                percent = (downloaded_bytes / total_bytes) * 100
                self.progress['value'] = percent
                self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoDownloader(root)
    root.mainloop()