import requests
import json
import time

CHANNEL_NAME = '聊天室'
ACCESS_TOKEN_URL = 'https://bots.qq.com/app/getAppAccessToken'
API_URL = 'https://api.sgroup.qq.com'

false = False
true = True
null = None


class QQBot:
    def __init__(self, appId, clientSecret):
        self.appId = appId
        self.clientSecret = clientSecret
        self.token = None
        self.expires = 0
        self.last_time = time.time()

    def get_token(self):
        if not self.token or time.time() > self.last_time+self.expires:
            headers = {
                'Content-Type': 'application/json'
            }
            data = {
                'appId': self.appId,
                'clientSecret': self.clientSecret
            }
            response = requests.post(
                ACCESS_TOKEN_URL, headers=headers, data=json.dumps(data))
            response_val = eval(response.text)
            self.token = response_val['access_token']
            self.expires = int(response_val['expires_in'])
            self.last_time = time.time()
        return self.token

    def get_guilds(self):
        url = API_URL+'/users/@me/guilds'
        headers = {
            'Authorization': 'QQBot {}'.format(self.get_token()),
            'X-Union-Appid': self.appId
        }
        response = requests.get(url, headers=headers)
        response_val = eval(response.text)
        return response_val

    def get_channels(self, guild_id):
        url = API_URL+'/guilds/{}/channels'.format(guild_id)
        headers = {
            'Authorization': 'QQBot {}'.format(self.get_token()),
            'X-Union-Appid': self.appId
        }
        response = requests.get(url, headers=headers)
        response_val = eval(response.text)
        return response_val

    def send_message(self, message: str):
        headers = {
            'Authorization': 'QQBot {}'.format(self.get_token()),
            'X-Union-Appid': self.appId
        }
        data = {
            'content': message
        }
        for guild in bot.get_guilds():
            for channel in bot.get_channels(guild['id']):
                if channel['name'] == CHANNEL_NAME:
                    print(channel['id'], channel['name'])
                    url = API_URL+'/channels/{}/messages'.format(channel['id'])
                    response = requests.post(url, headers=headers, data=data)
                    pass


if __name__ == '__main__':
    with open('qq_bot.json', 'r') as file:
        data = json.load(file)
    bot = QQBot(**data)
    bot.send_message('hello')
