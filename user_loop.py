from asyncio import sleep
from bilibili_api import user, sync


class UserList:
    class Agent:
        def __init__(self, uid, u: user.User, info, dynamics):
            self.uid = uid
            self.u = u
            self.info = info
            self.dynamics = dynamics

    def __init__(self, uid_list, callback=print, sleep_time=10):
        self.uid_list = uid_list
        self.callback = callback
        self.sleep_time = sleep_time
        self._all = []

    async def _get_all_dynamics(self, u: user.User):
        offset = 0
        dynamics = []
        while True:
            page = await u.get_dynamics(offset)
            if 'cards' in page:
                dynamics.extend(page['cards'])
            if page['has_more'] != 1:
                break
            offset = page['next_offset']

        return dynamics

    async def _get_new_dynamics(self, agent: Agent):
        offset = 0
        while True:
            page = await agent.u.get_dynamics(offset)
            if 'cards' in page:
                for card in page['cards']:
                    if card['desc']['rid'] not in map(lambda x: x['desc']['rid'], agent.dynamics):
                        self.callback(card)
                    else:
                        return
            if page['has_more'] != 1:
                break
            offset = page['next_offset']

    async def _loop(self):
        for id in self.uid_list:
            u = user.User(id)
            info = await u.get_user_info()
            dynamics = await self._get_all_dynamics(u)
            print('user {} has {} dynamics'.format(
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
