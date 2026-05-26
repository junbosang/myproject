import tornado.web
import json
import random
from app.controllers.base import BaseHandler
from app.models.chat import ChatRepository
from app.models.user import UserRepository
from app.models.digital_employee import DigitalEmployeeRepository

class ChatHomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = UserRepository.get_user_by_username(self.current_user)
        friends = ChatRepository.get_friends(current_user['id'])
        groups = ChatRepository.get_groups(current_user['id'])
        employees = DigitalEmployeeRepository.get_all()
        users = ChatRepository.get_users_except(current_user['id'])
        self.render("chat/home.html", 
                   title="智能聊天", 
                   username=self.current_user,
                   friends=friends, groups=groups, employees=employees,
                   all_users=users, current_user=current_user)

class ChatPrivateHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        friend_id = self.get_argument("friend_id")
        current_user = UserRepository.get_user_by_username(self.current_user)
        friend = UserRepository.get_user_by_id(friend_id)
        messages = ChatRepository.get_messages(friend_id, 'private')
        self.render("chat/private.html", 
                   title=f"与 {friend['username']} 聊天", 
                   username=self.current_user,
                   friend=friend, messages=messages, current_user=current_user)
    
    @tornado.web.authenticated
    def post(self):
        friend_id = self.get_argument("friend_id")
        content = self.get_argument("content")
        current_user = UserRepository.get_user_by_username(self.current_user)
        
        ChatRepository.send_message(current_user['id'], friend_id, 'private', content)
        
        # 数字员工自动回复
        friend = UserRepository.get_user_by_id(friend_id)
        if friend and friend['username'] in ['川农小助手', '天气小助手', '毒鸡汤助手', '新闻助手', '电影助手']:
            response = self._get_employee_response(friend['username'], content)
            ChatRepository.send_message(friend_id, current_user['id'], 'private', response)
        
        self.redirect(f"/chat/private?friend_id={friend_id}")
    
    def _get_employee_response(self, emp_name, user_msg):
        if emp_name == '毒鸡汤助手':
            soups = [
                "努力不一定成功，但不努力真的很舒服 😊",
                "不要在意别人的看法，其实别人根本没在看你",
                "世上无难事，只要肯放弃",
                "比你优秀的人还在努力，那你努力还有什么用",
                "不是路不平，而是你不行",
                "人生没有过不去的坎，只有过不完的坎"
            ]
            return random.choice(soups)
        elif emp_name == '天气小助手':
            cities = ['北京', '上海', '成都', '广州', '深圳', '杭州', '武汉', '西安', '南京', '重庆']
            city = user_msg.strip()
            if city not in cities:
                city = random.choice(cities)
            weathers = ['晴朗 ☀️', '多云 ⛅', '小雨 🌧️', '阴天 ☁️', '雷阵雨 ⛈️']
            temps = [f"{random.randint(10,35)}°C"]
            return f"【{city}天气】{random.choice(weathers)}，温度{random.choice(temps)}，空气质量良好。"
        elif emp_name == '川农小助手':
            responses = [
                "四川农业大学是一所以生物科技为特色，农业科技为优势的国家211工程重点大学",
                "川农有雅安、成都、都江堰三个校区，风景优美，学风优良",
                "川农的动物科学、动物医学、林学等专业在全国都很有名气",
                "欢迎你报考四川农业大学！",
                "川农校训：追求真理、造福社会、自强不息"
            ]
            return random.choice(responses)
        elif emp_name == '新闻助手':
            news = [
                "【科技】AI技术在农业领域的应用正在快速发展",
                "【教育】高校教育改革新政策将于下月实施",
                "【娱乐】新上映的多部电影票房破亿",
                "【体育】国际赛事中国队取得优异成绩"
            ]
            return random.choice(news)
        elif emp_name == '电影助手':
            movies = [
                "推荐最近热门：《流浪地球3》科幻巨制震撼来袭",
                "推荐经典：《肖申克的救赎》永远的豆瓣第一",
                "推荐喜剧：《开心麻花》系列让你笑出眼泪",
                "推荐动画：《寻梦环游记》温馨感人"
            ]
            return random.choice(movies)
        return "收到！我正在思考..."

class ChatGroupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        group_id = self.get_argument("group_id")
        current_user = UserRepository.get_user_by_username(self.current_user)
        group = ChatRepository.get_group(group_id)
        members = ChatRepository.get_group_members(group_id)
        messages = ChatRepository.get_messages(group_id, 'group')
        self.render("chat/group.html", 
                   title=f"群聊 - {group['name']}", 
                   username=self.current_user,
                   group=group, messages=messages, 
                   members=members, current_user=current_user)
    
    @tornado.web.authenticated
    def post(self):
        group_id = self.get_argument("group_id")
        content = self.get_argument("content")
        current_user = UserRepository.get_user_by_username(self.current_user)
        
        ChatRepository.send_message(current_user['id'], group_id, 'group', content)
        
        # 检查是否@了数字员工
        if '@川农小助手' in content:
            ChatRepository.send_message(0, group_id, 'group', "🤖 川农小助手：四川农业大学是一所很棒的学校！")
        if '@天气小助手' in content:
            ChatRepository.send_message(0, group_id, 'group', "☀️ 天气小助手：今天天气晴朗，适合出门！")
        if '@毒鸡汤助手' in content:
            soup = "努力不一定成功，但不努力真的很舒服 😊"
            ChatRepository.send_message(0, group_id, 'group', f"☕ 毒鸡汤助手：{soup}")
        
        self.redirect(f"/chat/group?group_id={group_id}")

class AddFriendHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        friend_id = self.get_argument("friend_id")
        current_user = UserRepository.get_user_by_username(self.current_user)
        ChatRepository.add_friend(current_user['id'], friend_id)
        self.redirect("/chat/home")

class CreateGroupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = UserRepository.get_user_by_username(self.current_user)
        friends = ChatRepository.get_friends(current_user['id'])
        employees = DigitalEmployeeRepository.get_all()
        self.render("chat/create_group.html", 
                   title="创建群聊", 
                   username=self.current_user,
                   friends=friends, employees=employees)
    
    @tornado.web.authenticated
    def post(self):
        name = self.get_argument("name")
        announcement = self.get_argument("announcement", "")
        member_ids = self.get_arguments("member_ids")
        current_user = UserRepository.get_user_by_username(self.current_user)
        
        group_id = ChatRepository.create_group(name, current_user['id'], announcement)
        for member_id in member_ids:
            ChatRepository.add_group_member(group_id, member_id)
        
        self.redirect("/chat/home")
