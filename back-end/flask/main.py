from flask import Flask,render_template,request,session,redirect
from debug import debug
from os import urandom
from uuid import uuid4
from datetime import datetime
from random import choice

from db import getStudentData

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)

def checkLogin() :
    """
    確認登入狀態
    預防非用戶登入，確認是否為用戶
    """
    try:
        session["account"]
        session["password"]

        # todo 用判斷判定是否為用戶

    except:
        # 非用戶
        return False
    pass

def generate_random_string(length=6):
    key = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"    
    random_string = ''.join(choice(key) for _ in range(length))
    return random_string


# 路由 Router
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign")
def sign():
    return render_template("sign.html")

@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/lastStep")
def lastStep():
    return render_template("lastStep.html")

@app.route("/consent")
def consent():
    student_id = request.args.get("studentID","")
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("consent.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

@app.route("/maintenance")
def maintenance():
    student_id = request.args.get("studentID")
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("maintenance.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

@app.route("/admin")
def admin():
    return render_template("admin/admin.html")


# api
@app.route("/login",methods=["POST"])
def login():
    # 讀取資料
    account = request.form.get("account")
    password = request.form.get("password")

    # todo 
    # get isAccount 
    # if YES:
        # 存入session
        # 跳轉網頁
    # if NO:
        # 上一頁 ==

    # 存入session
    session["account"] = account
    session["password"] = password

    # todo del 
    debug.panel(title="/login",account=account,password = password)

    return redirect("/sign")

@app.route("/signUp",methods=["POST"])
def signUp():
    # userID
    uuid = [uuid4()]
    # 時間戳
    timestamp = [datetime.timestamp(datetime.now())] 
    # 姓名 email school 科系 社團 password tel id birth 聯絡人 聯絡人關西 聯絡人電話  size 飲食習慣  特殊疾病  團報優惠碼
    data_values = request.form.getlist('data[]')
    male = request.form.getlist('data[male]')
    food = request.form.getlist('data[food]')
    isLive = request.form.getlist('data[live]')
    coupon = [generate_random_string()]
    # debug.blue(data_values)
    for d in data_values:
        debug.yellow(d)
        
    debug.yellow(str(male))
    debug.yellow(str(food))

    #  todo     
    # 要船上去的資料
    result = uuid + data_values[0:7] + male + data_values[7:13] + food + isLive + coupon + timestamp
    
    return redirect("/lastStep")

@app.route("/sendSign",methods=["POST"])
def sendSign():
    try:
        # 获取POST请求的原始数据
        data = request.data.decode('utf-8')
        print('Received data:', data)

        # 在这里处理接收到的文本数据，可以根据需要进行其他操作

        return redirect('/edit')

    except Exception as e:
        print('Error:', str(e))
        return 'Error occurred'

# admin
@app.route("/admin/login")
def adminLogin():
    return


if __name__ == "__main__":
    app.run(debug=True)