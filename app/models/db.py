#数据库链接与建表
import os
import sqlite3


# 获得项目根路径的方法
def _project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
#获得数据库连接
DB_PATH = os.path.join(_project_root(),"database","app.db")

def get_connection():
    os.makedirs(os.path.dirname(DB_PATH),exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
#
def init_db():
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id integer PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                create_at TEXT NOT NULL DEFAULT(datetime('now')),
                avatar TEXT,
                status TEXT DEFAULT 'online'
            )
            """
        )
        # 数字员工表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS digital_employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                description TEXT,
                avatar TEXT,
                prompt TEXT,
                status TEXT DEFAULT 'active',
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 模型引擎表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS model_engines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT,
                api_endpoint TEXT,
                api_key TEXT,
                is_local INTEGER DEFAULT 0,
                token_limit INTEGER DEFAULT 4096,
                streaming INTEGER DEFAULT 1,
                status TEXT DEFAULT 'active',
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 系统配置表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS system_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                config_key TEXT NOT NULL UNIQUE,
                config_value TEXT,
                config_type TEXT DEFAULT 'string',
                description TEXT
            )
        """)
        # 聊天用户关系表（好友）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_friends (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                create_at TEXT DEFAULT(datetime('now')),
                UNIQUE(user_id, friend_id)
            )
        """)
        # 群聊表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                owner_id INTEGER NOT NULL,
                avatar TEXT,
                announcement TEXT,
                status TEXT DEFAULT 'active',
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 群成员表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                is_admin INTEGER DEFAULT 0,
                join_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 聊天消息表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                target_type TEXT NOT NULL DEFAULT 'private',
                content TEXT NOT NULL,
                message_type TEXT DEFAULT 'text',
                file_url TEXT,
                read_at TEXT,
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 文件表（支持去重）
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_hash TEXT NOT NULL UNIQUE,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_size INTEGER,
                file_type TEXT,
                uploader_id INTEGER,
                upload_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 瞭望源表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS watch_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                url TEXT,
                type TEXT,
                config TEXT,
                status TEXT DEFAULT 'active',
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 舆情数据表
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sentiment_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_type TEXT,
                source_id INTEGER,
                content TEXT,
                sentiment_score REAL,
                risk_level TEXT,
                create_at TEXT DEFAULT(datetime('now'))
            )
        """)
        # 初始化默认数据
        _init_default_data(conn)

def _init_default_data(conn):
    # 检查是否已有数字员工
    cursor = conn.execute("SELECT COUNT(*) as cnt FROM digital_employees")
    if cursor.fetchone()['cnt'] == 0:
        employees = [
            ('川农小助手', 'knowledge', '回答关于四川农业大学的问题', '🤖', '你是四川农业大学的专业助手，请只回答关于川农的相关问题'),
            ('天气小助手', 'weather', '查询指定城市的天气信息', '☀️', '你是天气查询助手，用户输入城市名后你返回天气信息'),
            ('毒鸡汤助手', 'emotion', '随机回复毒鸡汤语句', '☕', '你是毒鸡汤助手，会随机回复一些毒鸡汤内容'),
            ('新闻助手', 'news', '提供最新资讯推送', '📰', '你是新闻资讯助手'),
            ('电影助手', 'movie', '推荐电影娱乐内容', '🎬', '你是电影推荐助手')
        ]
        for emp in employees:
            conn.execute("""
                INSERT INTO digital_employees (name, type, description, avatar, prompt, status) 
                VALUES (?, ?, ?, ?, ?, 'active')
            """, emp)
    
    # 检查是否有模型引擎
    cursor = conn.execute("SELECT COUNT(*) as cnt FROM model_engines")
    if cursor.fetchone()['cnt'] == 0:
        conn.execute("""
            INSERT INTO model_engines (name, type, is_local, token_limit, streaming, status) 
            VALUES ('本地模型', 'llm', 1, 4096, 1, 'active')
        """)
        conn.execute("""
            INSERT INTO model_engines (name, type, is_local, token_limit, streaming, status) 
            VALUES ('云端模型', 'llm', 0, 8192, 1, 'active')
        """)
    
    # 初始化系统配置
    configs = [
        ('database_type', 'sqlite', 'string', '数据库类型: sqlite/mysql'),
        ('login_failure_limit', '5', 'number', '登录失败限制次数'),
        ('session_timeout', '3600', 'number', '会话超时秒数'),
        ('upload_max_size', '52428800', 'number', '最大上传大小(字节)')
    ]
    for cfg in configs:
        try:
            conn.execute("""
                INSERT INTO system_config (config_key, config_value, config_type, description) 
                VALUES (?, ?, ?, ?)
            """, cfg)
        except sqlite3.IntegrityError:
            pass
