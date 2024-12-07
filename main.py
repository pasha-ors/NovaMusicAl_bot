import discord
from discord.ext import commands
from config import DISCORD_TOKEN

from commands.main_commands import setup_commands
from commands.voice_commands import setup_voice_commands

intents = discord.Intents.default()
intents.message_content = True  # Permission to read message content

bot = commands.Bot(command_prefix="/", intents=intents)

setup_commands(bot)
setup_voice_commands(bot)


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)