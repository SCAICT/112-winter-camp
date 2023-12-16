from flask import Flask,render_template,request,session,redirect
from debug import debug
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)

def checkLogin() -> bool:
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
    return render_template("consent.html")


# api
@app.route("/login",methods=["POST"])
def login():
    # 讀取資料
    account = request.form.get("account")
    password = request.form.get("password")

    # 存入session
    session["account"] = account
    session["password"] = password

    # todo del 
    debug.panel(title="/login",account=account,password = password)

    return redirect("/sign")

@app.route("/signUp",methods=["POST"])
def signUp():
    data_values = request.form.getlist('data[]')
    male = request.form.getlist('data[male]')
    food = request.form.getlist('data[food]')   
    session["code"] = data_values[14]
    # debug.blue(data_values)
    for d in data_values:
        debug.yellow(d)
        
    debug.yellow(str(male))
    debug.yellow(str(food))

    session["test"]

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



if __name__ == "__main__":
    app.run(debug=True)