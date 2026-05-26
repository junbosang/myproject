# 程序的主入口
# 承担服务器容器+程序作用
# 程序服务器：提供http容器服务,程序放置于该容器中
# 程序：本体-智能瞭望与智能文数系统

import os
import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer

# 导入BaseHandler
from app.controllers.base import BaseHandler

# 引入controller层
from app.controllers.home import IndexHandler
from app.controllers.auth import LoginHandler, LogoutHandler, RegisterHandler
from app.controllers.admin import (
    DigitalEmployeeHandler, ModelEngineHandler, ChatAdminHandler,
    DataWarehouseHandler, WatchTowerHandler, InterfaceHandler, 
    DashboardHandler, SystemSettingsHandler
)
from app.controllers.chat import (
    ChatHomeHandler, ChatPrivateHandler, ChatGroupHandler,
    AddFriendHandler, CreateGroupHandler
)

# 数据库初始化
from app.models.db import init_db

# 私有页面处理器（必须登录）
class PrivateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.write(f"✅ 登录成功！欢迎你：{self.current_user}")

def make_app():
    base_url = os.path.dirname(os.path.abspath(__file__))
    settings = dict(
        template_path = os.path.join(base_url, "app", "templates"),
        static_path = os.path.join(base_url, "app", "static"),
        cookie_secret="demo-cookie-secret-change-me",
        login_url="/auth/login",
        xsrf_cookies=True,
        debug=True,
        autoreload=True
    )
    return tornado.web.Application([
        (r"/", IndexHandler),
        (r"/auth/login", LoginHandler),
        (r"/auth/logout", LogoutHandler),
        (r"/auth/register", RegisterHandler),
        (r"/private", PrivateHandler),
        
        # 管理模块路由
        (r"/admin/digital-employee", DigitalEmployeeHandler),
        (r"/admin/model-engine", ModelEngineHandler),
        (r"/admin/chat-admin", ChatAdminHandler),
        (r"/admin/data-warehouse", DataWarehouseHandler),
        (r"/admin/watch-tower", WatchTowerHandler),
        (r"/admin/interface", InterfaceHandler),
        (r"/admin/dashboard", DashboardHandler),
        (r"/admin/settings", SystemSettingsHandler),
        
        # 用户聊天模块路由
        (r"/chat/home", ChatHomeHandler),
        (r"/chat/private", ChatPrivateHandler),
        (r"/chat/group", ChatGroupHandler),
        (r"/chat/add-friend", AddFriendHandler),
        (r"/chat/create-group", CreateGroupHandler),
    ], **settings)

if __name__=="__main__":
    init_db()
    app = make_app()
    server = HTTPServer(app)
    server.bind(10086)
    server.start()

    print("======Server 启动成功=======端口 : 10086 ======", flush=True)
    # 修复ioloop启动错误
    tornado.ioloop.IOLoop.current().start()