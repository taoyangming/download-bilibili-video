from flask import Flask, request, render_template, redirect
import whisper
from datetime import timedelta
import yt_dlp
import os
from pathlib import Path
from flask import Response
import json
import time

app = Flask(__name__)
# 添加全局进度状态
current_progress = {'percent': '0%', 'speed': '', 'eta': ''}
# 先定义进度钩子函数
def progress_hook(d):
    global current_progress
    if d['status'] == 'downloading':
        current_progress = {
            'percent': d['_percent_str'],
            'speed': d['_speed_str'],
            'eta': d['_eta_str']
        }
    elif d['status'] == 'error':
        current_progress = {'error': d['error']}


# 下载配置
ydl_opts = {
    'outtmpl': 'medias/%(title)s.%(ext)s',
    'format': 'bestvideo[ext=mp4][vcodec^=avc]+bestaudio[ext=m4a]/bestvideo+bestaudio',
    'merge_output_format': 'mp4',
    'ffmpeg_location': 'C:/Windows/System32/ffmpeg.exe',
    'postprocessors': [
        {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
            'when': 'post_process'
        },
        {
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'nopostoverwrites': True
        }
    ],
    'retries': 5,
    'keepvideo': True,
    'progress_hooks': [progress_hook],
}

# 初始化Whisper模型
model = whisper.load_model("medium")


@app.route('/')
def index():
    return render_template('index.html')

# 添加SSE路由
@app.route('/progress')
def progress():
    def generate():
        while True:
            yield f"data: {json.dumps(current_progress)}\n\n"
            time.sleep(1)
    return Response(generate(), mimetype='text/event-stream')

@app.route('/download', methods=['POST'])
def download_video():
    current_progress = {'percent': '0%', 'speed': '', 'eta': ''}
    video_url = request.form['video_url']
    os.makedirs('medias', exist_ok=True)
    Path("templates").mkdir(exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            title = info.get('title', 'untitled').replace("/", "_")

            # 生成字幕
            audio_path = f"medias/audio/{title}.mp3"
            transcript_path = f"medias/transcripts/{title}.txt"
            os.makedirs(os.path.dirname(transcript_path), exist_ok=True)

            result = model.transcribe(audio_path)
            with open(transcript_path, 'w', encoding='utf-8') as f:
                for segment in result['segments']:
                    start = str(timedelta(seconds=segment['start']))
                    end = str(timedelta(seconds=segment['end']))
                    f.write(f"[{start} --> {end}] {segment['text']}\n")

            return redirect(f'/report/{title}')
    except Exception as e:
        return f"处理失败: {str(e)}"


@app.route('/report/<title>')
def show_report(title):
    return render_template('report.html',
                           title=title,
                           video_file=f"medias/{title}.mp4",
                           audio_file=f"medias/audio/{title}.mp3",
                           transcript_file=f"medias/transcripts/{title}.txt"
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)