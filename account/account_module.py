import hashlib,binascii
from flask import Blueprint, redirect, render_template,request, session
import sqlite3 as sql
from flask.json import jsonify
from os import urandom as randbytes
import pytz,datetime
import uuid
# fetchall 使用后 cursor 就变成空的了
# 需要注意

acc_bp=Blueprint('account',__name__)

@acc_bp.route('/login',methods=['POST','GET'])
def login():
    try:
        data=req_parse(request)
        uname=data['username']
        pwd=hashlib.sha256(data['pwd'].encode()).hexdigest()  # 需传 sha256
    except:
        return jsonify(errcode=120,msg='argument missing')

    udb=sql.connect('./databases/user_basic.db')
    udb.row_factory=sql.Row
    
    u_cur=udb.cursor()

    u_cur.execute('SELECT pwd,uid,is_banned FROM users WHERE email=? OR username=?',[uname,uname])
    info=u_cur.fetchall()
    if len(info)==0:
        udb.close()
        return jsonify(errcode=150,msg='Wrong username.')
    rel_pwd=info[0][0] # 密码
    uid=info[0][1] # uid
    is_banned=info[0][2]
    udb.close()
    if is_banned==1:
        udb.close()
        return jsonify(errcode=1200,msg='Your account is no longer avaliable. Please contact admin for further information.')

    if pwd==rel_pwd:
        tdb=sql.connect('./databases/user_token.db')
        tdb.row_factory=sql.Row
        t_cur=tdb.cursor()
        
        token=''.join(str(uuid.uuid4()).split('-'))
        t_cur.execute('INSERT INTO token (uid,token) VALUES (?,?)',[uid,token])
        tdb.commit() # 保存更改
        tdb.close()
        session['token']=token
        session.permanent=True
        '''return jsonify({
            'errcode':0,
            'msg':'success',
            'token':token
        }) if request.method=='POST' else'''
        return '这是你的饼干，请保管好。<br>'+token
    else:
        return jsonify({
            'errcode':200,
            'msg':'wrong pwd or username.'
        })

@acc_bp.route('/sign_up',methods=['POST'])
def sign_up():
    try:
        data=request.form.to_dict()
        uname=data['uname'] # 用户名 唯一
        nickname=data['nickname'] # 昵称
        email=data['email']
        pwd=hashlib.sha256(data['pwd'].encode()).hexdigest() # 加密
        verify_token=data['token']
        verify_code=data['verify']
    except:
        return jsonify(errcode=120,msg='argument missing')

    #print(data)    
    mdb=sql.connect('./databases/mail_verify.db')
    mdb.row_factory=sql.Row

    udb=sql.connect('./databases/user_basic.db')
    mdb.row_factory=sql.Row

    mail_cur=mdb.cursor()
    mail_cur.execute('SELECT verify FROM records WHERE token=? LIMIT 1',[verify_token])
    mail_info=mail_cur.fetchall()
    if len(mail_info)==0:
        mdb.close()
        udb.close()
        return jsonify(errcode=110,msg='Wrong token.')
    real_vcode=mail_info[0][0]
    mail_cur.execute('delete from records where token=?',[verify_token])
    mdb.commit()
    
    u_cur=udb.cursor()
    u_cur.execute('SELECT * FROM users WHERE username=? OR email=?',[uname,email])
    rel_len=len(u_cur.fetchall())

    if rel_len==0 and real_vcode==verify_code:
        # avatar='https://imgs.aixifan.com/newUpload/54612354_c376fd5211dc4b9691c2cd6643026b48.png' # 阿卡林
        avatar = 'https://imgs.aixifan.com/newUpload/54612354_34a010f44e47485cba058455f394dfa4.png'
        uid=hashlib.md5((uname+email+''.join(str(uuid.uuid4()).split('-'))).encode()).hexdigest() # 分配uid
        u_cur.execute('INSERT INTO users (uid,username,email,pwd,is_admin,is_official,is_virtual,is_banned) VALUES (?,?,?,?,?,?,?,?)',
        [uid,uname,email,pwd,0,0,0,0])
        udb.commit()
        udb.close()
        mdb.close()

        udb2=sql.connect('./databases/user_info.db')
        u2_cur=udb2.cursor()
        u2_cur.execute('insert into users (uid,username,email,nickname,gender,birthday,avatar,slogan) values (?,?,?,?,?,?,?,?)',
        [uid,uname,email,nickname,0,'2005-01-01',avatar,'天下魔怔壬是一家'])
        udb2.commit()
        udb2.close()
        return jsonify({
            'errcode':0,
            'msg':'success',
            'uid':uid,
        })
    else:
        udb.close()
        mdb.close()
        return jsonify({
            'errcode':200,
            'msg':'email addr occupied or the username is unavailable.'
        })

@acc_bp.route('/user_info',methods=['POST'])
def fetch_user_info():
    try:
        data=request.form.to_dict()
        uid_like=data['uid'] # 此处有两种方式：uid或用户名username
    except:
        return jsonify(errcode=120,msg='argument missing')

    udb=sql.connect('./databases/user_info.db')
    udb.row_factory=sql.Row
    cur=udb.cursor()

    cur.execute('SELECT * FROM users WHERE uid=? or username=?',[uid_like,uid_like])
    _info=cur.fetchall()
    udb.close()
    if len(_info)==0: # 用户不存在
        return jsonify(errcode=200,msg='this user doesn\'t exist.')

    info=_info[0]

    nickname=info['nickname']
    uname=info['username']
    email=info['email']
    avatar=info['avatar']
    gender=info['gender']
    birthday=info['birthday']
    slogan=info['slogan']
    aixifan=info['acfun']
    ruiliruili=info['bilibili']
    wc=info['wechat']
    qq=info['qq']

    return jsonify({
        'errcode':0,
        'msg':'',
        'nickname':nickname,
        'username':uname,
        'email':email,
        'avatar':avatar,
        'gender':gender,
        'birth':birthday,
        'slogan':slogan,
        'ac':aixifan,
        'bili':ruiliruili,
        'wechat':wc,
        'qq':qq
    })

@acc_bp.route('/exit_login',methods=['POST','GET'])
def exit_login():
    try:
        data=req_parse(request)
        #uid=data['uid']
        token=data['token']
    except:
        token=session.get('token')
        if token==None:
            return jsonify(errcode=120,msg='argument missing')
    tdb=sql.connect('./databases/user_token.db')
    tdb.execute('delete from token where token=?',[token])
    tdb.commit()
    tdb.close()

    return jsonify(errcode=0,msg="success") if request.method=="POST"\
        else "你饼干没了！"
@acc_bp.route('/get_permit')
def permit():
    try:
        token=session.get('token')
        if token==None:
            if request.method=="POST":
                return jsonify(errcode=100,msg="wrong token")
            else: 
                return render_template('error.html',error_msg="token 有误！")
    except:
        if request.method=="POST":
            return jsonify(errcode=100,msg="wrong token")
        else: return render_template('error.html',error_msg="token 有误！")
    db=sql.connect('./databases/permit.db')

    r=db.execute('select date from permit where token=?',[token]).fetchall()
    curtime=int(datetime.datetime.now()\
        .replace(tzinfo=pytz.timezone('Asia/Chongqing'))\
            .strftime('%Y%m%d'))
    
    if len(r)==0: # 还没签到
        db.execute('insert into permit (token,date) values (?,?)',[token,curtime])

        session['article_lim']=10 # 发帖
        session['comment_lim']=50 # 发评论
        session['massive_blog_lim']=2 # 发大量文本
        session['new_thread_lim']=1 # 新建讨论串

        session.permanent=True
        ret=jsonify(errcode=0,msg="success") if request.method=='POST'\
            else redirect('/ui/forum')

    elif r[0][0]<curtime:
        db.execute('update permit set date=? where token=?',[int(curtime),token])
        session['article_lim']=5
        session['comment_lim']=20
        session['massive_blog_lim']=5
        session['new_thread_lim']=1 # 新建讨论串
        
        session.permanent=True
        ret=jsonify(errcode=0,msg="success") if request.method=='POST'\
            else redirect('/ui/forum')
    else:
        ret=jsonify(errcode=130,msg="no") if request.method=='POST'\
            else render_template('error.html',error_msg="今天签到过了")

    db.commit()
    db.close()
    return ret

@acc_bp.route('/settings')
def settings():
    data=req_parse(request)

    try:
        token=data['token']
    except:
        token=session.get('token')
        if token==None:
            return jsonify(errcode=120,msg="token missing") if request.method=='POST'\
                else render_template('error.html',error_msg="你还没有登录！")
    
    try:
        nickname=data['nickname']
        birthday=data['birthday']
        gender=int(data['gender'])
        slogan=data['slogan']
        avatar=data['avatar']
    except:
        return jsonify(errcode=150,msg="argument missing") if request.method=='POST'\
            else render_template('error.html',error_msg="请求参数不完整！确保你填写了所有项！")
    
    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select uid from token where token=? limit 1',[token]).fetchall()
    tdb.close()

    if len(t_info)==0:return render_template('error.html',error_msg="token 有误！")
    uid=t_info[0][0]

    udb=sql.connect('./databases/user_info.db')
    udb.execute('update users set nickname=?,birthday=?,gender=?,slogan=?,avatar=? where uid=?',[nickname,birthday,gender,slogan,avatar,uid]).fetchall()
    udb.commit()
    udb.close()

    return jsonify(errcode=0,msg="success") if request.method=="POST"\
        else redirect('/ui/forum')


def req_parse(req):
    if req.method=='GET':
        return req.args
    else:
        return req.form.to_dict()