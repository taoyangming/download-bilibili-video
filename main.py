import yt_dlp
import os  # 新增导入os模块

# 设置下载选项
ydl_opts = {
    'outtmpl': 'medias/%(title)s.%(ext)s',
    # 修正格式选择器
    'format': 'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'merge_output_format': 'mp4',
    'ffmpeg_location': 'C:/Windows/System32/ffmpeg.exe',
    'postprocessors': [
        # 优先处理视频合并
        {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
            'when': 'post_process'
        },
        # 音频提取配置
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'nopostoverwrites': True
        }
    ],
    'retries': 5,
    'keepvideo': True,
}

# 视频链接
video_url = 'https://www.bilibili.com/video/BV1WJMXzfEzD/?spm_id_from=333.1007.tianma.3-2-8.click&vd_source=c23476bee50dc6790b1c16bfc5377bb6'

# 创建保存目录（新增代码）
os.makedirs('medias', exist_ok=True)

# 使用 yt-dlp 下载视频
if __name__ == '__main__':
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])  # 修正缩进问题