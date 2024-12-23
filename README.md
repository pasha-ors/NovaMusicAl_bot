# Discord Music Bot

This is a Discord bot that allows users to control music playback through voice commands. It integrates with the YouTube API to download music tracks, uses speech recognition for voice commands, and provides various commands like play, stop, skip, repeat, and more.

## Features:
- Join and leave voice channels
- Play, stop, skip, and repeat tracks
- Display the current music queue
- Process voice commands using speech recognition
- NLP-based command recognition with fuzzy matching
- Use of FFmpeg for audio playback

## Requirements:

- Python 3.8 or higher
- `discord.py` library
- `speech_recognition` library
- `fuzzywuzzy` library
- `transformers` library (for BERT-based intent classification)
- `yt-dlp` for downloading YouTube audio
- `gTTS` for text-to-speech functionality
- FFmpeg installed (make sure it's accessible via the system path or specify its path in the config)

## Installation:

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/music-bot.git
    cd music-bot
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up the `.env` file to store sensitive information:
    ```bash
    DISCORD_TOKEN=your-discord-bot-token
    ```

5. Install FFmpeg:
    - Download FFmpeg from [FFmpeg official website](https://ffmpeg.org/download.html) and set it up.
    - Make sure `FFMPEG_PATH` in the `config.py` file is updated with the path to the FFmpeg executable.

## Usage:

1. Start the bot:
    ```bash
    python main.py
    ```

2. Once the bot is running, you can interact with it by sending commands in your Discord server.

### Example Commands:

- `/join` - Makes the bot join your voice channel.
- `/leave` - Makes the bot leave the voice channel.
- `/play <song_name>` - Plays a song. You can specify the song name, e.g., `/play Never Gonna Give You Up by Rick Astley`.
- `/stop` - Stops the music.
- `/next` - Skips the current track.
- `/repeat` - Repeats the current song if enabled.
- `/queue` - Shows the current queue of songs.
- `/clear` - Clears the music queue.

### Voice Commands:

The bot also listens to your voice commands while you're in a voice channel. To start voice listening mode:

- `/start_listening` - Activates voice listening mode.
- `/stop_listening` - Stops voice listening mode.

## How It Works:

1. **Speech Recognition**: The bot uses the `speech_recognition` library to listen for voice commands in real-time. These commands are processed and matched with pre-defined actions like `join`, `play`, `stop`, etc.

2. **YouTube Audio Download**: The bot downloads YouTube audio using `yt-dlp` and converts it to MP3 format using FFmpeg.

3. **NLP for Intent Recognition**: The bot uses a pre-trained BERT model (via the `transformers` library) to classify text commands and determine the intended action (e.g., play a song, stop the music).

4. **Queue Management**: The bot maintains a music queue, allowing users to play multiple songs sequentially. Users can skip to the next song, repeat the current song, or stop the playback.

## Contributing:

Feel free to fork this project and submit pull requests. Contributions are welcome!
