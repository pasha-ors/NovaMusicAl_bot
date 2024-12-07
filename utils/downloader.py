import os
from yt_dlp import YoutubeDL
from config import FFMPEG_PATH, TEMP_FOLDER

ytdl_format_options = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'ffmpeg_location': FFMPEG_PATH,
    'outtmpl': os.path.join(TEMP_FOLDER, '%(title)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
}

ytdl = YoutubeDL(ytdl_format_options)

def download_track(query):
    """Downloads the track and returns its path, title, and URL."""
    info = ytdl.extract_info(f"ytsearch:{query}", download=True)
    video = info['entries'][0]
    title = video['title']
    url = video['webpage_url']
    filepath = ytdl.prepare_filename(video)
    if filepath.endswith('.webm'):
        filepath = filepath.replace('.webm', '.mp3')
    return filepath, title, url