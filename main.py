import botpy
import os
from user_loop import UserList
from botpy import logging
from botpy.message import Message
from botpy.types.message import MarkdownPayload, MessageMarkdownParams
from botpy.ext.cog_yaml import read

CHANNEL_NAME = '聊天室'
_log = logging.get_logger()
test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def post_message(self, content):
        params = [
            MessageMarkdownParams(key="title", values=["New"]),
            MessageMarkdownParams(key="content", values=[content]),
        ]
        markdown = MarkdownPayload(
            custom_template_id="102078331_1702986277", params=params)
        guilds = await self.api.me_guilds()
        for guild in guilds:
            channels = await self.api.get_channels(guild["id"])
            for channel in channels:
                if channel["name"] == CHANNEL_NAME:
                    _log.info(f"post_message: {content}")
                    respone = await self.api.post_message(channel["id"], markdown=markdown)
                    _log.info(f"channel respone: {respone}")

    async def on_ready(self):
        self.user_list = UserList(
            'user_list.txt', callback=self.post_message, need_wait=True, logger=_log.info)
        await self.user_list.load()
        self.user_list.start_loop()
        await self.post_message("hello")

    async def on_at_message_create(self, message: Message):
        _log.info(f"on_at_message_create: {message.content}")
        if '/关注列表' in message.content:
            await message.reply(content=self.user_list.get_list())
        elif '/添加' in message.content:
            try:
                uid = int(message.content.split(' ')[-1])
                await self.user_list.add_uid(uid)
                await message.reply(content=f'{self.user_list.get_name_by_uid(uid)}添加成功')
            except Exception as e:
                _log.info(f"{e}")
                await message.reply(content=f'添加失败')
        pass


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
