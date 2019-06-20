from utils.log import logger
from aiohttp import web
import asyncio
from utils.db import create_pool
from models.model import Users


async def index(request):
    user = Users(name="BBB", email="1@1.cn")
    await user.save()
    return web.Response(body='Awesome')


async def ui(request):
    return web.Response()


async def init():
    app = web.Application()
    app.add_routes([web.get("/", index)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 9000)
    await site.start()
    await create_pool(user='root', password='123', db='ops')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
    logger.info("Server up and running")
    loop.run_forever()
