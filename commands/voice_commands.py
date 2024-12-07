from discord.ext import commands
from utils.voice_handler import start_listening, stop_listening

def setup_voice_commands(bot):
    @bot.command()
    async def listen(ctx):
        """Activates voice listening mode."""
        await start_listening(ctx)

    @bot.command()
    async def stop_listening(ctx):
        """Stops voice listening mode."""
        await stop_listening(ctx)