import asyncio
import user_loop


async def main(user_list):
    tasks = [asyncio.create_task(user_loop.user_loop(id)) for id in user_list]
    await asyncio.wait(tasks)

with open('user_list') as f:
    user_list = list(map(int, f.read().split()))

asyncio.run(main(user_list))
