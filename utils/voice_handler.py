import discord
import speech_recognition as sr
import asyncio
import concurrent.futures
from gtts import gTTS
from neural_network.model import classify_action_and_extract_song
from utils.music_player import MusicPlayer
import json
from fuzzywuzzy import fuzz
from transformers import pipeline

classifier = pipeline("text-classification", model="bert-base-uncased")

listening = False

def listen_loop(ctx, loop):
    global listening
    recognizer = sr.Recognizer()

    music_player = MusicPlayer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        while listening:
            try:
                print("Listening...")
                audio = recognizer.listen(source, timeout=5)
                command_text = recognizer.recognize_google(audio)
                # Use the passed loop to run the asynchronous function
                asyncio.run_coroutine_threadsafe(process_command(ctx, command_text, music_player), loop)
            except sr.UnknownValueError:
                print("Could not understand the speech.")
            except sr.WaitTimeoutError:
                print("Timeout while waiting for command.")
            except Exception as e:
                print(f"Error: {e}")

async def start_listening(ctx):
    global listening

    if not ctx.author.voice:
        await ctx.send("You need to be in a voice channel to use this command.")
        return

    if listening:
        await ctx.send("Voice listening mode is already active.")
        return

    listening = True
    await ctx.send("Voice listening mode is activated. Speak your commands.")
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executor, listen_loop, ctx, loop)

async def stop_listening(ctx):
    global listening
    if listening:
        listening = False
        await ctx.send("Voice listening mode is stopped.")
    else:
        await ctx.send("Voice listening mode is already off.")

def fuzzy_process(command, text):
    return fuzz.partial_ratio(text, command) > 70

def process_command_fuzzy(command):
    if fuzzy_process(command, "join") or fuzzy_process(command, "joint") or fuzzy_process(command, "go"):
        return "join"
    elif fuzzy_process(command, "leave") or fuzzy_process(command, "exit") or fuzzy_process(command, "live"):
        return "leave"
    elif fuzzy_process(command, "play") or fuzzy_process(command, "pay"):
        return "play"
    elif fuzzy_process(command, "stop") or fuzzy_process(command, "top"):
        return "stop"
    else:
        return "unknown"

# NLP for intent recognition

def jarvis(command):
    intents = classifier(command)
    if "jarvis" in command.lower():
        return True

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):].strip()
    return text

def process_command_nlp(command):
    # If the command contains "jarvis", process it
    if jarvis(command):
        command = remove_prefix(command, "jarvis")  # Remove "jarvis"

        # Define commands based on keywords
        intent_keywords = {
            "join": {"join", "joint", "go"},
            "leave": {"leave", "exit"},
            "play": {"play", "pay"},
            "stop": {"stop", "top"},
            "repeat": {"repeat"},
            "queue": {"list"},
            "next": {"next"},
            "clear": {"delete"},
        }

        # Find matching intent
        for intent, keywords in intent_keywords.items():
            if any(keyword in command.lower() for keyword in keywords):
                return intent

        # If the command is not recognized
        return "unknown"
    else:
        return "unknown"

async def join_and_play(ctx, audio_file):
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send("You need to be in a voice channel.")
        return

    vc = await channel.connect()

    try:
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg/ffmpeg-2024-12-04-git-2f95bc3cb3-essentials_build/bin/ffmpeg.exe", source=audio_file), after=lambda e: print('done', e))
        while vc.is_playing():
            await asyncio.sleep(1)
    except discord.ClientException as e:
        await ctx.send(f"Playback error: {e}")

async def choice_command(command, ctx, command_text, music_player):

    action, song = classify_action_and_extract_song(command_text)
    print(f"Action: {action}, song: {song}")
    print(f"Command: {command}")

    if command == "join":
        await join_and_play(ctx, "voice_jarvis/caged_activated.aif")
    elif command == "leave":
        await music_player.leave_channel(ctx)
    elif command == "play" and action == "play":
        print(f"Starting playback: {song}")
        if song:
            await music_player.play(ctx, song)
        else:
            await ctx.send("Song not specified. Try saying, for example, 'play Hello by Adele'.")
    elif command == "stop" and action == "stop":
        await music_player.stop(ctx)
    elif command == "next":
        await music_player.next_music(ctx)
    elif command == "repeat":
        await  music_player.repeat(ctx)
    elif command == "queue":
        await  music_player.print_queue(ctx)
    elif command == "clear":
        await music_player.clear(ctx)

async def process_command(ctx, command_text, music_player):

    nlp_result = process_command_nlp(command_text)
    await choice_command(nlp_result, ctx, command_text, music_player)
