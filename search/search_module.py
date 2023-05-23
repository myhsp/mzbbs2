from flask import Blueprint,request,render_template,jsonify
import sqlite3 as sql
from typing import NamedTuple

s_bp=Blueprint('search',__name__)

def req_parse(req):
    if req.method=='GET':
        data=req.args
    if req.method=='POST':
        data=req.form.to_dict()
    return data

@s_bp.route('/search_service',methods=['GET'])
def search():
    data=req_parse(request)
    try:
        search_type=data.get('type')
        search_query='%'+data.get('query').replace(' ','%')+'%'
        _page=data.get('page') if 'page' in data else 1
        page=int(_page)
    except:
        return render_template('error.html',error_msg="请求参数有误！")

    if search_type=='user':
        htm='search_user.html'
        db=sql.connect('./databases/user_info.db')
        r=db.execute('select username,nickname,email,slogan,avatar from users where username like ? or nickname like ?',[search_query,search_query]
        ).fetchall()
    elif search_type=='tag':
        htm='search_article.html'
        db=sql.connect('./databases/articles.db')
        r=db.execute('select num,title,username,date from articles where tags like ? order by date desc',[search_query]
        ).fetchall()
    elif search_type=='section':
        htm='search_article.html'
        db=sql.connect('./databases/articles.db')
        r=db.execute('select num,title,username,date from articles where section=? order by date desc',[int(data.get('query').replace('%',''))]
        ).fetchall()
    else:
        htm='search_article.html'
        db=sql.connect('./databases/articles.db')
        r=db.execute('select num,title,username,date from articles where title like ? or description like ? order by date desc',[search_query,search_query]
        ).fetchall()
    db.close()

    length=len(r)
    if length % 10 !=0:
        pages=length//10+1 #总共的页数
    else:
        pages=length//10
    use_nextpage=True # 是否显示“下一页”按钮
    use_previous=True # 是否显示“上一页”按钮

    if page>=pages:
        page=pages
        use_nextpage=0

    if page<=1:
        page=1
        use_previous=0


    ret=r[(page-1)*10:page*10]
    return render_template(htm,count=str(length),
    records=ret,
    search_type=search_type,
    search_query=search_query,
    cur_page=page,total_page=pages,
    use_next=use_nextpage,use_previous=use_previous)