import asyncio
import time
import anyio

from anyio import Event, create_task_group, run, sleep


async def task(event: Event, number: int):
    print('Task', number, 'is waiting')
    await event.wait()
    print('Task', number, 'finished')


async def main():
    event = Event()
    async with create_task_group() as tg:
        for i in range(100):
            tg.start_soon(task, event, i)

        await sleep(1)
        await event.set()
    print(event)
if __name__ == '__main__':
    run(main)
