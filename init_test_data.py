from app.models.db import init_db
from app.models.user import UserRepository

init_db()

result = UserRepository.create_user('admin', '123456')
if result:
    print('✅ 测试账号创建成功: admin / 123456')
else:
    print('⚠️ 用户已存在')
