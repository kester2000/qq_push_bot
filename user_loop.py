import time
from bilibili_api import user, sync


async def check_update(u: user.User, info, callback, last_dynamics):
    offset = 0

    dynamics = []

    loop = True
    while loop:
        # 获取该页动态
        page = await u.get_dynamics(offset)

        now_dynamics = page.get('cards', None)
        if now_dynamics:
            for dynamic in now_dynamics:
                if dynamic['desc']['rid'] not in map(lambda x: x['desc']['rid'], last_dynamics):
                    dynamics.append(dynamic)
                    if last_dynamics:
                        callback(dynamic)
                        loop = False
                    pass

        if not loop:
            break

        if page['has_more'] != 1:
            print('user {} init len {}'.format(info['name'], len(dynamics)))
            break

        offset = page['next_offset']

    return dynamics+last_dynamics


async def user_loop(user_id, callback=print, sleep_time=10):
    u = user.User(user_id)
    info = await u.get_user_info()
    dynamics = []
    while True:
        dynamics = await check_update(u, info, callback, dynamics)
        time.sleep(sleep_time)


if __name__ == '__main__':
    sync(user_loop(23119645))
