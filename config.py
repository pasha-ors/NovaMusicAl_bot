import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Path to FFmpeg executable (update depending on your system)
FFMPEG_PATH = r"ffmpeg/ffmpeg-2024-12-04-git-2f95bc3cb3-essentials_build/bin/ffmpeg.exe"

# Folder for temporary files
TEMP_FOLDER = os.path.join(os.getcwd(), "temp")
os.makedirs(TEMP_FOLDER, exist_ok=True)

# Path to the database
DB_PATH = os.path.join(os.getcwd(), "database", "tracks.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)