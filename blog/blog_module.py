import hashlib,binascii
from os import mkdir
from flask import Blueprint, redirect, render_template,request, session
import sqlite3 as sql
from flask.json import jsonify
import datetime,pytz
import uuid

import json

blog_bp=Blueprint('blog',__name__)

@blog_bp.route('post_blog',methods=['POST','GET'])
def post_blog():
    try:
        data=req_parse(request)

        #token=data['token']
        try:
            token=session.get('token') # 使用 cookie
            _limit=session.get('article_lim')
            if token==None or _limit==None:
                return render_template('error.html',
                error_msg="检查饼干是否正确配置，再看看你今天是否签了到。")
            else:
                limit=int(_limit)
        except:
            token=data['token']

        title=data['title'].replace('\n',' ') # 标题
        section=int(data['section']) # 分区
        tags=data['tags'].replace('\n',' ')
        desc=data['description'] # 简介
        content=data['content'].replace('\\n','\n').strip()
        '''
        captcha_ans=data['ans']
            captcha_random=data['random']
            captcha_key=data['key']
            ts=data['timestamp']

            is_passed=session.get('captcha_passed')
            #session.pop('captcha_passed')
        '''
    except:
        if request.method=="POST":
            return jsonify(errcode=120,msg='argument missing')
        else: return render_template('error.html',error_msg="请求参数不完整！把这个发给管理员！"+str(data))
    
    #pwd=captcha_ans+captcha_random+ts
    #key_user=hashlib.sha256(pwd.encode()).hexdigest()

    if (limit<=0):
        #captcha_key!='62fee18c9669ac64d088b0393974141031ee5334281433439fabeff9e60e4bb4': # 密钥测试用 hashlib.sha256('yjsnpi11451419pwd').hexdigest()
        #if request.method=='POST':
            #return jsonify(errcode=160,msg='cannot post more blogs')
        #else:
            return render_template('error.html',error_msg="今天不能再发帖了")
    length=len(content)
    if not(section>=0 or section<=6) or length<=0 or length>=5000:
        return render_template('error.html',error_msg="确保你的字数控制在 0~5000 之间")#jsonify(errcode=200,msg='sth wrong with arguments') if request.method=='POST' else\
              # 分区错误

    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select * from token where token=? limit 1',[token]).fetchall()
    tdb.close()

    if len(t_info)!=0:
        uid=t_info[0][0]
        udb=sql.connect('./databases/user_info.db')
        u_info=udb.execute('select username from users where uid=?',[uid]).fetchall()
        udb.close()
        uname=u_info[0][0]

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
        [current_post_num,uid,uname,curtime,title,section,tags,desc])
        ardb.commit()
        ardb.close()
        ret={'errcode':0,'msg':''}
        session['article_lim']=str(limit-1)
    else:
        return render_template('error.html',error_msg="token 有误！确保你的饼干正确配置")
    return redirect('/ui/articles/'+str(current_post_num))

@blog_bp.route('/comment',methods=['GET','POST'])
def send_comment():
    data=req_parse(request)
    try:
        token=data['token']
    except:
        token=session.get('token')
        if token==None:
            return render_template('error.html',error_msg="确保饼干正确配置")

    try:
        content=data['content']
        target=data['target']
    except:
        return render_template('error.html',error_msg="请求参数有误！") #if request.method=='GET'\
            #else jsonify(errcode=120,msg="argument missing")
    length=len(content)
    if length<=0 or length>=500:
        return render_template('error.html',error_msg="确保评论字数控制在500字以内！")

    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select * from token where token=? limit 1',[token]).fetchall()
    tdb.close()
    try:
        limit=int(session.get('comment_lim'))
    except:
        limit=session.get('comment_lim')
    if limit==None or limit<=0:
        return render_template('error.html',error_msg="你今天不能再发评论了！") #if request.method=='GET'\
            #else jsonify(errcode=150,msg="no more comments today!")

    if len(t_info)!=0:
        uid=t_info[0][0]
        udb=sql.connect('./databases/user_info.db')
        u_info=udb.execute('select username from users where uid=?',[uid]).fetchall()
        udb.close()
        uname=u_info[0][0]

        curtime=datetime.datetime.now().\
            replace(tzinfo=pytz.timezone('Asia/Chongqing')).\
                strftime('%Y-%m-%d')
        fname='./articles/'+target+'/comment.json'
        try:
            with open(fname,'r',encoding='utf-8') as f:
                j=json.load(f)
                f.close()
        except:
            return render_template('error.html',error_msg="文章不存在") #if request.method =="GET"\
                #else jsonify(errcode=130,msg="article missing")
        
        id=len(j['comments'])
        j['comments'].append({"id":id,"uname":uname,"content":content,"time":curtime})
        j_=json.dumps(j)

        with open(fname,'w',encoding='utf-8') as f:
            f.write(j_)

        session['comment_lim']=str(limit-1) # 扣一次发评论机会
        session.permanent=True

        return redirect('/ui/articles/'+target) #if request.method=='GET' \
            #else jsonify(errcode=0,msg="success")

    else:
        return jsonify(errcode=120,msg="wrong token") if request.method=="POST"\
        else render_template('error.html',error_msg="token 有误！确保你的饼干正确配置")

@blog_bp.route('/new_thread',methods=['GET','POST'])
def new_thread():
    data=req_parse(request)
    try:
        token=data['token']
    except:
        token=session.get('token')
        if token==None:
            return render_template('error.html',error_msg="确保饼干正确配置")
    limit=session.get('new_thread_lim')
    
    err_flag=0
    try:
        title=data['title']
        desc=data['description']
        if len(title)>30 or len(desc)>500:
            err_flag=1
    except:
        err_flag=1
    if err_flag:
        return render_template('error.html',error_msg="请求参数有误！") #if request.method=='GET'\
            #else jsonify(errcode=120,msg="argument missing")

    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select * from token where token=? limit 1',[token]).fetchall()
    tdb.close()

    if len(t_info)!=0:
        uid=t_info[0][0]
        udb=sql.connect('./databases/user_info.db')
        u_info=udb.execute('select username from users where uid=?',[uid]).fetchall()
        udb.close()
        uname=u_info[0][0]

        curtime=datetime.datetime.now().\
            replace(tzinfo=pytz.timezone('Asia/Chongqing')).\
                strftime('%Y-%m-%d')
        
        if limit!=None:
            if int(limit)>0:
                session['new_thread_lim']=str(0)
                session.permanent=True

                thread_db=sql.connect('./databases/threads.db')
                id=len(thread_db.execute('select id from threads').fetchall())+1
                thread_db.execute('insert into threads (id,title,desc,author,date) values (?,?,?,?,?)',
                [id,title,desc,uname,curtime])
                thread_db.commit()
                thread_db.close()

                with open('./articles/threads/{}.json'.format(str(id)),'w',encoding='utf-8') as f:
                    d={'comments':[{'id':0,'uname':'bishi','content':'初始化评论区！','time':curtime}]}
                    j=json.dumps(d)
                    f.write(j)
                    f.close()
                return redirect('/ui/thread/'+str(id))
                
            else:
                return render_template('error.html',error_msg="你今天不能创建讨论串了！")

        else:
            return render_template('error.html',error_msg="你还没有签到！")
        
    else:
        return render_template('error.html',error_msg="token 有误！确保你的饼干正确配置")

@blog_bp.route('/comment_thread',methods=['GET','POST'])
def send_comment_thread():
    data=req_parse(request)
    try:
        token=data['token']
    except:
        token=session.get('token')
        if token==None:
            return render_template('error.html',error_msg="确保饼干正确配置")

    try:
        content=data['content']
        target=data['target']
    except:
        return render_template('error.html',error_msg="请求参数有误！") if request.method=='GET'\
            else jsonify(errcode=120,msg="argument missing")
    length=len(content)
    if length<=0 or length>=500:
        return render_template('error.html',error_msg="确保评论字数控制在500字以内！")

    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select * from token where token=? limit 1',[token]).fetchall()
    tdb.close()
    try:
        limit=int(session.get('comment_lim'))
    except:
        limit=session.get('comment_lim')
    if limit==None or limit<=0:
        return render_template('error.html',error_msg="你今天不能再发评论了！") if request.method=='GET'\
            else jsonify(errcode=150,msg="no more comments today!")

    if len(t_info)!=0:
        uid=t_info[0][0]
        udb=sql.connect('./databases/user_info.db')
        u_info=udb.execute('select username from users where uid=?',[uid]).fetchall()
        udb.close()
        uname=u_info[0][0]

        curtime=datetime.datetime.now().\
            replace(tzinfo=pytz.timezone('Asia/Chongqing')).\
                strftime('%Y-%m-%d')
        fname='./articles/threads/{}.json'.format(target)
        try:
            with open(fname,'r',encoding='utf-8') as f:
                j=json.load(f)
                f.close()
        except:
            return render_template('error.html',error_msg="串不存在") if request.method =="GET"\
                else jsonify(errcode=130,msg="thread missing")
        
        id=len(j['comments'])
        j['comments'].append({"id":id,"uname":uname,"content":content,"time":curtime})
        j_=json.dumps(j)

        with open(fname,'w',encoding='utf-8') as f:
            f.write(j_)

        session['comment_lim']=str(limit-1) # 扣一次发评论机会
        session.permanent=True

        return redirect('/ui/thread/{}'.format(target))

    else:
        return render_template('error.html',error_msg="token 有误！确保你的饼干正确配置")
    
def req_parse(req):
    if req.method=='GET':
        data=req.args
    if req.method=='POST':
        data=req.form.to_dict()
    return data