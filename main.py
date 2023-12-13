import asyncio
import botpy
import os
from user_loop import UserList
from botpy import logging
from botpy.message import Message
from botpy.ext.cog_yaml import read

CHANNEL_NAME = '聊天室'
_log = logging.get_logger()
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def post_message(self, content):
        guilds = await self.api.me_guilds()
        for guild in guilds:
            channels = await self.api.get_channels(guild["id"])
            for channel in channels:
                if channel["name"] == CHANNEL_NAME:
                    _log.info(f"post_message: {content}")
                    respone = await self.api.post_message(channel["id"], content)
                    _log.info(f"respone: {respone}")

    async def on_ready(self):
        with open('user_list.txt') as f:
            uid_list = list(map(int, f.read().split()))
        user_list = UserList(
            uid_list, callback=self.post_message, need_wait=True, logger=_log.info)
        user_list.start_loop()
        await self.post_message("start pushing")

    async def on_at_message_create(self, message: Message):
        pass


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
