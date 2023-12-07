import asyncio
import user_loop


async def main(user_list):
    tasks = [asyncio.create_task(user_loop.user_loop(id)) for id in user_list]
    done, pending = await asyncio.wait(tasks)


asyncio.run(main([23119645]))
