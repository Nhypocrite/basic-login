from flask import Flask, render_template, redirect, url_for, request, jsonify, session, g
from flask_cors import CORS
import mysql.connector
import hashlib
import random
import os
from datetime import timedelta

app = Flask(__name__)
CORS(app)

# 设置 secret_key，用于 session 加密
app.secret_key = os.urandom(24)

# 配置数据库连接
db_config = {
    "user": "root",
    "password": "",
    "host": "localhost",
    "database": "web_programming",
    "charset": "utf8mb4",
    "collation": "utf8mb4_general_ci",
}

# 设置Session过期时间
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


# 优化：使用 g 对象存储数据库连接，避免每次请求都创建新的数据库连接
# 获取数据库连接
def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db


# 关闭数据库连接
@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


# 密码加密函数
def hash_password(password):
    salt = "NTUSALT1234"
    return hashlib.sha256((password + salt).encode("utf-8")).hexdigest()


# 注册用户
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        encrypted_password = hash_password(request.form["password"])

        # 插入用户数据到数据库
        try:
            connection = get_db()
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, encrypted_password))
            connection.commit()
            cursor.close()
            return redirect(url_for("login"))
        except mysql.connector.IntegrityError:  # 用户名重复
            return "Username already exists.", 400
        except mysql.connector.Error as err:
            return "An error occurred. Please try again later.", 500
    return render_template("register.html")


# 登录用户
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        encrypted_password = hash_password(request.form["password"])

        # 获取数据库连接并查找用户
        connection = get_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        # 验证密码
        if user and user[2] == encrypted_password:

            session["user_id"] = user[0]
            session["username"] = user[1]

            # 处理 "Remember me" 功能
            if request.form.get("remember_me"):
                session.permanent = True  # 启用持久化session（和上面设置一样，保存7天）
            else:
                session.permanent = False  # 启用短时session（浏览器关闭时即失效）

            return redirect(url_for("index"))

        cursor.close()

    return render_template("login.html")


# 注销用户
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    session.pop("username", None)
    return redirect(url_for("login"))


# 主页
@app.route("/")
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return render_template("index.html", username=session["username"])


if __name__ == "__main__":
    app.run(debug=True)
