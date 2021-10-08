import asyncio
import time

async def say_after(delay, what):
    print("wait...")
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    await say_after(3, 'wait three second 1')
    await say_after(3, 'wait three second 2')
    await say_after(3, 'wait three second 3')
    # -> worker가 하나
    print(f"finished at {time.strftime('%X')}")

    task1 = asyncio.create_task(say_after(3, 'wait three second 1'))
    task2 = asyncio.create_task(say_after(3, 'wait three second 2'))
    task3 = asyncio.create_task(say_after(3, 'wait three second 3'))
    print(f"started at {time.strftime('%X')}")

    await task1
    await task2
    await task3
    # worker가 3개
    print(f"finished at {time.strftime('%X')}")


if __name__ == '__main__':
    asyncio.run(main())