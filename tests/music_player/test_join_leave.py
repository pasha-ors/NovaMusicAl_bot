import unittest
from unittest.mock import AsyncMock, MagicMock
from utils.music_player import MusicPlayer

class TestMusicPlayer(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.music_player = MusicPlayer()

    async def test_join_channel_user_not_in_voice(self):

        ctx = MagicMock()
        ctx.author.voice = None
        ctx.send = AsyncMock()

        # Вызываем метод join_channel
        await self.music_player.join_channel(ctx)

        # Проверяем, что метод ctx.send был вызван с нужным сообщением
        ctx.send.assert_called_once_with("You must be in a voice channel to use this command!")

    async def test_join_channel_bot_connects(self):
        # Создаем фиктивный контекст с голосовым каналом
        ctx = MagicMock()
        ctx.author.voice = MagicMock()
        ctx.author.voice.channel = MagicMock()
        ctx.voice_client = None
        ctx.send = AsyncMock()

        # Эмулируем подключение бота к каналу
        ctx.author.voice.channel.connect = AsyncMock()

        # Вызываем метод join_channel
        await self.music_player.join_channel(ctx)

        # Проверяем, что бот пытается подключиться и отправляет сообщение
        ctx.author.voice.channel.connect.assert_called_once()
        ctx.send.assert_called_with(f"The bot has joined the channel: {ctx.author.voice.channel.name}")

    async def test_leave_channel_bot_connected(self):
        # Создаем фиктивный контекст с подключенным ботом
        ctx = MagicMock()
        ctx.voice_client = MagicMock()
        ctx.voice_client.disconnect = AsyncMock()
        ctx.send = AsyncMock()

        # Вызываем метод leave_channel
        await self.music_player.leave_channel(ctx)

        # Проверяем, что бот отключился и сообщение отправлено
        ctx.voice_client.disconnect.assert_called_once()
        ctx.send.assert_called_once_with("The bot has disconnected from the voice channel.")

    async def test_leave_channel_bot_not_connected(self):
        # Создаем фиктивный контекст, где бот не подключен
        ctx = MagicMock()
        ctx.voice_client = None
        ctx.send = AsyncMock()

        # Вызываем метод leave_channel
        await self.music_player.leave_channel(ctx)

        # Проверяем, что отправлено соответствующее сообщение
        ctx.send.assert_called_once_with("The bot is not connected to the voice channel.")


if __name__ == "__main__":
    unittest.main()