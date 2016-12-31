#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from coroweb import get, post
from models import User, Blog, Comment, next_id
from aiohttp import web
from apis import APIValueError, APIPermissionError, Page
from markdown2 import markdown

from subprocess import run
import time
import re
import json
import hashlib
import logging
import MeCab
import json
from datetime import datetime, timedelta
import os

from stopwords import stopwordslist
from config import configs

COOKIE_NAME = 'myBlogsession'
_COOKIE_KEY = configs.session.secret


BOSS_CD = {
    "nube": ("努贝尔(ヌベール)", 9, 4),
    "kutu": ("库图姆(クツム)", 9, 3),
    "kuza": ("库扎卡(クザカ)", 8, 4),
    "kara": ("卡兰达(カランダ)", 15, 3)
}

_RE_EMAIL = re.compile(r'[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile(r'^[0-9a-f]{40}$')


def _not_in_black_list(word):
    n = len(word)
    if n == 1 and 0x3041 <= ord(word) <= 0x3093:
        return False
    if n == 1 and word.isalpha() or word.isdigit():
        return False
    if word in stopwordslist:
        return False
    return True


@get('/api/crawl_boss')
def api_crawl_boss():
    if os.path.exists("bossinfo.json"):
        run("rm bossinfo.json", shell=True)

    run("scrapy crawl bdspider -o ../bossinfo.json", shell=True, cwd="./bossSpider")
    with open("bossinfo.json") as data_file:
        data = json.load(data_file)
    run("rm bossinfo.json", shell=True)

    bosses = [(
        el["boss"],
        BOSS_CD[el["boss"]][0],
        el["last_time"],
        el["last_time"] + timedelta(hours=BOSS_CD[el["boss"]][1]).total_seconds(),
        BOSS_CD[el["boss"]][2]) for el in data]
    logging.info({boss[0]: boss[1:] for boss in bosses})
    return {boss[0]: boss[1:] for boss in bosses}


@get('/bdo_boss')
def bosspage():
    return {
        '__template__': 'bdo_boss.html'
    }


def parse(c):
    nouns, verbs = set(), set()
    mt = MeCab.Tagger()
    for line in mt.parse(c).splitlines()[:-1]:
        word, attrs = line.split()[:2]
        if attrs[:2] == '名詞' and _not_in_black_list(word) and word not in nouns:
            nouns.add(word)
        if attrs[:2] == '動詞' and _not_in_black_list(word) and word not in verbs:
            verbs.add(word)
    return list(nouns), list(verbs)


def check_admin(request):
    if request.__user__ is None or not request.__user__.admin:
        raise APIPermissionError()


def get_page_index(page_str):
    p = 1
    try:
        p = int(page_str)
    except ValueError as e:
        pass
    if p < 1:
        p = 1
    return p


def user2cookie(user, max_age):
    # build cookie string by: id-expires-sha1
    expires = str(int(time.time() + max_age))
    s = '%s-%s-%s-%s' % (user.id, user.passwd, expires, _COOKIE_KEY)
    L = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
    return '-'.join(L)


def text2html(text):
    lines = map(
        lambda s: '<p>%s</p>' % s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'),
        filter(lambda s: s.strip() != '', text.split('\n'))
    )
    return ''.join(lines)


async def cookie2user(cookie_str):
    if not cookie_str:
        return None
    try:
        L = cookie_str.split('-')
        if len(L) != 3:
            return None
        uid, expires, sha1 = L
        if int(expires) < time.time():
            return None
        user = await User.find(uid)
        if user is None:
            return None
        s = '%s-%s-%s-%s' % (uid, user.passwd, expires, _COOKIE_KEY)
        if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
            logging.info('invalid sha1')
            return None
        user.passwd = '******'
        return user
    except Exception as e:
        logging.exception(e)
        return None


@get('/mecab')
def mecabpage():
    return {
        '__template__': 'mecab.html'
    }


@get('/info')
def information():
    return {
        '__template__': 'info.html'
    }


@get('/')
async def index(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    page = Page(num, page_index)
    if num == 0:
        blogs = []
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(page.offset, page.limit))
    return {
        '__template__': 'blogs.html',
        'page': page,
        'blogs': blogs
    }


@get('/manage/')
def manage():
    return 'redirect:/manage/comments'


@get('/signin')
async def signin():
    return {
        '__template__': 'signin.html'
    }


@get('/signout')
def signout(request):
    referer = request.headers.get('Referer')
    r = web.HTTPFound(referer or '/')
    r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
    logging.info('user signed out.')
    return r


@get('/register')
async def register():
    return {
        '__template__': 'register.html'
    }


@get('/api/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, users=())
    users = await User.findAll(orderBy='created_at desc')
    for u in users:
        u.passwd = '*******'
    return dict(page=p, users=users)


@post('/api/parse')
def api_parse_text(*, content):
    content = content.strip()
    if not content:
        raise APIValueError('content', 'content cannot be empty.')
    if len(content) > 1000:
        raise APIValueError('content', 'too many words > 1000')

    nouns, verbs = parse(content)
    result = dict(nouns=nouns, verbs=verbs)
    print(result)

    return result


@post('/api/users')
async def api_register_user(*, email, name, passwd):
    if not name or not name.strip():
        raise APIValueError('name')
    if not passwd or not _RE_EMAIL.match(email):
        raise APIValueError('email')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIValueError('passwd')
    users = await User.findAll('email=?', [email])
    if len(users) > 0:
        raise APIError('register:faild', 'email', 'Email is already in use.')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(
        id=uid,
        name=name.strip(),
        email=email,
        passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
        image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest()
    )
    await user.save()
    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email:
        raise APIValueError('email', 'Invalid email.')
    if not passwd:
        raise APIValueError('passwd', 'Invalid password.')
    users = await User.findAll('email=?', [email])
    if len(users) == 0:
        raise APIValueError('email', 'Email not exist.')
    user = users[0]

    sha1 = hashlib.sha1()
    sha1.update(user.id.encode('utf-8'))
    sha1.update(b':')
    sha1.update(passwd.encode('utf-8'))
    if user.passwd != sha1.hexdigest():
        raise APIValueError('passwd', 'Invalid password.')

    r = web.Response()
    r.set_cookie(COOKIE_NAME, user2cookie(user, 8400), max_age=86400, httponly=True)
    user.passwd = '******'
    r.content_type = 'application/json'
    r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
    return r


@get('/blog/{id}')
async def get_blog(id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = markdown(c.content)
    blog.html_content = markdown(blog.content)
    return {
        '__template__': 'blog.html',
        'blog': blog,
        'comments': comments
    }


@get('/api/blogs/{id}')
async def api_get_blog(*, id):
    blog = await Blog.find(id)
    return blog


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
    check_admin(request)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not content.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog = Blog(
        user_id=request.__user__.id,
        user_name=request.__user__.name,
        user_image=request.__user__.image,
        name=name.strip(),
        summary=summary.strip(),
        content=content.strip()
    )
    await blog.save()
    return blog


@get('/manage/blogs/create')
async def manage_create_blog():
    return {
        '__template__': 'manage_blog_edit.html',
        'id': '',
        'action': '/api/blogs'
    }


@get('/api/blogs')
async def api_blogs(*, page='1'):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, blogs=())
    blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/manage/blogs')
async def manage_blogs(*, page='1'):
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@post('/api/blogs/{id}/delete')
async def api_delete_blog(request, *, id):
    check_admin(request)
    blog = await Blog.find(id)
    await blog.remove()
    return dict(id=id)


@post('/api/blogs/{id}')
async def api_update_blog(id, request, *, name, summary, content):
    check_admin(request)
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIValueError('name', 'name cannot be empty.')
    if not summary or not summary.strip():
        raise APIValueError('summary', 'summary cannot be empty.')
    if not content or not content.strip():
        raise APIValueError('content', 'content cannot be empty.')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    await blog.update()
    return blog


@get('/manage/blogs/edit')
def manage_edit_blog(*, id):
    return {
        '__template__': 'manage_blog_edit.html',
        'id': id,
        'action': '/api/blogs/%s' % id
    }


@get('/api/comments')
async def api_get_comments(*, page='1'):
    page_index = get_page_index(page)
    num = await Comment.findNumber('count(id)')
    p = Page(num, page_index)
    if num == 0:
        return dict(page=p, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, comments=comments)


@get('/manage/comments')
async def get_comments(*, page='1'):
    return {
        '__template__': 'manage_comments.html',
        'page_index': get_page_index(page)
    }


@post('/api/comments/{id}/delete')
async def api_delete_comments(request, *, id):
    check_admin(request)
    comment = await Comment.find(id)
    await comment.remove()
    return dict(id=id)


@post('/api/blogs/{id}/comments')
async def api_create_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIPermissionError('Please signin first.')
    if not content or not content.strip():
        raise APIValueError('content')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceNotFoundError('Blog')
    comment = Comment(
        blog_id=blog.id,
        user_id=user.id,
        user_name=user.name,
        user_image=user.image,
        content=content.strip()
    )
    await comment.save()
    return comment


@get('/manage/users')
async def get_users(*, page='1'):
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }
