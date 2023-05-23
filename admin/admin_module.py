import hashlib,binascii
from sqlite3.dbapi2 import connect
from flask import Blueprint, blueprints,request
import sqlite3 as sql
from flask.json import jsonify
from os import urandom as randbytes

import json
import datetime, pytz
from os import mkdir
import hashlib
import uuid

admin_bp=Blueprint('admin',__name__)

@admin_bp.route('/sql_console',methods=['POST'])
def console():
    info=request.form.to_dict()
    key=hashlib.sha256(info['key'].encode()).hexdigest()
    key2=hashlib.sha256(info['key2'].encode()).hexdigest()
    command=info['command']
    arg=info['arg']
    d={'ban_account':ban_account,
    'ban_article':ban_article,
    'reg':reg,
    'admin':set_admin}


    if key=='47e53b08c816898a7bf35236c6bdf70982d3ec62cdfc76128a3dff23604b4938'\
        and key2=='138c0b80064ef77fc282123efb5e2391a322acd44f304633db23ed9b195f6f6f':
        f=d[command]
        ret=f(arg)
        return jsonify(ret)
    else:
        return jsonify(msg='fuck off')

def ban_account(username):
    db1=sql.connect('./databases/user_basic.db')
    db1.execute('update users set is_banned=1 where username=?',[username])
    db1.commit()
    uid=db1.execute('select uid from users where username=?',[username]).fetchall()[0][0]
    db1.close()
    db2=sql.connect('./databases/user_token.db')
    db2.execute('delete from token where uid=?',[uid])
    db2.commit()
    db2.close()
    return {'msg':'success'}

def ban_article(num):
    db=sql.connect('./databases/articles.db')
    db.execute('delete from articles where num=?',[num])
    db.commit()
    db.close()
    return {'msg':'success'}

def reg(arg:str):
    args=arg.split(';')
    uname=args[0]
    email=args[1]
    pwd=hashlib.sha256(args[2].encode()).hexdigest()
    nickname=args[3]

    udb=sql.connect('./databases/user_basic.db')
    c=udb.execute('SELECT * FROM users WHERE username=? OR email=?',[uname,email])
    rel_len=len(c.fetchall())
    if rel_len==0:
        #avatar='https://imgs.aixifan.com/newUpload/54612354_c376fd5211dc4b9691c2cd6643026b48.png' # 阿卡林
        avatar = 'https://imgs.aixifan.com/newUpload/54612354_34a010f44e47485cba058455f394dfa4.png'
        uid=hashlib.md5((uname+email+''.join(str(uuid.uuid4()).split('-'))).encode()).hexdigest() # 分配uid
        udb.execute('INSERT INTO users (uid,username,email,pwd,is_admin,is_official,is_virtual,is_banned) VALUES (?,?,?,?,?,?,?,?)',
        [uid,uname,email,pwd,0,0,0,0])
        udb.commit()
        udb.close()

        udb2=sql.connect('./databases/user_info.db')
        u2_cur=udb2.cursor()
        u2_cur.execute('insert into users (uid,username,email,nickname,gender,birthday,avatar,slogan) values (?,?,?,?,?,?,?,?)',
        [uid,uname,email,nickname,0,'2005-01-01',avatar,'天下魔怔壬是一家'])
        udb2.commit()
        udb2.close()
    else:
        return {"errcode":200,"msg":"user already exists"}
    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_cur=tdb.cursor()
        
    token=binascii.hexlify(hashlib.pbkdf2_hmac('sha256',uname.encode(),
            hashlib.md5(randbytes(16)).digest(),10)).decode()
    t_cur.execute('INSERT INTO token (uid,token) VALUES (?,?)',[uid,token])
    tdb.commit() # 保存更改
    tdb.close()
    return {'token':token}

def set_admin(args):
    username,key3=map(str,args.split())
    if key3=='b9777226d0e048c71ca4abfdde5a4c32fee5a9576ae1295e0433574d81041fde':
        db=sql.connect('./databases/user_basic.db')
        db.execute('update users set is_admin=1 where username=?',[username])
        db.commit()
        db.close()
        ret={'errcode':0,'msg':'success'}
    else:
        ret={'errcode':1145,'msg':'fuck off'}
    return ret

@admin_bp.route('/announcement',methods=['POST'])
def post_announcement():
        data=request.form.to_dict()
        key=hashlib.sha256(data['key'].encode()).hexdigest()
        key2=hashlib.sha256(data['key2'].encode()).hexdigest()
        if not(key=='47e53b08c816898a7bf35236c6bdf70982d3ec62cdfc76128a3dff23604b4938'\
        and key2=='138c0b80064ef77fc282123efb5e2391a322acd44f304633db23ed9b195f6f6f'):
            return jsonify(msg="fuck off")
        content=data['content']
        uname=data['uname']
        title=data['title']
        section=-1
        tags='官方公告'
        desc='官方公告'
        
        curtime=datetime.datetime.now().replace(tzinfo=pytz.timezone('Asia/Chongqing')).strftime('%Y-%m-%d')

        current_post_num=114514
        with open('blog_num.txt','r') as f:
            current_post_num=int(f.read())
            f.close()
        current_post_num+=1
        with open('blog_num.txt','w') as f:
            f.write(str(current_post_num))
        mkdir('./articles/'+str(current_post_num))

        with open('./articles/'+str(current_post_num)+'/article.txt','w',encoding='utf-8') as f:
            f.write(content)
            f.close()
        with open('./articles/'+str(current_post_num)+'/comment.json','w',encoding='utf-8') as f:
            d={'comments':[{'id':0,'uname':'bishi','content':'初始化评论区！','time':curtime}]}
            j=json.dumps(d)
            f.write(j)
            f.close()
        
        ardb=sql.connect('./databases/articles.db')
        ardb.execute('insert into articles (num,uid,username,date,title,section,tags,description) values (?,?,?,?,?,?,?,?)',
        [current_post_num,1,uname,curtime,title,section,tags,desc])
        ardb.commit()
        ardb.close()
        ret={'errcode':0,'msg':''}

        return jsonify(ret)