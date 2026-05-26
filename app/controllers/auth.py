# 认证相关 controller(登录/注册/退出)
# 通过Handler 展示 mvc 中controller 层 如何接收表单, 校验输入, 调用model层, 再渲染view层 或 跳转
# 登录态 用 secure cookie 保存username

import tornado.web

from app.controllers.base import BaseHandler
from app.models.user import UserRepository

class LoginHandler(BaseHandler):
    # /auth/login
    # get:渲染登录页
    # post:校验用户名和密码,通过后写入secure cookie 并跳转到目标页
    def get(self):
        # self.write(f"""<h3>登录</h3>
        # <form method="post" action="/auth/login">
        # <input name="username">
        # <input name="password">
        # <button type="submit">登录admin</button>
        # {self.xsrf_form_html()}
        # </form>
        # """)
        self.render("login.html", title="登录", error=None, is_login_page=True)

    def post(self):
        username = (self.get_body_argument("username", "") or "").strip()
        password = self.get_body_argument("password", "")
        if not username or not password:
            self.set_status(400)
            # return self.write(f"""<h3>登录</h3>
            # 用户名或密码不能为空或输入了无效数据
            # <form method="post" action="/auth/login">
            # <input name="username">
            # <input name="password">
            # <button type="submit">登录admin</button>
            # {self.xsrf_form_html()}
            # </form>
            # """)
            return self.render("login.html", title="登录", error="用户名或密码不能为空或输入了无效数据", is_login_page=True)

        if not UserRepository.verify_user(username, password):
            self.set_status(401)
            # return self.write(f"""<h3>登录</h3>
            # 用户名或密码错误
            # <form method="post" action="/auth/login">
            # <input name="username">
            # <input name="password">
            # <button type="submit">登录admin</button>
            # {self.xsrf_form_html()}
            # </form>
            # """)
            return self.render("login.html", title="登录", error="用户名或密码错误", is_login_page=True)



        self.set_secure_cookie("username",username)
        # self.write(f"登录成功,欢迎:{username}")
        self.redirect("/")

class RegisterHandler(BaseHandler):
    def get(self):
        self.render("register.html", title="注册", error=None, success=None, is_login_page=True)

    def post(self):
        username = (self.get_body_argument("username", "") or "").strip()
        password = self.get_body_argument("password", "")
        confirm = self.get_body_argument("confirm_password", "")

        if not username or not password:
            return self.render("register.html", title="注册", error="用户名和密码不能为空", success=None, is_login_page=True)
        if len(username) < 3:
            return self.render("register.html", title="注册", error="用户名至少需要3个字符", success=None, is_login_page=True)
        if len(password) < 6:
            return self.render("register.html", title="注册", error="密码至少需要6个字符", success=None, is_login_page=True)
        if password != confirm:
            return self.render("register.html", title="注册", error="两次输入的密码不一致", success=None, is_login_page=True)
        if UserRepository.get_user_by_username(username):
            return self.render("register.html", title="注册", error="用户名已存在", success=None, is_login_page=True)

        UserRepository.create_user(username, password)
        return self.render("register.html", title="注册", error=None, success="注册成功！请登录", is_login_page=True)

class LogoutHandler(BaseHandler):
# /auth/logout
    def post(self):
        self.clear_cookie("username")
        self.redirect("/auth/login")