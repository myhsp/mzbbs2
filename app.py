from flask import Flask, render_template, request
from flask_mail import Mail,Message
from flask.json import jsonify
from threading import Thread
import hashlib,binascii
import sqlite3 as sql
from os import urandom as randbytes

from account.account_module import acc_bp
from blog.blog_module import blog_bp
from admin.admin_module import admin_bp
from lite_captcha.lite_captcha import lc_bp
from ui.ui import ui
from search.search_module import s_bp
from hitokoto.hito import hito_bp
from blog.massive_blog import upload_bp
from chat import oauth, chat_main

from mail import send_email
from werkzeug.utils import redirect

from datetime import timedelta

app=Flask(__name__)
mail=Mail(app)

app.register_blueprint(acc_bp,url_prefix='/account')
app.register_blueprint(blog_bp,url_prefix='/blog')
app.register_blueprint(admin_bp,url_prefix='/admin')
app.register_blueprint(lc_bp,url_prefix='/captcha')
app.register_blueprint(ui,url_prefix='/ui')
app.register_blueprint(s_bp,url_prefix='/search')
app.register_blueprint(hito_bp,url_prefix='/hitokoto')
app.register_blueprint(upload_bp,url_prefix='/upload')

app.register_blueprint(chat_main.chat, url_prefix = '/chat')
app.register_blueprint(oauth.oauth, url_prefix = '/oauth')


class conf:
    JSON_AS_ASCII=False
    SECRET_KEY=b'\xbf~\x94@\xcf6,7\xb1\xb4\x15^\x94\x90*b' # 神必代码
    PERMANENT_SESSION_LIFETIME=timedelta(weeks=24)

    UPLOAD_FOLDER='./upload'
    ALLOWED_EXTENSIONS=set(['.txt'])
    MAX_CONTENT_LENGTH=1024*1024

    MAIL_SERVER='smtp.office365.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='creeperblin@outlook.com',
    MAIL_PASSWORD='cp:U6JdRQ3yL8Pe'
app.config.from_object(conf)


@app.route('/auth/mail_verify',methods=['POST'])
def send_mail():
    '''
    首先 lite captcha 人机验证
    再发这个邮箱验证
    '''
    try:
        data=request.form.to_dict()

        user_mail=data['user_mail']

        key=data['key']
        random=data['random']
        ans=data['ans']
    except:
        return jsonify(errcode=120,msg='argument missing')

    pwd=ans+random
    key_user=hashlib.sha256(pwd.encode()).hexdigest()

    if key != key_user:
        return jsonify({
            'errcode':200,
            'msg':'error'
        })
    else:
        token=hashlib.md5(randbytes(16)).hexdigest()
        verify_code=hashlib.md5(randbytes(16)).hexdigest()

        send_email(app,mail,'verify_code','creeperblin@outlook.com',user_mail,verify_code,verify_code)

        mdb=sql.connect('./databases/mail_verify.db')
        mdb.row_factory=sql.Row
        mdb.execute('INSERT INTO records (token,verify) VALUES (?,?)',
        [token,verify_code])
        mdb.commit()
        mdb.close()
        return jsonify({
            'token':token,
            'errcode':0,
            'msg':''
        })

@app.route('/databases/',methods=['GET','POST'])
@app.route('/databases/<any>',methods=['GET','POST']) # 阻止强行访问数据库
def protection(any=''):
    return ('You have no accessibility to this folder. Please contact admin for further information.')

@app.route('/')
def auto_route():
    return redirect('/ui/forum')

@app.errorhandler(404)
def page404_handler(error):
    return render_template('404.html',error_msg=error),404

@app.errorhandler(500)
def page500_handler(error):
    errstring='''
    按理说这个界面是不会出现的，但是它确实出现了
    说明我们的代码有问题，不过也要想想你是不是
    进行了一些刁钻操作。'''
    return render_template('error.html',error_msg=errstring),500