import hashlib, binascii, time, calendar
import sqlite3 as sql
from flask import Blueprint
from os import urandom as randbytes
from flask.json import jsonify

lc_bp=Blueprint('captcha',__name__)

@lc_bp.route('/fetch_question')
def fetch_question(args=(), **kwargs):
    question_db=sql.connect('./databases/question.db')

    question_db.row_factory=sql.Row
    q_cur=question_db.cursor()

    q_cur.execute('SELECT * FROM questions ORDER BY RANDOM() limit 1',parameters=args) # 随机跳题（？）
    rows=q_cur.fetchall()

    num=rows[0][0]
    content=rows[0][1]
    descr=rows[0][2]
    q_args=rows[0][3]
    ans=rows[0][4]

    ret=__gen_key(question_num=num,question_ans=ans)

    return jsonify({
        "errcode":0,
        "random":ret['random'],
        "key":ret['key'],
        "content":content,
        "desc":descr,
        "args":q_args
    })

def __gen_key(question_ans:str, args=(), **kwargs):
    random=hashlib.sha1(randbytes(16)).hexdigest()
    pwd=question_ans+random
    key=hashlib.sha256(pwd.encode()).hexdigest()

    return({
        "key":key,
        "random":random
    }
    )