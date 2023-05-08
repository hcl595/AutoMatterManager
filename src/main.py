#Head
from flask import Flask, redirect, render_template, request
from flaskwebgui import FlaskUI
import time
import ctypes

#models
from models import *
from Setup import Settings

#Flask
app = Flask(__name__)
app.config.from_object(__name__)

#Release_Ver_0.5.4_Dev 2023-05-07-1

#database
import data as db
from data import userInfo,matter,type,share,setup

#settings
sets = Settings()

#config
headers = ["Id", "day", "start_time", "finish_time", "event", "level", "acc"]
headers1 = ["Id", "type", "level", "acc"]
headers_f = ["Id","friends"]
global choose,events,type_list,edit_msg,edit_judge_msg,login_error
choose = 0
login_sc = 0
show_share = 0
edit_judge_msg = 0
edit_msg = None
login_error = "已打开"
event2 = []
acc = sets.keep_login()
dev_mode = sets.dev_mode()
port = sets.rd("Settings","port")

#app
@app.route('/')#根目录
def login():
    result = db.session.query(userInfo.id,userInfo.name,userInfo.key,).all()
    print(result)
    return render_template('login.html',
                            **{'error':login_error})


@app.route('/home')#主页
def home():
    global choose,events,edit_msg,edit_judge_msg
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if choose != 1:
        edit_judge_msg = 0
        events = db.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,).all()
        print(events)
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
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    datechoose = request.form.get("datechoose")
    if datechoose == '':
        choose = 0
    else:
        choose = 2
        events = db.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,)\
                .filter(matter.day== datechoose,matter.acc== acc,).all()
        events = lamba(events,events,headers)
    return redirect('/home')


@app.route('/home-event-check',methods=["POST"])#主页-分支-删除
def home_event_check():
    global choose,events,edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "完成!"
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    delid = request.form.get("finish")
    db.session.query(db.type).filter(type.id== delid).delete()
    db.session.commit()
    db.session.remove()
    return redirect('/home')


@app.route('/search',methods=["POST"])#搜索
def home_search():
    global choose,events,type_list,edit_msg,edit_judge_msg
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    redirect_1 = request.form.get("redirect")
    search = request.form.get("search")
    edit_judge_msg = 1
    edit_msg = "搜索完成"
    if redirect_1 == 'home':
        choose = 1
        events = cut_search(search,acc,headers)
        return redirect('/home')
    elif redirect_1 == 'share':
        choose = 1
        events = cut_search(search,acc,headers)
        return redirect('/share')
    elif redirect_1 == "types" :
        choose = 2
        type_list = cut_types(search,acc,headers)
        return redirect('/type')
    else:
        return redirect('/home')


@app.route('/add')#添加
def add():
    global edit_judge_msg,edit_msg
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
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
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    event = request.form.get("event")
    day = request.form.get("date")
    start_time = request.form.get("start_time")
    finish_time = request.form.get("finish_time")
    level = request.form.get("level")
    if len(day) == 0:
        day = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    Info = db.matter(day=day,start_time=start_time,finish_time=finish_time,event=event,level=level,acc=acc)
    db.session.add(Info)
    db.session.commit()
    db.session.remove()
    return redirect('/add')


@app.route('/share')#分享
def share():
    global edit_judge_msg,edit_msg,events
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    share_list = db.session.query(db.share.id,db.share.share_user,db.share.acc_user,db.share.eventID,db.share.eventInfo,)\
                .filter(db.share.acc_user == acc,).all()
    share_list = lamba(share_list,share_list,headers=["Id","share_user","acc_user","event","event_name"])
    if choose != 1:
        edit_judge_msg = 0
        events = db.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,)\
                .filter(matter.acc == acc).all()
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
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    input_acc = request.form.get("share_user")
    share_ids = request.form.getlist("select")
    for share_id in share_ids:
        share_id,*share_ids = share_ids
        share_names = db.session.query(matter.event).filter(matter.id == share_id).one()
        for share_name in share_names:
            share_name,*share_names = share_names
            Info = db.share(share_user = acc,acc_user = input_acc,eventID = share_id,eventInfo = share_name)
            db.session.add(Info)
            db.session.commit()
            db.session.remove()
    return redirect('/share')
    

@app.route('/share_acc&ref',methods=['POST'])#分享-接受&删除
def share_accref():
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    msg = request.form.get("state")
    id = request.form.get("id")
    share_id = request.form.get("share_id")
    if msg == "acc":
        share_list = db.session.query(matter.day,matter.start_time,matter.finish_time,matter.event,matter.level)\
                    .filter(matter.id == id).one()
        day,start_time,finish_time,event,level = share_list
        Info = db.matter(day=day,start_time=start_time,finish_time=finish_time,event=event,level=level,acc=acc)
        db.session.add(Info)
        db.session.query(db.share).filter(db.share.id == share_id).delete()
        edit_msg = "已接受"
    elif msg == "ref":
        edit_msg = "已拒绝"
        db.session.query(db.share).filter(id == share_id).delete()
    db.session.commit()
    db.session.remove()
    return redirect('/share')


@app.route('/type')#类别
def type_web():
    global type_list,edit_msg,edit_judge_msg
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    if choose != 2:
        edit_judge_msg = 0
        type_list = db.session.query(type.id,type.type,type.level,type.acc,).filter(acc == acc).all()
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
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    type_input = request.form.get("type")
    level_input = request.form.get("level")
    Info = type(type= type_input,level= level_input,acc= acc)
    db.session.add(Info)
    db.session.commit()
    db.session.remove()
    return redirect("/type")


@app.route('/type_del',methods=["POST"])#类别-删除
def type_del():
    global edit_msg,edit_judge_msg
    edit_judge_msg = 1
    edit_msg = "删除成功"
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    id = request.form.get("id")
    db.session.query(db.type).filter(type.id == id).delete()
    db.session.commit()
    db.session.remove()
    return redirect("/type")


@app.route('/edit')#编辑
def edit():           
    global edit_msg,edit_judge_msg
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    id = db.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,)\
        .filter(acc == acc).all()
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
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
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
    sel_list = db.session.query(matter.id,matter.day,matter.start_time,matter.finish_time,matter.event,matter.level,)\
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
        db.session.query(db.matter).filter(matter.acc == acc,matter.id == sel_id).update({
                                                db.matter.event:up_na,
                                                db.matter.day:up_da,
                                                db.matter.start_time:up_st,
                                                db.matter.finish_time:up_ft,
                                                db.matter.event:up_na,
                                                db.matter.level:up_le,
                                                })
        db.session.commit()
        db.session.remove()
        edit_judge_msg = "编辑成功"         
    elif sel_type == "del":
        db.session.query(db.matter).filter(matter.id == sel_id).delete()
        db.session.commit()
        db.session.remove()
        edit_judge_msg = "删除成功"      
    return redirect('/edit')


@app.route('/friends')#好友页
def friends():
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    friends = db.session.query(userInfo.name).filter(userInfo.name == acc).all()
    #friends = db.get_list("select * from `friends` where friends-o =",acc)#prdc mode
    friends = lamba(friends,friends,headers_f)
    return render_template("friends.html",
                           friends = friends
                           )


@app.route('/settings')#设置
def settings():
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    o_data_mode = sets.rd("config","Data_Mode")
    o_keep_login = sets.rd("config","Keep_Login")
    o_Dev_Mode = sets.rd("config","Dev_Mode")
    return render_template('settings.html',
                           Data_c = o_data_mode,
                           KpLi_c = o_keep_login,
                           Dev_c = o_Dev_Mode)


@app.route('/settings_update',methods=["POST"])#更新设置
def update_settings():
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    set_data = request.form.get("DataBase_Mode")
    set_KpLi = request.form.get("Keep_Login")
    set_Mode = request.form.get("Dev_Mode")
    sets.cfg_in("config","Data_Mode",set_data)
    sets.cfg_in("config","Keep_Login",set_KpLi)
    sets.cfg_in("config","Dev_Mode",set_Mode)
    sets.cfg_in("Settings","acc",acc)
    db.reconn()
    return redirect('/settings')


@app.route('/personal')#个人页
def me():
    login_error = check_login(acc)
    if login_error != 1:
        return redirect("/")
    uid = db.session.query(userInfo.id).filter(userInfo.name == acc,).first()
    uid = cal_add(*uid)
    return render_template('personal.html',
                            user = acc,
                            uid = uid
                            )


@app.route('/login',methods=['POST'])#登录
def login_check():
    global login_error,choose
    account = request.form.get("logid")
    password = request.form.get("password")
    get_acc = db.session.query(userInfo.name).filter(userInfo.name == account).all()
    acc_result = len(get_acc)
    get_pwd = db.session.query(userInfo.key).filter(userInfo.key == password).all()
    print(get_pwd)
    pwd_result = len(get_pwd)
    if account and password:
        if acc_result >= 1:
            if pwd_result >= 1:
                global acc
                acc = request.form.get("logid")
                login_error = "已登录"
                choose = 0
                return redirect('/home')
            else:
                login_error = "密码错误"
                return redirect('/')
        else:
            login_error = "未知用户名"
            return redirect('/')
    else:
        login_error = "请写入信息"
        return redirect('/')


@app.route('/logout',methods=['POST'])#登出
def logout():
    global login_error,acc
    acc = None
    login_error = '登出成功'
    return redirect('/')


@app.route('/register_test',methods=['POST'])#注册
def register_test():
    global login_error
    account = request.form.get("reg_txt")
    mail = request.form.get("email")
    password = request.form.get("set_password")
    check_password = request.form.get("check_password")
    if password == check_password:
        print(account,password)
        info = db.userInfo(
                        name=account,
                        key= password,
                        mail=mail,)
        db.session.add(info)
        db.session.commit()
        db.session.remove()
        login_error = '注册成功'
    else:
        login_error = '密码不一'
    return redirect('/')


@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    setup()
    if dev_mode == "True":
    #WEB MODE
        app.run(debug=True,port=port)
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=port,width=1000,height=800).run()