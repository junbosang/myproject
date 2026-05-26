import tornado.web
from app.controllers.base import BaseHandler
from app.models.digital_employee import DigitalEmployeeRepository
from app.models.model_engine import ModelEngineRepository
from app.models.chat import ChatRepository
from app.models.user import UserRepository
from app.models.db import init_db
import json

class DigitalEmployeeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        employees = DigitalEmployeeRepository.get_all()
        self.render("admin/digital_employee.html", 
                   title="数字员工管理", 
                   username=self.current_user,
                   employees=employees)
    
    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", "")
        if action == "create":
            name = self.get_argument("name")
            emp_type = self.get_argument("type")
            description = self.get_argument("description", "")
            avatar = self.get_argument("avatar", "🤖")
            prompt = self.get_argument("prompt", "")
            DigitalEmployeeRepository.create(name, emp_type, description, avatar, prompt)
        elif action == "update":
            emp_id = self.get_argument("id")
            name = self.get_argument("name")
            emp_type = self.get_argument("type")
            description = self.get_argument("description", "")
            avatar = self.get_argument("avatar", "🤖")
            prompt = self.get_argument("prompt", "")
            status = self.get_argument("status", "active")
            DigitalEmployeeRepository.update(emp_id, name, emp_type, description, avatar, prompt, status)
        elif action == "delete":
            emp_id = self.get_argument("id")
            DigitalEmployeeRepository.delete(emp_id)
        self.redirect("/admin/digital-employee")

class ModelEngineHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        models = ModelEngineRepository.get_all()
        self.render("admin/model_engine.html", 
                   title="模型引擎管理", 
                   username=self.current_user,
                   models=models)
    
    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", "")
        if action == "create":
            name = self.get_argument("name")
            model_type = self.get_argument("type", "llm")
            is_local = self.get_argument("is_local", "0") == "1"
            api_endpoint = self.get_argument("api_endpoint", "")
            api_key = self.get_argument("api_key", "")
            token_limit = int(self.get_argument("token_limit", "4096"))
            streaming = self.get_argument("streaming", "1") == "1"
            ModelEngineRepository.create(name, model_type, is_local, api_endpoint, api_key, token_limit, streaming)
        elif action == "update":
            model_id = self.get_argument("id")
            name = self.get_argument("name")
            model_type = self.get_argument("type", "llm")
            is_local = self.get_argument("is_local", "0") == "1"
            api_endpoint = self.get_argument("api_endpoint", "")
            api_key = self.get_argument("api_key", "")
            token_limit = int(self.get_argument("token_limit", "4096"))
            streaming = self.get_argument("streaming", "1") == "1"
            status = self.get_argument("status", "active")
            ModelEngineRepository.update(model_id, name, model_type, is_local, api_endpoint, api_key, token_limit, streaming, status)
        elif action == "delete":
            model_id = self.get_argument("id")
            ModelEngineRepository.delete(model_id)
        self.redirect("/admin/model-engine")

class ChatAdminHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        groups = ChatRepository.get_all_groups()
        files = ChatRepository.get_all_files()
        self.render("admin/chat_admin.html", 
                   title="智能聊天管理", 
                   username=self.current_user,
                   groups=groups, files=files)
    
    @tornado.web.authenticated
    def post(self):
        action = self.get_argument("action", "")
        group_id = self.get_argument("group_id", "")
        if action == "delete_group":
            ChatRepository.delete_group(group_id)
        elif action == "ban_group":
            ChatRepository.update_group_status(group_id, "banned")
        elif action == "active_group":
            ChatRepository.update_group_status(group_id, "active")
        elif action == "update_announcement":
            announcement = self.get_argument("announcement", "")
            ChatRepository.update_group_announcement(group_id, announcement)
        self.redirect("/admin/chat-admin")

class DataWarehouseHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/data_warehouse.html", 
                   title="数据仓库", 
                   username=self.current_user)

class WatchTowerHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/watch_tower.html", 
                   title="瞭望管理", 
                   username=self.current_user)

class InterfaceHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/interface.html", 
                   title="接口管理", 
                   username=self.current_user)

class DashboardHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("admin/dashboard.html", 
                   title="数智大屏", 
                   username=self.current_user)

class SystemSettingsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        init_db()
        self.render("admin/settings.html", 
                   title="系统设置", 
                   username=self.current_user)
