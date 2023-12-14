from flask import Flask,render_template,request,session,redirect
from debug import debug
from os import urandom

app = Flask(__name__)
app.config['SECRET_KEY'] = urandom(24)

# 路由 Router
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign.html")
def sign():
    return render_template("sign.html")

@app.route("/success.html")
def success():
    return render_template("success.html")

@app.route("/lastStep.html")
def lastStep():
    return render_template("sign.html")


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

    return redirect("/sign.html")

if __name__ == "__main__":
    app.run(debug=True)