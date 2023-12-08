import json
from user_loop import UserList
from qq_bot import QQBot

with open('qq_bot.json', 'r') as file:
    data = json.load(file)
bot = QQBot(**data)
bot.send_message('start pushing')


def push(message):
    print(message)
    with open('qq_bot.log', mode='a+') as f:
        f.write(message)
        f.write('\n')
    bot.send_message(message)


with open('user_list.txt') as f:
    user_list = list(map(int, f.read().split()))

user_list = UserList(user_list, push)
try:
    user_list.run_loop()
except Exception as e:
    message = f'Error: {e}'
    push(message)
