# 每一个Url对应一个RequestHandler，可以理解为Controller
# RequestHandler 提供 post / get 等方法来处理http请求
# 本程序可以提供一个统一的基础类，用于处理一些公共业务，如登录态的处理或获得逻辑，供其他Handler继承使用


import tornado.web

class BaseHandler(tornado.web.RequestHandler):
    # 公共类的用户态认证机制：
    # - 框架会通过 get_current_user() 的返回值来判断是否"已经登录"
    # - 如果返回None，则 @tornado.web.authenticated 装饰器会触发跳转到指定的路由URL: login_url
    def get_current_user(self):
        # 返回当前登录用户的字符串 或 None
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode('utf-8')

    def render(self, template_name, **kwargs):
        if 'is_login_page' not in kwargs:
            kwargs['is_login_page'] = False
        if 'username' not in kwargs:
            kwargs['username'] = self.current_user or ''
        if 'title' not in kwargs:
            kwargs['title'] = '控制台'
        return super().render(template_name, **kwargs)