import sqlite3 as sql
from flask import Blueprint, render_template, request, session
import base64,uuid

upload_bp=Blueprint('upload',__name__)

@upload_bp.route('/text',methods=['POST'])
def upload_massive_text():
    _token=session.get('token')
    _limit=session.get('massive_blog_lim')
    if _token==None or _limit==None:
        return render_template('error.html',error_msg="你的token没有正确配置或未签到")
    token=_token
    limit=int(_limit)

    if limit<=0:
        return render_template('error.html',error_msg="今天使用该功能次数用完了")

    tdb=sql.connect('./databases/user_token.db')
    tdb.row_factory=sql.Row
    t_info=tdb.execute('select uid from token where token=? limit 1',[token]).fetchall()
    tdb.close()

    if len(t_info)!=0:
        uid=t_info[0][0]
        uid_b64=base64.b64encode(uid.encode()).decode()
        fname=''.join(str(uuid.uuid4()).split('-'))

        file=request.files['file']
        file.save('./upload/text/'+fname+'.txt')
        with open('./upload/text/'+fname+'.txt','a',encoding='utf-8') as f:
            f.write('\nAuthor: '+uid_b64)
            f.close()
        session['massive_blog_lim']=limit-1
        session.permanent=True
        return "请把这串字符粘贴到“发帖”中有关区域。<br>"+fname
    else:
        return render_template('error.html',error_msg="token有误")

        

