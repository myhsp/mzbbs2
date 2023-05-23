from flask import Blueprint,jsonify,request
import os,datetime,time
import sqlite3 as sql

hito_bp=Blueprint('hito',__name__)
db=sql.connect('./databases/hito.db')

@hito_bp.route('/')
def hito():
  all=get_count()
  if all==0:
    return 'WDNMD'
  hit=db.execute('select content,author from hito order by random() limit 1').fetchall()[0]
  content=hit[0]
  author=hit[1]
  raw='''<!--    Made with 💖 by Deu5ExMach1na
/////////////////////////////////////////////
//                                         //
//                                         //
//    +   +                                //
//   +++ +++                               //
//  +++++++++                              //
//    +++++            /\                 ///
//     +++            /  \               / //
//      +            /    \             /  //
//                  /      \           /   //
//                 /        \_________/    //
//                /                        //
//               /       \         /       //
//              /       __\       /__      //
//             /                           //
//            /             ____           //
//           /              \  /           //
//          /     _~_        \/    _~_     //
//         /     /  /             |   |    //
//        /     /  /              |   |    //
//       /     /  /               |   |    //
/////////////////////////////////////////////
-->
<html><head><meta charset="utf-8"><title>Hitokoto</title><style id="initial-style">:root{--error-color:rgb(0, 0, 0, 0.5);--error-title-color:rgba(0, 0, 0, 0.87);--error-footer-color:rgba(0, 0, 0, 0.4);--error-background-color:#f3f3f3}#error{position:fixed;top:0;left:0;z-index:999999999;width:calc(100vw - 28px);margin:0 14px 0 14px;height:100vh;display:flex;flex-direction:column;align-items:center;color:var(--error-color);font-family:"Helvetica Neue",Helvetica,Roboto,Segoe,Tahoma,sans-serif;overflow:auto}#error::after,#error::before{content:"";flex-basis:90px;flex-shrink:999999999}#error ::selection{background-color:#cce2ff}#error-title{display:flex;align-items:center;color:var(--error-title-color);margin:32px 0 25px 0}#error-icon{width:50px;position:relative;height:50px;border-radius:50%;border:2px solid var(--error-color);margin-right:20px}#error-icon::after,#error-icon::before{position:absolute;content:"";width:5%;left:47.5%;top:15%;height:70%;background-color:var(--error-color);transform:rotate(-45deg)}#error-icon::before{transform:rotate(45deg)}#error h1{font-weight:400;font-size:28px;margin:0}#error p{margin:7px 0 7px 0;font-size:14px}#error pre{box-sizing:border-box;max-width:100%;overflow:auto;margin:25px 0 0 0;background:var(--error-background-color,#f3f3f3);padding:13px;font-size:13px;flex-shrink:1}#error-footer{font-size:13px;color:var(--error-footer-color);margin:25px 0 25px 0;text-align:center;line-height:1.4}#error a{color:#4183c4;text-decoration:none}#error a:hover{color:#1e70bf}#error code,#error pre{font-family:"Fira Code","Roboto Mono","DM Mono",Menlo,Consolas,"Ubuntu Mono"}body{background:var(--theme-background,#fff)!important}@media only screen and (prefers-color-scheme:dark){body{background:var(--theme-background,#222)!important}:root{--error-color:rgb(255, 255, 255, 0.5);--error-title-color:rgba(255, 255, 255, 0.87);--error-footer-color:rgba(255, 255, 255, 0.4);--error-background-color:#0c0c0c}}</style><script type="text/javascript" async="" src="https://www.gstatic.cn/recaptcha/releases/TDBxTlSsKAUm3tSIa0fwIqNu/recaptcha__zh_cn.js" crossorigin="anonymous" integrity="sha384-+1xTZD1vXy4iYpvAgshm/J25tGGIOEBGzwJvtWiX6bJvTIuQBQI0VJIeRASsTPiz"></script><script>function fatalError(e,n){var t=document.getElementById("error");if(""!==t.style.display){var r=document.getElementById("root");r&&document.body.removeChild(r);for(var o=document.getElementsByTagName("style"),a=o.length-1;a>=0;a--)"initial-style"!==o[a].id&&o[a].parentNode.removeChild(o[a]);var i=document.getElementById("error-footer");for(var a in e){var l=document.createElement("p");l.innerText=e[a],t.insertBefore(l,i)}if(n){var d=document.createElement("pre");d.innerText=n,t.insertBefore(d,i)}t.style.display=""}}function handleLoadingError(){fatalError(["There's an error loading the application. Please check your network connection.","加载应用程序时出现错误，请检查您的网络连接。"])}function refreshSession(e){e||(e=function(){try{var e=JSON.parse(localStorage.appState);if(!e.logout)return e.token;e.logout=!1,localStorage.appState=JSON.stringify(e)}catch(e){return null}}()||"");var n=document.createElement("script");n.async=!0,n.onerror=handleLoadingError,n.src=window.apiEndpoint+"api/auth/getSessionInfo?jsonp=1&token="+encodeURIComponent(e),document.head.appendChild(n)}refreshSession(),function(){var e;e=window.publicPath+"static/css/styles~main.e6f86da8.chunk.css",addLinkTag("stylesheet",e,handleLoadingError)}();</script><script async="" src="undefinedapi/auth/getSessionInfo?jsonp=1&amp;token="></script><script async="" src="https://api.loj.ac.cn/api/auth/getSessionInfo?jsonp=1&amp;token="></script><link rel="stylesheet" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/styles~main.e6f86da8.chunk.css"><script async="" src="https://api.loj.ac.cn/api/auth/getSessionInfo?jsonp=1&amp;token="></script><link rel="stylesheet" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/styles~main.e6f86da8.chunk.css"><script async="" src="https://api.loj.ac.cn/api/auth/getSessionInfo?jsonp=1&amp;token="></script><link rel="stylesheet" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/styles~main.e6f86da8.chunk.css"><link rel="stylesheet" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/3777e6553c3f7c82f9ab49216846716b.css"><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/73.5260a5e9.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/175.2737b942.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/176.77b12433.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/177.f35d370e.chunk.js"></script><script src="https://www.google-analytics.com/analytics.js" async=""></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/85.57ecdc8f.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/246.05129a17.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/101.1484c9a3.chunk.js"></script><meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" data-rh="true"><style id="font-preference-code">.monospace, code, pre {
  font-family: "Fira Code", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft Yahei", "WenQuanYi Micro Hei", "Droid Sans Fallback", monospace !important;
  font-size: 14px !important;
  line-height: 1.3 !important;
  font-variant-ligatures: normal !important;
}</style><style id="font-preference-content">.content-font {
  font-family: "Open Sans", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft Yahei", "WenQuanYi Micro Hei", "Droid Sans Fallback", sans-serif !important;
}</style><style id="font-ui">.ui-font, body, h1, h2, h3, h4, h5, .ui.button, .ui.text.container, .ui.header, .ui.input > input, .ui.list .list > .item .header, .ui.list > .item .header, .ui.steps .step .title, .ui.form input:not([type]), .ui.form input[type="date"], .ui.form input[type="datetime-local"], .ui.form input[type="email"], .ui.form input[type="number"], .ui.form input[type="password"], .ui.form input[type="search"], .ui.form input[type="tel"], .ui.form input[type="time"], .ui.form input[type="text"], .ui.form input[type="file"], .ui.form input[type="url"], .ui.input textarea, .ui.form textarea, .ui.menu, .ui.message .header, .ui.cards > .card > .content > .header, .ui.card > .content > .header, .ui.items > .item > .content > .header, .ui.statistics .statistic > .value, .ui.statistic > .value, .ui.statistics .statistic > .label, .ui.statistic > .label, .ui.accordion .title:not(.ui), .ui.modal > .header, .ui.popup > .header, .ui.search > .results .result .title, .ui.search > .results > .message .header, .ui.category.search > .results .category > .name {
  font-family: "Lato", "Noto Sans CJK SC", "Source Han Sans SC", "PingFang SC", "Hiragino Sans GB", "Microsoft Yahei", "WenQuanYi Micro Hei", "Droid Sans Fallback", sans-serif;
}</style><script id="google-recaptcha-v3" src="https://www.recaptcha.net/recaptcha/api.js?render=6Lcqn94ZAAAAABeUyevpLws6eRIQqWZQ3i_sMX6c&amp;hl=zh-CN"></script><link rel="stylesheet" type="text/css" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/33.fc72314d.chunk.css"><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/33.0e8d737a.chunk.js"></script><link rel="stylesheet" type="text/css" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/27.e1b65e37.chunk.css"><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/27.5ce4b22c.chunk.js"></script><link rel="stylesheet" type="text/css" href="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/css/131.a310d99f.chunk.css"><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/131.4572cb34.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/0.caeb875c.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/1.bd2585c5.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/2.1aea64d0.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/17.2b678627.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/38.2b81050f.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/32.325220ea.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/58.d0b97d06.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/129.0bc0577b.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/9.3a0d9e83.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/8.59bc6432.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/20.ad918d12.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/35.fbd238b2.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/29.880f74dd.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/50.8400fdbf.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/63.39b95bb7.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/99.6eff4d40.chunk.js"></script><script charset="utf-8" src="https://unpkg.zhimg.com/@lyrio/ui@0.2.8/build/static/js/150.ed77c875.chunk.js"></script></head><body data-theme="far"><div class="siteName--3HEzm" style="width:400;height:30">Hitokoto</div><div class="siteName--3HEzm" style="width:400;height:30"> </div><div class="five wide column" style="position:relative;left:5;width:400;height:101"><h4 class="ui block top attached header header--2-FS1 hitokoto--2x2Pr"><i aria-hidden="true" class="comment alternate icon"></i><div class="content">一言（ヒトコト）</div></h4><div class="ui bottom attached center aligned segment segment--2PECa"><div>wdnmd<div class="hitokotoFrom--2PmvT">xxx</div></div></div></div><a class=" " href="/hitokoto/get" style="position:absolute;left:10;top:220">/hitokoto/get</a>
<a class=" " href="/hitokoto/upload" style="position:absolute;left:10;top:240">/hitokoto/upload?author=..&amp;content=..&amp;uploader=..</a><div><div class="grecaptcha-badge" data-style="bottomright" style="width: 256px; height: 60px; display: block; transition: right 0.3s ease 0s; position: fixed; bottom: 14px; right: -186px; box-shadow: gray 0px 0px 5px; border-radius: 2px; overflow: hidden;"><div class="grecaptcha-logo"><iframe title="reCAPTCHA" src="https://www.recaptcha.net/recaptcha/api2/anchor?ar=1&amp;k=6Lcqn94ZAAAAABeUyevpLws6eRIQqWZQ3i_sMX6c&amp;co=aHR0cDovLzEyNy4wLjAuMTo1MDAw&amp;hl=zh-CN&amp;v=TDBxTlSsKAUm3tSIa0fwIqNu&amp;size=invisible&amp;cb=xwophxs50620" width="256" height="60" role="presentation" name="a-mo9znxmvzssr" frameborder="0" scrolling="no" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation"></iframe></div><div class="grecaptcha-error"></div><textarea id="g-recaptcha-response-100000" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea></div><iframe style="display: none;"></iframe></div><div><div class="grecaptcha-badge" data-style="none" style="width: 256px; height: 60px; position: fixed; visibility: hidden;"><div class="grecaptcha-logo"><iframe title="reCAPTCHA" src="https://www.recaptcha.net/recaptcha/api2/anchor?ar=1&amp;k=6Lcqn94ZAAAAABeUyevpLws6eRIQqWZQ3i_sMX6c&amp;co=aHR0cDovLzEyNy4wLjAuMTo1MDAw&amp;hl=zh-CN&amp;v=TDBxTlSsKAUm3tSIa0fwIqNu&amp;size=invisible&amp;cb=c750jw8glv62" width="256" height="60" role="presentation" name="a-y658uhaeoyg6" frameborder="0" scrolling="no" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation"></iframe></div><div class="grecaptcha-error"></div><textarea id="g-recaptcha-response-100000" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea></div><iframe style="display: none;"></iframe></div><div><div class="grecaptcha-badge" data-style="none" style="width: 256px; height: 60px; position: fixed; visibility: hidden;"><div class="grecaptcha-logo"><iframe title="reCAPTCHA" src="https://www.recaptcha.net/recaptcha/api2/anchor?ar=1&amp;k=6Lcqn94ZAAAAABeUyevpLws6eRIQqWZQ3i_sMX6c&amp;co=aHR0cDovLzEyNy4wLjAuMTo1MDAw&amp;hl=zh-CN&amp;v=TDBxTlSsKAUm3tSIa0fwIqNu&amp;size=invisible&amp;cb=wgv0kg5le239" width="256" height="60" role="presentation" name="a-umv56xflvbmr" frameborder="0" scrolling="no" sandbox="allow-forms allow-popups allow-same-origin allow-scripts allow-top-navigation allow-modals allow-popups-to-escape-sandbox allow-storage-access-by-user-activation"></iframe></div><div class="grecaptcha-error"></div><textarea id="g-recaptcha-response-100000" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid rgb(193, 193, 193); margin: 10px 25px; padding: 0px; resize: none; display: none;"></textarea></div><iframe style="display: none;"></iframe></div></body></html>
'''
  raw=raw.replace("wdnmd",content)
  raw=raw.replace("xxx",author)
  return raw

@hito_bp.route("/upload", methods=["GET"])
def upload():
  count=get_count()
  count+=1

  content=request.args.get("content")
  if(content==None):
    return {"res":"failed"} 
  time=datetime.datetime.now()
  author=request.args.get("author")
  uploader=request.args.get("uploader")
  db.execute('insert into hito (id,content,time,author,uploader) values (?,?,?,?,?)',[count,content,time,author,uploader])
  db.commit()
  update_count(count)
  return jsonify({"res":"success"})

@hito_bp.route("/get")
def get():
  all=get_count()
  if all==0:
    return 'WDNMD'
  hit=db.execute('select id,content,time,author,uploader from hito order by random() limit 1').fetchall()[0]
  ret={"id":hit[0],"content":hit[1],"time":hit[2],"author":hit[3],"uploader":hit[4]}
  return jsonify(ret)

@hito_bp.route("/reset",methods=["GET"])
def reset():
  db.execute('delete from hito')
  db.commit()
  update_count(0)
  return jsonify({"msg":"success"})

@hito_bp.route("/count",methods=["GET"])
def count():
  return jsonify({"msg":"success","count":get_count()})

def get_count():
  with open('hito.txt','r') as f:
    c=int(f.read())
    f.close()
    return c

def update_count(_num):
  num=str(_num)
  with open('hito.txt','w') as f:
    f.write(num)
    f.close()


