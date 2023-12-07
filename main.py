import json
from user_loop import UserList
from qq_bot import QQBot

with open('qq_bot.json', 'r') as file:
    data = json.load(file)
bot = QQBot(**data)
bot.send_message('start pushing')


def push(dynamic):
    # with open('output.json', mode='w') as f:
    #     f.write(json.dumps(dynamic, ensure_ascii=False))
    type = dynamic['desc']['type']
    user_name = dynamic['desc']['user_profile']['info']['uname']
    if dynamic['desc']['type'] == 8:
        # video
        title = dynamic['card']['title']
        desc = dynamic['card']['desc']
        message = '{}发布了视频\n标题：{}\n简介：{}'.format(user_name, title, desc)
    elif dynamic['desc']['type'] == 4:
        # messege
        content = dynamic['card']['item']['content']
        message = '{}发布了文字\n内容：{}'.format(user_name, content)
    elif dynamic['desc']['type'] == 2:
        # image
        message = '{}发布了图片'.format(user_name)
    else:
        message = '{}发布了未知类型[{}]的动态'.format(user_name, type)
    bot.send_message(message)


with open('user_list.txt') as f:
    user_list = list(map(int, f.read().split()))

user_list = UserList(user_list, push)
try:
    user_list.run_loop()
except Exception as e:
    message = f'Error: {e}'
    bot.send_message(message)
