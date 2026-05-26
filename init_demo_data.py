
import sys
import os

project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from app.models.db import init_db, get_connection
from app.models.user import UserRepository

print("正在初始化数据库...")
init_db()

print("正在创建测试账号...")
result = UserRepository.create_user('admin', '123456')
print(f"admin/123456 创建 {'成功' if result else '已存在'}")

result = UserRepository.create_user('admin1', '123456')
print(f"admin1/123456 创建 {'成功' if result else '已存在'}")

print("正在添加数字员工作为用户...")
employees = [
    ('川农小助手', '123456'),
    ('天气小助手', '123456'),
    ('毒鸡汤助手', '123456'),
    ('新闻助手', '123456'),
    ('电影助手', '123456')
]

for emp, pwd in employees:
    result = UserRepository.create_user(emp, pwd)
    print(f"{emp}/123456 创建 {'成功' if result else '已存在'}")

print("初始化完成！")
