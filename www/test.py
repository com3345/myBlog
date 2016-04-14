import orm
import asyncio
import sys
from models import User, Blog, Comment


async def test(loop):
    await orm.create_pool(loop=loop, user='root', password='', database='myBlog')
    u = User(admin=False, name='Test2', email='test2@example.com', passwd='1234567890', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)
