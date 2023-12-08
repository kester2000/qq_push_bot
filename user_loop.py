from asyncio import sleep
from bilibili_api import user, sync


class UserList:
    class Agent:
        def __init__(self, uid, u: user.User, info, dynamics):
            self.uid = uid
            self.u = u
            self.info = info
            self.dynamics = dynamics

    def __init__(self, uid_list, callback=print, sleep_time=5):
        self.uid_list = uid_list
        self.callback = callback
        self.sleep_time = sleep_time
        self._all = []

    async def _get_first_page(self, u: user.User):
        offset = 0
        dynamics = []
        page = await u.get_dynamics(offset)
        if 'cards' in page:
            dynamics.extend(page['cards'])
        return dynamics

    async def _get_new_dynamics(self, agent: Agent):
        offset = 0
        while True:
            page = await agent.u.get_dynamics(offset)
            if 'cards' in page:
                for dynamic in page['cards']:
                    if dynamic['desc']['rid'] in map(lambda x: x['desc']['rid'], agent.dynamics):
                        return
                    agent.dynamics.append(dynamic)
                    # with open('output.json', mode='w') as f:
                    #     f.write(json.dumps(dynamic, ensure_ascii=False))
                    type = dynamic['desc']['type']
                    user_name = dynamic['desc']['user_profile']['info']['uname']
                    if dynamic['desc']['type'] == 8:
                        # video
                        title = dynamic['card']['title']
                        desc = dynamic['card']['desc']
                        message = '{}发布了视频\n标题：{}\n简介：{}'.format(
                            user_name, title, desc)
                    elif dynamic['desc']['type'] == 4:
                        # messege
                        content = dynamic['card']['item']['content']
                        message = '{}发布了文字\n内容：{}'.format(user_name, content)
                    elif dynamic['desc']['type'] == 2:
                        # image
                        message = '{}发布了图片'.format(user_name)
                    else:
                        message = '{}发布了未知类型[{}]的动态'.format(user_name, type)
                    self.callback(message)
            if page['has_more'] != 1:
                break
            offset = page['next_offset']

    async def _loop(self):
        for id in self.uid_list:
            u = user.User(id)
            info = await u.get_user_info()
            dynamics = await self._get_first_page(u)
            print('user {} load {} dynamics'.format(
                info['name'], len(dynamics)))
            self._all.append(self.Agent(id, u, info, dynamics))
        while True:
            for agent in self._all:
                await self._get_new_dynamics(agent)
            await sleep(self.sleep_time)

    def run_loop(self):
        sync(self._loop())


if __name__ == '__main__':
    user_list = UserList([23119645, 1583832354])
    user_list.run_loop()
