from utils.music_player import MusicPlayer


def setup_commands(bot):
    music_player = MusicPlayer()

    @bot.event
    async def on_ready():
        print(f"Bot {bot.user.name} is online and ready!")

    @bot.command()
    async def join(ctx):
        """Command to join the voice channel."""
        await music_player.join_channel(ctx)

    @bot.command()
    async def leave(ctx):
        """Command to leave the voice channel."""
        await music_player.leave_channel(ctx)

    @bot.command()
    async def play(ctx, *, query):
        """Command to play music."""
        await music_player.play(ctx, query)

    @bot.command()
    async def stop(ctx):
        """Command to stop the music."""
        await music_player.stop(ctx)

    @bot.command()
    async def queue(ctx):
        """Command to view the music queue."""
        await music_player.print_queue(ctx)

    @bot.command()
    async def next(ctx):
        """Command to play the next track in the queue."""
        await music_player.next_music(ctx)

    @bot.command()
    async def repeat(ctx):
        """Command to repeat the current track."""
        await music_player.repeat(ctx)

    @bot.command()
    async def clear(ctx):
        """Command to clear the music queue."""
        await music_player.clear(ctx)