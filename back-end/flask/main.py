from flask import Flask,render_template,request,session,redirect,jsonify
from debug import debug
from os import urandom
from uuid import uuid4
from datetime import datetime
from random import choice
from re import match

from db import *

def timestamp_to_date(timestamp):
    # 将时间戳转换为datetime对象
    dt_object = datetime.utcfromtimestamp(timestamp)
    # 使用strftime方法格式化日期和时间
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date


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

def generate_random_string(length=6):
    key = "ABCDEFGHJKMNPQRSTUVWXYZ23456789"    
    random_string = ''.join(choice(key) for _ in range(length))
    return random_string

def is_email(input_str):
    # 定義電子郵件地址的正規表達式
    if input_str and '@' in input_str:
        return True
    else:
        return False
    # email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # return match(email_pattern, input_str) is not None

# 路由 Router
@app.route("/login")
def home():
    if checkLogin():
        debug.bg_yellow(session["userID"])
        return redirect("/lastStep")

    return render_template("home.html")

@app.route("/")
def index():
    return render_template("/index.html")

@app.route("/sitemap.xml")
def sitemap():
    return render_template("sitemap.xml")

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
    if not(checkLogin()):
        return redirect("/")
    
    return render_template("edit.html")

# 完成
@app.route("/success")
def success():
    if not(checkLogin()):
        return redirect("/")
    return render_template("success.html",coupon = FinishGetCoupon(UserID=session["userID"]))

# 最後一步
@app.route("/lastStep")
def lastStep():
    if not(checkLogin()):
        return redirect("/")
    if getUserStatus(UserID=session["userID"]):
        return redirect("/success")

    # coupon,isPaid,consentID,maintenance
    result = getUserLastStep(UserID=session["userID"])[0]
    debug.yellow(str(result))
    return render_template("lastStep.html",coupon=result[0],isPaid=result[1],consent=result[2],maintenance=result[3],adminCheck=result[4],userID=session["userID"])

# 家長同意書
@app.route("/consent")
def consent():
    if not(checkLogin()):
        return redirect("/")
    
    session["agreement"] = 0

    student_id = session["userID"]
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("consent.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

# 場地切結書
@app.route("/maintenance")
def maintenance():
    if not(checkLogin()):
        return redirect("/")
    
    session["agreement"] = 1
    student_id = session["userID"]
    debug.bg_yellow(student_id)
    # 姓名、手機、家長姓名、家長手機
    # name,phone,emergencyContact,emergencyPhone
    data = getStudentData(student_id)
    return render_template("maintenance.html",name=data[0],phone=data[1],emergencyContact=data[2],emergencyPhone=data[3])

@app.route("/error")
def error():
    return render_template("error.html")

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
    if not(checkLogin()):
        return redirect("/")
    return str(userPay(userID=session["userID"],timestamp=datetime.timestamp(datetime.now())+28800))


@app.route("/signUp",methods=["POST"])
def signUp():
    # userID
    uuid = [str(uuid4())]
    # 時間戳    
    timestamp = [datetime.timestamp(datetime.now())+28800] 
    # 姓名 email school 科系 社團 password tel id birth 聯絡人 聯絡人關西 聯絡人電話  size 飲食習慣  特殊疾病  團報優惠碼
    data_values = request.form.getlist('data[]')
    male = request.form.getlist('data[male]')
    food = request.form.getlist('data[food]')
    isLive = request.form.getlist('data[live]')
    if checkUserExist(email=data_values[1],phone=data_values[6]):
        return '<script>alert("帳號已存在");window.location.href = "/sign";</script>'
    
    if not(checkCoupon(inputCoupon=data_values[-1])):
        print("not exist")
        data_values[-1] = ""
        
    result = uuid + data_values[0:7] + male + data_values[7:13] + food + data_values[13:15] + isLive + [data_values[15]]+ timestamp + [0,"","","",""]
    createUser(Data=result)

    session["userID"] = str(uuid[0])

    return redirect("/lastStep")

@app.route("/sendSign",methods=["POST"])
def sendSign():
        # 获取POST请求的原始数据
    data = request.data.decode('utf-8')
    
    if not(checkLogin()):
        return redirect("/")
    debug.panel("sign",str(signConsent(userID=session["userID"],consentID=session["agreement"],signData=data)))
    return str(True)

    # try:
    #     pass
    # except Exception as e:
    #     debug.panel("error",str(e))
    #     # print('Error:', str(e))
    #     return 'Error occurred'

@app.route("/getCoupon",methods=["POST"])
def getCoupon():
    """
    核對團體優惠碼
    """ 
    data = request.data.decode("utf-8")
    
    if data:
        return str(checkCoupon(data))
    else:
        return str(False)

# admin 
# 管理者頁面
def adminCheck():
    try:
        session["admin"]
        session["adminAccount"]
        return True
    except:
        return False

@app.route("/admin")
def admin():
    return render_template("admin/login.html")

@app.route("/admin/manage")
def adminLoginPage():
    if not(adminCheck()):
        return redirect('/admin')
    data = getAllStudent()
    modified_data = []  # 用于存储修改后的数据
    
    for item in data:
        # 将元组转换为列表以便修改
        item_list = list(item)
        
        # 修改元素，假设 'timestamp' 是元组的第一个元素
        timestamp_index = 20
        item_list[timestamp_index] = timestamp_to_date(float(item_list[timestamp_index]))
        if item_list[24]:
            item_list[24] = timestamp_to_date(float(item_list[24]))
        
        # 将修改后的列表添加到新的数据集
        modified_data.append(tuple(item_list))
    
    return render_template("admin/admin.html", data=modified_data)

@app.route("/admin/getStudentData",methods=["POST"])
def AdminGetStudentData():
    if not(adminCheck()):
        return redirect('/admin')
    stuID = request.data.decode("utf-8")
    data = list(getUserData(UserID=stuID)[0])
    data[20] = timestamp_to_date(float(data[20]))
    if data[24]:
        data[24] = timestamp_to_date(float(data[24]))
    return jsonify(data)

@app.route("/admin/setPay",methods=["POST"])
def AdminSetPay():
    if not(adminCheck()):
        return redirect('/admin')
    stuID = request.data.decode("utf-8")
    if checkUserPay(userID=stuID):
        setUserCoupon(userID=stuID,data=generate_random_string())
        return "True"
    else:
        return "False"
    
@app.route("/admin/login",methods=["POST"])
def adminLogin():
    account = request.form.get("account")
    # todo 加密
    password = request.form.get("password")

    if (isAdminPasswordCorrect(account=account,password=password)):
        session["admin"] = True
        session["adminAccount"] = account
        return redirect("/admin/manage")
    else:
        return "<script>alert('密碼錯誤');window.location.href='/admin';</script>"

# 拿來備份資料，應該沒有問題 by 毛哥
@app.route("/admin/getAllData",methods=["GET"])
def AdminGetAllData():
    if not(adminCheck()):
        return redirect('/admin')
    data = getAllData()
    return data
        

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0", port=80) 
