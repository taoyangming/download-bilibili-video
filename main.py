import yt_dlp
import os  # 新增导入os模块

# 设置下载选项
ydl_opts = {
    'outtmpl': '下载的视频/%(title)s.%(ext)s',
    # 修改格式选择器为兼容性更好的组合
    'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'merge_output_format': 'mp4',
    # 添加ffmpeg路径（如果已安装请取消注释）
    'ffmpeg_location': 'C:/Windows/System32/ffmpeg.exe',
    # 强制使用h264编码
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4'
    }],
    'retries': 5
}

# 视频链接
video_url = 'https://www.bilibili.com/video/BV1jx39zsE6i/?spm_id_from=333.1007.tianma.5-4-18.click&vd_source=c23476bee50dc6790b1c16bfc5377bb6'

# 创建保存目录（新增代码）
os.makedirs('下载的视频', exist_ok=True)

# 使用 yt-dlp 下载视频
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([video_url])  # 修正缩进问题