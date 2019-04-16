import asyncio
import threading


async def hello1():
    print("Hello....", threading.current_thread())
    y = await asyncio.sleep(5)
    print("Hello again....", threading.current_thread())

async def hello2():
    print("Hello....", threading.current_thread())
    y = await asyncio.sleep(5)
    print("Hello again....", threading.current_thread())

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait([hello1(), hello2()]))
loop.close()