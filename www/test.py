import orm
import asyncio
import sys
from models import User, Blog, Comment

# import pymysql

# conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='', db='myBlog')
# cur = conn.cursor()
# cur.execute("""SELECT * FROM users""")
# for r in cur.fetchall():
#     print(r)
# cur.close()
# conn.close()

async def test(loop):
    await orm.create_pool(loop=loop, user='root', host='127.0.0.1', port=3306, password='', db='myBlog')
    u = User(admin=False, name='Test3', email='test3@example.com', passwd='1234567890', image='about:blank')
    await u.save()

loop = asyncio.get_event_loop()
loop.run_until_complete(test(loop))
loop.close()
if loop.is_closed():
    sys.exit(0)
