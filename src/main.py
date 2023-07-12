#Head
from flask import Flask, redirect, render_template, request, session
from flaskwebgui import FlaskUI,close_application
import time
import ctypes

#models
from models import *
from Setup import Settings

#Flask
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'ReleaseVer060'

#Release_Ver_0.6.0_Dev 2023-05-12-1

#database
import data as db
from data import userInfo,matter,type,setup

#settings
sets = Settings()

#config
headers = ["Id", "day", "start_time", "finish_time", "event", "level", "acc"]
headers1 = ["Id", "type", "level", "acc"]
headers_f = ["Id","friends"]
global choose,events,type_list,edit_msg,edit_judge_msg,login_error,page
choose = 0
edit_judge_msg = 0
edit_msg = None
page = 'login'
login_error = "已打开"
keep_login = sets.keep_login()
dev_mode = sets.dev_mode()


#app
@app.route('/')#根目录
def login():
    return render_template('login.html',
                           page = page,
                            **{'error':login_error},)


@app.route('/home')#主页
def home():
    global choose,events,edit_msg,edit_judge_msg
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if choose != 1:
        edit_judge_msg = 0
        events = db.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,).all()
        events = lamba(events,events,headers)
    return render_template('home.html',
                            day = day,
                            tables = events,
                            semd = "home",
                            **{'edit_msg':edit_msg},
                            **{'edit_judge_msg':edit_judge_msg}
                            )


@app.route('/home_check',methods=["POST"])#主页-分支-根据日期查找
def home_check():
    global choose,events,edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "搜索成功"
    datechoose = request.form.get("datechoose")
    if datechoose == '':
        choose = 0
    else:
        choose = 2
        events = db.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,)\
                .filter(matter.date== datechoose,matter.account == session.get('username'),).all()
        events = lamba(events,events,headers)
    return redirect('/home')


@app.route('/home-event-check',methods=["POST"])#主页-分支-删除
def home_event_check():
    global choose,events,edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "完成!"
    delid = request.form.get("finish")
    db.session.query(db.type).filter(type.id== delid).delete()
    db.session.commit()
    
    return redirect('/home')


@app.route('/search',methods=["POST"])#搜索
def home_search():
    global choose,events,type_list,edit_msg,edit_judge_msg
    redirect_1 = request.form.get("redirect")
    search = request.form.get("search")
    edit_judge_msg = 1
    edit_msg = "搜索完成"
    if redirect_1 == 'home':
        choose = 1
        events = cut_search(search,session.get('username'),headers)
        return redirect('/home')
    elif redirect_1 == 'share':
        choose = 1
        events = cut_search(search,session.get('username'),headers)
        return redirect('/share')
    elif redirect_1 == "types" :
        choose = 2
        type_list = cut_types(search,session.get('username'),headers)
        return redirect('/type')
    else:
        return redirect('/home')


@app.route('/add')#添加
def add():
    global edit_judge_msg,edit_msg
    place_time = time.strftime('%H:%m',time.localtime(time.time()))
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render_template('add.html',
                            time = place_time,
                            date = day,
                            **{'edit_msg':edit_msg},
                            **{'edit_judge_msg':edit_judge_msg})


@app.route('/add_test',methods=['POST'])#添加-分支-获取
def add_test():
    global edit_judge_msg,edit_msg
    edit_judge_msg = 1
    edit_msg = "添加成功"
    event = request.form.get("event")
    date = request.form.get("date")
    start_time = request.form.get("start_time")
    finish_time = request.form.get("finish_time")
    level = request.form.get("level")
    if len(date) == 0:
        date = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    Info = db.matter(date=date,start_time=start_time,finish_time=finish_time,matterInfo=event,level=level,comment='None',account=session.get('username'))
    db.session.add(Info)
    db.session.commit()
    return redirect('/add')


@app.route('/share')#分享
def share():
    global edit_judge_msg,edit_msg,events
    share_list = db.session.query(db.share.id,db.share.share_user,db.share.accept_user,db.share.matterID,db.share.matterInfo,)\
                .filter(db.share.accept_user == session.get('username'),).all()
    share_list = lamba(share_list,share_list,headers=["Id","share_user","accept_user","matterID","matterInfo"])
    if choose != 1:
        edit_judge_msg = 0
        events = db.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,)\
                .filter(matter.account == session.get('username')).all()
        events = lamba(events,events,headers)
    return render_template('share.html',
                            events = events,
                            shares = share_list,
                            semd = "share",
                            **{'edit_msg':edit_msg},
                            **{'edit_judge_msg':edit_judge_msg}
                            )


@app.route("/share_share",methods=["POST"])#分享-分享
def share_check():
    global edit_judge_msg,edit_msg
    edit_judge_msg = 1
    edit_msg = "已发送,等待对方接受"
    input_acc = request.form.get("share_user")
    share_ids = request.form.getlist("select")
    for share_id in share_ids:
        share_id,*share_ids = share_ids
        share_names = db.session.query(matter.matterInfo).filter(matter.id == share_id).one()
        for share_name in share_names:
            share_name,*share_names = share_names
            Info = db.share(share_user = session.get('username'),accept_user = input_acc,matterID = share_id,matterInfo = share_name)
            db.session.add(Info)
            db.session.commit()
            
    return redirect('/share')
    

@app.route('/share_acc&ref',methods=['POST'])#分享-接受&删除
def share_accref():
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    msg = request.form.get("state")
    id = request.form.get("id")
    share_id = request.form.get("share_id")
    if msg == "acc":
        share_list = db.session.query(matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level)\
                    .filter(matter.id == id).one()
        day,start_time,finish_time,event,level = share_list
        Info = db.matter(date=day,start_time=start_time,finish_time=finish_time,event=event,level=level,account=session.get('username'))
        db.session.add(Info)
        db.session.query(db.share).filter(db.share.id == share_id).delete()
        edit_msg = "已接受"
    elif msg == "ref":
        edit_msg = "已拒绝"
        db.session.query(db.share).filter(id == share_id).delete()
    db.session.commit()
    return redirect('/share')


@app.route('/type')#类别
def type_web():
    global type_list,edit_msg,edit_judge_msg
    if choose != 2:
        edit_judge_msg = 0
        type_list = db.session.query(type.id,type.type,type.level,type.account,).filter(matter.account == session.get('username')).all()
        type_list = list(map(lambda e: dict(zip(headers1, e)), type_list))
    return render_template('type.html',
                            tables = type_list,
                            semd = "types",
                            **{'edit_msg':edit_msg},
                            **{'edit_judge_msg':edit_judge_msg})


@app.route('/type_add',methods=["POST"])#类别-添加
def type_add():
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "添加成功"
    type_input = request.form.get("type")
    level_input = request.form.get("level")
    Info = type(type= type_input,level= level_input,account = session.get('username'))
    db.session.add(Info)
    db.session.commit()
    
    return redirect("/type")


@app.route('/type_del',methods=["POST"])#类别-删除
def type_del():
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "删除成功"
    id = request.form.get("id")
    db.session.query(db.type).filter(type.id == id).delete()
    db.session.commit()
    
    return redirect("/type")


@app.route('/edit')#编辑
def edit():           
    global edit_msg,edit_judge_msg
    id = db.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,)\
        .filter(matter.account == session.get('username')).all()
    id = list(map(lambda e: dict(zip(headers, e)), id))
    place_time = time.strftime('%H:%m',time.localtime(time.time()))
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    return render_template('edit.html',
                            tables = id,
                            day = day,
                            time = place_time,
                            **{'edit_msg':edit_msg},
                            **{'edit_judge_msg':edit_judge_msg})


@app.route('/edit-del&edi',methods=["POST"])#编辑-分支-删除&编辑
def edit_del():           
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    sel_type = request.form.get("type")
    sel_id = request.form.get("id")
    if sel_id == "MAX":
        edit_msg = "到底啦!"
        return redirect('/edit')
    sel_da = request.form.get("day")
    sel_st = request.form.get("start_time")
    sel_ft = request.form.get("finish_time")
    sel_na = request.form.get("event")
    sel_le = request.form.get("level")
    sel_list = db.session.query(matter.id,matter.date,matter.start_time,matter.finish_time,matter.matterInfo,matter.level,)\
            .filter(matter.id == sel_id).all()
    sel_all,*sel_list = sel_list
    sel_id,get_da,get_st,get_ft,get_na,get_le = sel_all
    if len(sel_da) == 0:
        up_da = get_da
    else:
        up_da = sel_da
    if len(sel_st) == 0:
        up_st = get_st
    else:
        up_st = sel_st
    if len(sel_ft) == 0:
        up_ft = get_ft
    else:
        up_ft = sel_ft
    if len(sel_na) == 0:
        up_na = get_na
    else:
        up_na = sel_na
    if len(sel_le) == 0:
        up_le = get_le
    else:
        up_le = sel_le
    sel_id = str(sel_id)
    if sel_type == "update":
        db.session.query(db.matter).filter(matter.account == session.get('username'),matter.id == sel_id).update({
                                                db.matter.matterInfo:up_na,
                                                db.matter.date:up_da,
                                                db.matter.start_time:up_st,
                                                db.matter.finish_time:up_ft,
                                                db.matter.matterInfo:up_na,
                                                db.matter.level:up_le,
                                                })
        db.session.commit()
        
        edit_judge_msg = "编辑成功"         
    elif sel_type == "del":
        db.session.query(db.matter).filter(matter.id == sel_id).delete()
        db.session.commit()
        
        edit_judge_msg = "删除成功"      
    return redirect('/edit')


@app.route('/friends')#好友页
def friends():
    friends = db.session.query(userInfo.account).filter(userInfo.account == session.get('username')).all()
    #friends = db.get_list("select * from `friends` where friends-o =",session.get('username'))#prdc mode
    friends = lamba(friends,friends,headers_f)
    return render_template("friends.html",
                           friends = friends
                           )


@app.route('/settings')#设置
def settings():
    o_keep_login = sets.rd("config","Keep_Login")
    o_keep_login = sets.rd("config","Keep_Login")
    o_Dev_Mode = sets.rd("config","Dev_Mode")
    o_Lac_Host = sets.rd("Settings","host")
    o_Lac_Port = sets.rd("Settings","port")
    return render_template('settings.html',
                           KpLi_c = o_keep_login,
                           Dev_c = o_Dev_Mode,
                           Host = o_Lac_Host,
                           Port = o_Lac_Port)


@app.route('/settings_update',methods=["POST"])#更新设置
def update_settings():
    set_data = request.form.get("DataBase_Mode")
    set_KpLi = request.form.get("Keep_Login")
    set_Mode = request.form.get("Dev_Mode")
    set_LaHs = request.form.get("Launch_Host")
    set_LaPt = request.form.get("Launch_Port")
    sets.cfg_in("config","Data_Mode",set_data)
    sets.cfg_in("config","Keep_Login",set_KpLi)
    sets.cfg_in("config","Dev_Mode",set_Mode)
    sets.cfg_in("Settings","host",set_LaHs)
    sets.cfg_in("Settings","port",set_LaPt)
    return redirect('/settings')


@app.route('/personal',methods=['POST','GET'])#个人页
def me():
    global edit_msg,edit_judge_msg,page,login_error
    edit_judge_msg = 1
    if request.method == 'POST':
        account = request.form.get("up_txt")
        mail = request.form.get("email")
        password = request.form.get("set_password")
        check_password = request.form.get("check_password")
        if account and password and check_password:
            if password == check_password:
                if len(mail) == 0:
                    mail = "None"
                db.session.query(db.userInfo).filter(userInfo.id == session.get('uid')).update({
                db.userInfo.account:account,
                db.userInfo.password:password,})
                db.session.commit()
                
                login_error = '修改成功'
                session.clear()
                page = "login"
                return redirect('/')
            else:
                edit_msg = '两次密码不一致'
                page = "edit"
        elif account: 
            db.session.query(db.userInfo).filter(userInfo.id == session.get('uid')).update({
                db.userInfo.account:account,})
            db.session.commit()
            
            login_error = '修改成功'
            session.clear()
            page = "login"
            return redirect('/')
        else:
            page = "edit"
            edit_msg = '未填写信息'
    elif request.method == 'GET':
        pass
    print(page)
    return render_template('personal.html',
                            username = session.get('username'),
                            uid = session.get('uid'),
                            page = page,
                            )


@app.route('/login',methods=['POST'])#登录
def login_check():
    global login_error,choose,page
    account = request.form.get("logid")
    password = request.form.get("password")
    acc_result = db.session.query(userInfo.account).filter(userInfo.account == account).first()
    pwd_result = db.session.query(userInfo.password).filter(userInfo.account == account,userInfo.password == password).first()
    if account and password:
        if acc_result:
            if pwd_result:
                session['username']=account
                session['password']=password
                uid =db.session.query(userInfo.id).filter(userInfo.account==account,userInfo.password==password).first()
                uid = uid[0]
                session['uid']= uid
                if keep_login == 'True':
                    session.permanent=True
                login_error = "已登录"
                choose = 0
                return redirect('/home')
            else:
                page = 'login'
                login_error = "密码错误"
                return redirect('/')
        else:
            page = 'login'
            login_error = "未知用户名"
            return redirect('/')
    else:
        page = 'login'
        login_error = "请写入信息"
        return redirect('/')


@app.route('/logout',methods=['POST'])#登出
def logout():
    global login_error
    session.clear()
    login_error = '登出成功'
    close_application()
    


@app.route('/register',methods=['POST'])#注册
def register():
    global login_error,page
    account = request.form.get("reg_txt")
    mail = request.form.get("email")
    password = request.form.get("set_password")
    check_password = request.form.get("check_password")
    if account and password and mail:
        if password == check_password:
            info = db.userInfo(
                            account=account,
                            password=password,
                            mail=mail,)
            db.session.add(info)
            db.session.commit()
            
            login_error = '注册成功'
            page = 'login'
        else:
            login_error = '两次密码不一'
    else:
        page = "register"
        login_error = '完整填写信息'
    return redirect('/')


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404


@app.before_request
def before_login():
    if 'username' in session:
        if request.path == '/':
            return redirect('/home')
        else:
            pass
    else:
        if request.path != '/' and request.path != '/login' and request.path != '/register' and request.endpoint not in ('static'):
            return redirect('/')
        pass


if __name__ == '__main__':
    setup()
    if dev_mode == "True":
    #WEB MODE
        app.run(debug=True,port=sets.rd("Settings","port"),host=sets.rd("Settings","host"))
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=sets.rd("Settings","port"),width=1000,height=800).run()