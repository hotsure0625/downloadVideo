!pip install yt-dlp
import os
from yt_dlp import YoutubeDL

def download_video_cli(url, resolution="best", extract_audio=False, download_dir="./downloads"):
    """
    使用 yt-dlp 下载视频或提取音频。

    Args:
        url (str): 视频的 URL。
        resolution (str): 下载视频的分辨率，如 '1080p', '720p', '480p' 或 'best'。
        extract_audio (bool): 是否提取音频为 MP3。
        download_dir (str): 下载文件保存的目录。
    """
    # 创建下载目录（如果不存在）
    os.makedirs(download_dir, exist_ok=True)

    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'ignoreerrors': True, # 忽略一些下载错误，但会记录
        'retries': 3,
        'throttledratelimit': 500000, # 限制下载速度（字节/秒），防止带宽占用过高
        'quiet': False, # 显示下载进度和信息
        'verbose': False, # 更详细的日志（可根据需要开启）
    }

    # 处理分辨率
    if resolution != "best":
        # 对于视频+音频，选择分辨率小于或等于指定分辨率的最佳视频和最佳音频
        ydl_opts['format'] = f'bestvideo[height<={resolution[:-1]}]+bestaudio/best[height<={resolution[:-1]}]'

    # 处理音频提取
    if extract_audio:
        ydl_opts['format'] = 'bestaudio/best' # 只下载最佳音频
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', # MP3 192kbps
        }]

    try:
        print(f"正在下载：{url} 到 {download_dir}...")
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"下载完成：{url}")
    except Exception as e:
        print(f"下载 {url} 失败：{e}")

# --- 示例用法 --- 更改以下参数进行测试

# 视频 URL 列表
# 请替换为您想要下载的视频 URL
video_urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ", # 示例 YouTube 视频 (Rick Astley - Never Gonna Give You Up)
    "https://www.youtube.com/watch?v=5gyDP0naR8Y" # 您的测试视频
]

# 下载选项
selected_resolution = "720p" # 可选 'best', '1080p', '720p', '480p'
extract_only_audio = False # 设置为 True 提取 MP3，设置为 False 下载视频
output_directory = "/content/downloads" # 下载文件保存的路径

print(f"将下载到目录: {os.path.abspath(output_directory)}")

for url in video_urls:
    download_video_cli(url, selected_resolution, extract_only_audio, output_directory)

print("所有下载任务已提交。")

#################################################

import shutil
from google.colab import files

# 要下载的文件夹路径
folder_to_archive = "/content/downloads"
# 压缩后保存的文件名
archive_name = "downloaded_videos"

# 创建压缩文件
shutil.make_archive(archive_name, 'zip', folder_to_archive)

# 下载压缩文件
try:
    files.download(f'{archive_name}.zip')
    print(f"文件夹 '{folder_to_archive}' 已被压缩并开始下载为 '{archive_name}.zip'。")
except Exception as e:
    print(f"下载时发生错误：{e}")
