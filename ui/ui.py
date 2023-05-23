from genericpath import isfile
from sqlite3.dbapi2 import DatabaseError, Date
from typing import NamedTuple
from flask import Blueprint, json, jsonify, redirect, render_template, request, session
import sqlite3 as sql
import hashlib
from os import listdir
from os.path import isfile
from os import urandom as randbytes
import time
from random import sample
from bs4 import BeautifulSoup
import lxml

ui = Blueprint('ui', __name__)


@ui.route('/forum', methods=['GET'])
def articles():
    files = []
    with open('./pics.txt', 'r') as f:
        files = f.readlines()
        f.close()
    db = sql.connect('./databases/articles.db')
    db.row_factory = sql.Row

    data = db.execute('SELECT num,title,username,date FROM articles ORDER BY RANDOM() limit 20').fetchall()
    db.close()
    db = sql.connect('./databases/threads.db')
    data2 = db.execute('select id,title,desc,date from threads order by random() limit 30').fetchall()
    db.close()

    announcement_flag = 0
    try:
        with open('./announcement.txt', 'r', encoding='utf-8') as f:
            announcement = f.readlines()
            f.close()
    except:
        f.close()
        announcement_flag = 0
    announcement_flag = 0 if len(announcement) < 2 else 1
    return render_template('article_list.html', articles=data, filename=sample(files, 1)[0], threads=data2,
                           a_flag=announcement_flag, announcement=announcement)


@ui.route('/massive/<id>', methods=['GET'])
def massive(id):
    type_ = request.args.get('type')
    try:
        with open('./upload/text/' + id + '.txt', encoding='utf-8') as f:
            _content = f.read()
            if type_ == 'img':
                content = _content.strip().split('\n')
                author = content[-1]
                del content[-1]
                ret = render_template('massive_img.html', pictures=content, author=author)
            else:
                ret = '<p style="word-wrap: break-word; white-space: pre-wrap;">' + _content + '</p>'
            f.close()
    except:
        ret = render_template('error.html',
                              error_msg="可能是编码有问题。请确保使用了utf-8编码。")
    return ret


@ui.route('/articles/<num>')
def view_article(num):
    db = sql.connect('./databases/articles.db')
    db.row_factory = sql.Row

    _data = db.execute('SELECT title,username,date,description,section,tags FROM articles where num=? limit 1',
                       [num]).fetchall()
    if len(_data) == 0:
        return render_template('error.html', error_msg="文章不存在")
    data = _data[0]
    db.close()
    try:
        with open('./articles/' + num + '/article.txt', 'r', encoding='utf-8') as f:
            _content = f.readlines()
            f.close()
        with open('./articles/' + num + '/comment.json', 'r', encoding='utf-8') as f:
            j = json.load(f)
            f.close()
    except:
        return render_template('error.html', error_msg="文章不存在或已被橄榄")
    content = list()
    for c in _content:
        if c[0:5] == '[img]':
            content.append(('img', c[5:]))
        elif c[0:8] == '[iframe]':
            content.append(('iframe', iframe_parser(c[8:])))
        elif c[0:11] == '[mass-text]':
            content.append(('mt', c[11:]))
        elif c[0:10] == '[mass-img]':
            content.append(('mi', c[10:]))
        elif c[0:6] == '[head]':
            content.append(('img', c[6:]))
        else:
            content.append(('text', c))

        sections = ['默认',
                    '校内',
                    'ACG',
                    '文艺',
                    '技术',
                    '水贴',
                    '反馈']
        section = sections[int(data[4])]
        if int(data[4]) == -1:
            section = '公告'

    return render_template('article_viewer.html', title=data[0], username=data[1],
                           date=data[2], description=data[3], section=section, tags=data[5], lines=content, num=num, \
                           comments=j['comments'])


@ui.route('/users/<uname>')
def user(uname):
    db = sql.connect('./databases/user_info.db')
    r = db.execute('select username,nickname,email,avatar,slogan,gender,birthday from users where username=? or uid=?',
                   [uname, uname]
                   ).fetchall()[0]
    db.close()
    db = sql.connect('./databases/articles.db')
    r1 = db.execute('select num,title,date from articles where username=?', [uname]).fetchall()
    try:
        return render_template('user.html', nickname=r[1], username=r[0],
                               avatar=r[3], slogan=r[4], email=r[2], gender=r[5], birthday=r[6], articles=r1)
    except:
        return render_template("error.html", error_msg="查无此人")


@ui.route('/search')
def search():
    return render_template('search_from.html')


@ui.route('/captcha')
def captcha():
    data = req_parse(request)
    url_to = data.get('url_to')

    question_db = sql.connect('./databases/question.db')

    question_db.row_factory = sql.Row
    q_cur = question_db.cursor()

    q_cur.execute('SELECT * FROM questions ORDER BY RANDOM() limit 1')  # 随机跳题（？）
    rows = q_cur.fetchall()

    num = rows[0][0]
    desc = rows[0][1]
    ans = rows[0][4]

    key, random, timestamp = __gen_key(question_num=num, question_ans=ans)
    return render_template('captcha.html', content=desc, key=key, random=random, timestamp=timestamp, url_to=url_to)


@ui.route('/cookie')
def set_cookie():
    return render_template('cookie_setter.html')


@ui.route('/cookie_setter')
def cookie_redirect():
    c = request.args.get('cookie')
    session.permanent = True
    session['token'] = c  # 设置session（使用SECRET_KEY加密）
    return redirect('/ui/forum')


@ui.route('/clear_cookie')
def clear_cookie():
    confirm = request.args.get('confirm')
    if confirm == '1':
        session.clear()
        return redirect('/ui/forum')
    else:
        return ('<a href="/ui/clear_cookie?confirm=1" style="color: rgb(255,0,0);">确认清除（不可逆！）</a>')


@ui.route('/write')
def write():
    '''
    random=request.args.get('random')
    ans=request.args.get('ans')
    key=request.args.get('key')
    timestamp=request.args.get('timestamp')
    if not captcha_verify(random,ans,key,timestamp):
        return ('人机校验错误！')
    else:session['captcha_passed']='true'
    '''
    return render_template('write.html')  # random=random,ans=ans,key=key,timestamp=timestamp)


@ui.route('/login')
def login():
    return render_template('login.html')


@ui.route('/upload')
def upload():
    return render_template('upload_massive.html')


@ui.route('/space')
def space():  # 个人中心
    token = session.get('token')
    if token == None: return render_template('error.html', error_msg="你还没有登录！")

    tdb = sql.connect('./databases/user_token.db')
    tdb.row_factory = sql.Row
    t_info = tdb.execute('select uid from token where token=? limit 1', [token]).fetchall()
    tdb.close()

    if len(t_info) == 0: return render_template('error.html', error_msg="token 有误！")
    uid = t_info[0][0]

    udb = sql.connect('./databases/user_info.db')
    u_info = udb.execute('select nickname,birthday,gender,slogan,avatar from users where uid=?', [uid]).fetchall()
    udb.close()

    nickname = u_info[0][0]
    birthday = u_info[0][1]
    gender = u_info[0][2]
    slogan = u_info[0][3]
    avatar = u_info[0][4]

    return render_template('settings.html',
                           nickname=nickname, birthday=birthday, gender=gender, slogan=slogan, avatar=avatar)


@ui.route('/new_thread')
def new_thread():
    return render_template('new_thread.html')


@ui.route('/thread/<num>', methods=['GET'])
def thread(num):
    _page = request.args.get('page')
    adb = sql.connect('./databases/articles.db')

    query = '[thread:{}]%'.format(num)
    _q = '[thread:{}]'.format(num)

    _articles = adb.execute('select num,title,username,date from articles where title like ?', [query]).fetchall()
    adb.close()
    thread_db = sql.connect('./databases/threads.db')
    _thread = thread_db.execute('select id, title, author, desc from threads where id=?', [num]).fetchall()
    thread_db.close()
    if len(_thread) == 0:
        return render_template('error.html', error_msg="未知的讨论串")
    pages = len(_articles) // 10 + 1
    use_previous = 1
    use_next = 1
    if _page == None:
        page = 1
    else:
        page = int(_page)
    if page <= 1:
        page = 1
        use_previous = 0
    if page >= pages:
        page = pages
        use_next = 0

    articles = _articles[(page - 1) * 10:page * 10 + 1]

    content = []
    for a in articles:
        with open('./articles/{}/article.txt'.format(a[0]), 'r', encoding='utf-8') as f:
            ar = f.read()[0:500].split('\n')
            head_img = ar[0]
            use_head_img = 0
            if head_img[0:6] == '[head]':
                use_head_img = 1
                head_img = head_img[6:]
                del ar[0]
            f.close()
        with open('./articles/{}/comment.json'.format(a[0]), 'r', encoding='utf-8') as f:
            _j = json.load(f)
            f.close()
        comment = _j['comments'][0:51]
        content.append((a[1].replace(_q, ''), a[2], a[3], ar, comment, a[0], use_head_img, head_img))
    with open('./articles/threads/{}.json'.format(num), 'r', encoding='utf-8') as f:
        _j = json.load(f)
        f.close()
        base_comments = _j['comments']

    return render_template('thread.html',
                           num=num, page=int(page), pages=int(pages), id=_thread[0][0], title=_thread[0][1],
                           author=_thread[0][2], desc=_thread[0][3], content=content, base_comments=base_comments,
                           use_previous=use_previous, use_next=use_next)


@ui.route('/docs')
def doc_list():
    li = listdir('./docs')
    str_ = '<h1>魔怔bbs 文档</h1>'
    for i in li:
        str_ += '<h3><a href="/ui/docs/{}">{}</a></h3>'.format(i, i.replace('.html', ''))
    return str_


@ui.route('/docs/<fname>')
def doc(fname):
    if isfile('./docs/{}'.format(fname)):
        with open('./docs/' + fname, 'r', encoding='utf-8') as f:
            content = f.read()
            f.close()
        return content
    else:
        return render_template('404.html')


def captcha_verify(random, ans, key, timestamp):
    pwd = ans + random + timestamp
    key_user = hashlib.sha256(pwd.encode()).hexdigest()

    return key == key_user and int(timestamp) + 60 >= int(time.time())


def __gen_key(question_ans: str, args=(), **kwargs):
    timestamp = time.time()
    random = hashlib.sha1(randbytes(16)).hexdigest()
    pwd = question_ans + random + str(int(timestamp))  # 密码结构：答案+随机的玩意+时间戳
    key = hashlib.sha256(pwd.encode()).hexdigest()

    return (key, random, str(int(timestamp)))


def req_parse(req):
    if req.method == 'GET':
        data = req.args
    if req.method == 'POST':
        data = req.form.to_dict()
    return data


def iframe_parser(src):
    try:
        soup = BeautifulSoup(src, 'lxml')
        iframe = str(soup.iframe)
        for i in soup.iframe.descendants:
            if str(i) not in (' ', ''):
                iframe = iframe.replace(str(i), '')
        ret = iframe
    except:
        ret = 'none'
    return ret
