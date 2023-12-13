import asyncio
from bilibili_api import user


class UserList:
    class Agent:
        def __init__(self, uid, u: user.User, info, dynamics):
            self.uid = uid
            self.u = u
            self.info = info
            self.dynamics = dynamics

    def __init__(self, uid_file, sleep_time=5, callback=print, need_wait=False, logger=print):
        self.uid_file = uid_file
        with open(uid_file, 'r') as f:
            self.uid_list = list(map(int, f.read().split()))
        self.sleep_time = sleep_time
        self.callback = callback
        self.need_wait = need_wait
        self.logger = logger
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
                    self.logger(f'dynamics: {dynamic}')
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
                    if self.need_wait:
                        await self.callback(message)
                    else:
                        self.callback(message)
            if page['has_more'] != 1:
                break
            offset = page['next_offset']

    async def _add(self, uid):
        assert all(uid != agent.uid for agent in self._all)
        u = user.User(uid)
        info = await u.get_user_info()
        dynamics = await self._get_first_page(u)
        self.logger('user {} load {} dynamics'.format(
            info['name'], len(dynamics)))
        self._all.append(self.Agent(uid, u, info, dynamics))

    def save(self):
        str = '\n'.join(f'{agent.uid}' for agent in self._all)
        with open(self.uid_file, 'w') as f:
            f.write(str)

    async def load(self):
        for id in self.uid_list:
            await self._add(id)

    async def _loop(self):
        while True:
            for agent in self._all:
                await self._get_new_dynamics(agent)
            await asyncio.sleep(self.sleep_time)

    def start_loop(self):
        asyncio.ensure_future(self._loop())

    def get_list(self):
        l = ['{} {}'.format(agent.uid, agent.info['name'])
             for agent in self._all]
        return '\n'.join(l)

    def get_name_by_uid(self, uid):
        for agent in self._all:
            if agent.uid == uid:
                return agent.info['name']
        return None

    async def add_uid(self, uid):
        await self._add(uid)
        self.save()


if __name__ == '__main__':

    async def main():
        user_list = UserList('user_list.txt')
        await user_list.load()
        user_list.start_loop()
        while True:
            pass

    asyncio.run(main())
