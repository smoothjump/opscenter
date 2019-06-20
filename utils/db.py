from utils.log import logger
import asyncio
import aiomysql


async def create_pool(**kw):
    logger.info('Initialize database connection pool...')
    global __pool
    loop = asyncio.get_event_loop()
    __pool = await aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 2),
        loop=loop
    )


async def select(sql, args=None, size=None):
    logger.info(sql)
    logger.info('Parameter: %s' % str(args))
    async with __pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            if args:
                await cur.execute(sql.replace('?', '%s'), args or ())
            else:
                await cur.execute(sql)
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
            logger.info('Rows returned: %s' % len(rs))
            await cur.close()
            logger.debug('Returned dataset: %s' % str(rs))
        return rs


async def execute(sql, args=None):
    logger.info(sql)
    logger.info('Parameter: %s' % str(args))
    async with __pool.acquire() as conn:
        try:
            cur = await conn.cursor()
            if args:
                await cur.execute(sql.replace('?', '%s'), args)
            else:
                await cur.execute(sql)
            affected = cur.rowcount
            await cur.close()
            logger.debug('Affected rows: %s' % str(affected))
        except BaseException as e:
            raise(e)
        return affected


def create_args_string(num):
    L = []
    for n in range(num):
        L.append('?')
    return ', '.join(L)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_pool(user='root', password='123', db='ops'))
    loop.run_until_complete(select("select * from user where reserved=?", args=(12.34)))
    # loop.run_until_complete(execute("insert into test values(?, ?)", args=[2, "RRT"]))
    loop.run_until_complete(execute("show tables"))
