from utils.log import logger
from aiohttp import web
import asyncio


async def index(request):
    return web.Response(body='Awesome')


async def init():
    app = web.Application()
    app.add_routes([web.get("/", index)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 9000)
    await site.start()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    logger.info("Server up and running")
    loop.run_forever()
