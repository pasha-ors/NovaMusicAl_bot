import asyncio
import discord
from discord import FFmpegPCMAudio

from config import FFMPEG_PATH
from utils.downloader import download_track


class MusicPlayer:
    def __init__(self):
        self.music_queue = []  # Music queue
        self.current_track = None
        self.repeat_mode = False
        self.is_playing = False

    async def join_channel(self, ctx):
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to use this command!")
            return

        channel = ctx.author.voice.channel
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            try:
                await channel.connect()
                await ctx.send(f"Bot joined the channel: {channel.name}")
            except Exception as e:
                await ctx.send(f"Error connecting: {str(e)}")

    async def leave_channel(self, ctx):
        if ctx.voice_client:
            try:
                await ctx.voice_client.disconnect()
                await ctx.send("Bot disconnected from the voice channel.")
            except Exception as e:
                await ctx.send(f"Error disconnecting: {str(e)}")
        else:
            await ctx.send("Bot is not connected to a voice channel.")

    async def play(self, ctx, query):
        print(f"Play method initiated with query: {query}")

        # Check if the user is in a voice channel
        if not ctx.author.voice:
            await ctx.send("You must be in a voice channel to play music.")
            return

        user_channel = ctx.author.voice.channel
        if not ctx.voice_client or not ctx.voice_client.is_connected():
            try:
                await user_channel.connect()
                await ctx.send(f"Bot joined the channel: {user_channel.name}")
            except Exception as e:
                await ctx.send(f"Error connecting: {str(e)}")

        # Play the music
        async with ctx.typing():
            try:
                filepath, title, url = download_track(query)
                print(f"Track downloaded: {title} ({url})")
                self.music_queue.append((filepath, title, url))
                await ctx.send(f"Added to queue: {title} ({url})")

                if not ctx.voice_client.is_playing():
                    await self.play_next(ctx)

            except Exception as e:
                await ctx.send(f"Error: {e}")
                print(f"Error in play method: {e}")

    async def play_next(self, ctx, repeat_current=False):

        if self.is_playing:
            return

        if not ctx.voice_client or not ctx.voice_client.is_connected():
            ctx.bot.loop.create_task(ctx.send("The bot is disconnected from the voice channel. Playback stopped."))
            return

        if repeat_current or (self.repeat_mode and self.current_track):
            filepath, title, url = self.current_track
        elif self.music_queue:
            filepath, title, url = self.music_queue.pop(0)
            self.current_track = (filepath, title, url)
        else:
            self.is_playing = False
            ctx.bot.loop.create_task(ctx.send("Queue is empty. Playback stopped."))
            return

        self.is_playing = True

        try:
            source = FFmpegPCMAudio(executable=FFMPEG_PATH, source=filepath)
            ctx.voice_client.play(source, after=lambda e: asyncio.create_task(self.on_track_end(ctx)))
            ctx.bot.loop.create_task(ctx.send(f"Now playing: {title} ({url})"))

        except Exception as e:
            await ctx.send(f"Playback error: {e}")
            print(f"Error in play_next method: {e}")

    async def on_track_end(self, ctx):
        self.current_track = None
        if self.music_queue:
            self.is_playing = False
            await self.play_next(ctx)
        else:
            await ctx.send("Queue is empty. Playback finished.")

    async def stop(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Playback stopped.")
        else:
            await ctx.send("Nothing is playing.")

    async def print_queue(self, ctx):
        """Displays the current playback queue."""
        if self.music_queue:
            queue_list = "\n".join([f"{i + 1}. {title}" for i, (_, title, _) in enumerate(self.music_queue)])
            await ctx.send(f"Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is empty.")

    async def next_music(self, ctx):

        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("Nothing is playing right now.")
            return

        ctx.voice_client.stop()
        self.is_playing = False

        if self.repeat_mode and self.current_track:
            await ctx.send("Repeating the current track...")
            await self.play_next(ctx, repeat_current=True)
        elif self.music_queue:
            await ctx.send("Skipping the current track, playing the next...")
            await self.play_next(ctx)
        else:
            await ctx.send("Queue is empty. Playback stopped.")

    async def repeat(self, ctx):
        """Toggles repeat mode."""
        self.repeat_mode = not self.repeat_mode
        if self.repeat_mode:
            await ctx.send("Repeat mode enabled. The current track will repeat.")
        else:
            await ctx.send("Repeat mode disabled.")

    async def clear(self, ctx):
        try:
            self.music_queue.clear()
            await ctx.send("Queue cleared. All tracks removed.")
        except Exception as e:
            await ctx.send(f"Error clearing the queue: {e}")