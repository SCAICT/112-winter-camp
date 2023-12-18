from flask import Flask,render_template,request,session,redirect
from debug import debug
from os import urandom
from uuid import uuid4
from datetime import datetime
from random import choice
from re import match

from db import *


app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)

def checkLogin() :
    """
    確認登入狀態
    預防非用戶登入，確認是否為用戶
    """
    if 'userID' in session:
        return True
    return False

def checkData():
    pass

def generate_random_string(length=6):
    key = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"    
    random_string = ''.join(choice(key) for _ in range(length))
    return random_string

def is_email(input_str):
    # 定義電子郵件地址的正規表達式
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return match(email_pattern, input_str) is not None

# 路由 Router
@app.route("/")
def home():
    if checkLogin():
        debug.bg_yellow(session["userID"])
        return redirect("/lastStep")

    return render_template("home.html")

# 登出
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# 創建資料
@app.route("/sign")
def sign():
    return render_template("sign.html")

# 編輯資料
@app.route("/edit")
def edit():
    return render_template("edit.html")

# 完成
@app.route("/success")
def success():
    return render_template("success.html")

# 最後一步
@app.route("/lastStep")
def lastStep():
    if not(checkLogin()):
        return redirect("/")
    # coupon,isPaid,consentID,maintenance
    result = getUserLastStep(UserID=session["userID"])[0]
    debug.yellow(str(result))
    return render_template("lastStep.html",coupon=result[0],isPaid=result[1],consent=result[2],maintenance=result[3],userID=session["userID"])

# 家長同意書
@app.route("/consent")
def consent():
    student_id = request.args.get("studentID","")
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("consent.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

# 場地切結書
@app.route("/maintenance")
def maintenance():
    student_id = request.args.get("studentID")
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("maintenance.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

# 管理者頁面
@app.route("/admin")
def admin():
    return render_template("admin/admin.html")


# api
@app.route("/login",methods=["POST"])
def login():
    # 讀取資料
    account = request.form.get("account")
    # todo 加密
    password = request.form.get("password")

    debug.panel("log",account=account,password=password)
    # 判斷為 email || 電話
    if is_email(account):
        # check[0] -> status , check[1] -> userID
        check = isUserMail(mail=account) 
        # is user
        if check[0]:
            # 回傳密碼正確與否
            if (isPasswordCorrect(userID=check[1],password=password)):
                pass
            # 密碼錯誤
            else:
                session.clear()
                return '<script>alert("密碼錯誤");window.location.href = "/";</script>'
        # not user
        else:
            return '<script>alert("查無此人");window.location.href = "/";</script>'
    else:
        # 數字防呆
        try:
            int(account)    
        except:
            session.clear()
            # 不為email和phone
            return '<script>alert("輸入錯誤");window.location.href = "/";</script>'
        
        check = isUserPhone(phone=account) 
        # is user
        if check[0]:
            # 回傳密碼正確與否
            if (isPasswordCorrect(userID=check[1],password=password)):
                pass
            # 密碼錯誤
            else:
                session.clear()
                return '<script>alert("密碼錯誤");window.location.href = "/";</script>'
        # not user
        else:
            return '<script>alert("查無此人");window.location.href = "/";</script>'

    # 存入session  
    session["userID"] = check[1]  

    # todo del 
    debug.panel(title="/login",account=account,password = password)

    return redirect("/lastStep")

@app.route("/finishPay",methods=["POST"])
def finishPay():
    debug.yellow(session["userID"])
    return str(userPay(userID=session["userID"]))


@app.route("/signUp",methods=["POST"])
def signUp():
    # userID
    uuid = [str(uuid4())]
    # 時間戳
    timestamp = [datetime.timestamp(datetime.now())] 
    # 姓名 email school 科系 社團 password tel id birth 聯絡人 聯絡人關西 聯絡人電話  size 飲食習慣  特殊疾病  團報優惠碼
    data_values = request.form.getlist('data[]')
    male = request.form.getlist('data[male]')
    food = request.form.getlist('data[food]')
    isLive = request.form.getlist('data[live]')
    coupon = [generate_random_string()]
    #  todo     
    # 要船上去的資料
    result = uuid + data_values[0:7] + male + data_values[7:13] + food + data_values[13:15] + isLive + coupon + timestamp + [0,"",""]
    debug.hr()
    for i,d in enumerate(data_values):
        debug.yellow(str(i),d)
    debug.hr()
    
    debug.hr()
    for i,d in enumerate(result):
        debug.blue(str(i))
        debug.yellow(str(d))
    debug.hr()
    
    print(createUser(Data=result))
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

@app.route("/getCoupon",methods=["POST"])
def getCoupon():
    """
    核對團體優惠碼
    """ 
    return str(checkCoupon(request.data.decode("utf-8")))

# admin 
@app.route("/admin/login")
def adminLogin():
    return


if __name__ == "__main__":
    app.run(debug=True) 