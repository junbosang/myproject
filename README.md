# cnAgentOS - AI智能问答与智能词表系统

> 项目学习文档 | 基于 Tornado MVC + Web 架构

---

## 一、项目概述

### 1.1 项目定位
cnAgentOS 是一个基于 **Tornado MVC 架构** 的 Web 应用系统，定位为 **AI智能瞭望与智能文数系统**。当前已完成基础框架搭建和登录认证功能，后续将扩展 **AI智能问答** 与 **智能词表** 核心业务模块。

### 1.2 技术栈

| 层级 | 技术 | 版本/说明 |
|------|------|-----------|
| 后端语言 | Python | 3.12（venv 中 pyc 文件显示为 cpython-312） |
| Web 框架 | Tornado | 6.5.5 |
| 数据库 | SQLite3 | 内置，文件型数据库 |
| 前端 | HTML5 + CSS + JavaScript | 模板引擎：Tornado 内置模板 |
| 密码加密 | PBKDF2-HMAC-SHA256 | 10万次迭代 + 随机盐值 |
| 会话管理 | Secure Cookie | Tornado 内置安全 Cookie 机制 |

### 1.3 运行环境
- **服务端口**: `10086`
- **数据库文件**: `database/app.db`
- **虚拟环境**: `venv/`（Python 虚拟环境）
- **启动命令**: `python app.py`

---

## 二、项目目录结构

```
cnAgentOS/
├── app.py                          # 【主入口】程序启动、路由配置、服务器容器
├── test.py                         # 【测试脚本】数据库初始化、用户CRUD、登录验证测试
├── app.md                          # 【项目说明】目录结构记录文件
│
├── app/                            # 【应用核心包】MVC 三层架构
│   ├── __init__.py                 # 包初始化（空文件）
│   │
│   ├── controllers/                # 【控制层 C】RequestHandler，处理 HTTP 请求
│   │   ├── __init__.py             # 包说明文档
│   │   ├── base.py                 # 基础 Handler：用户态认证（get_current_user）
│   │   ├── home.py                 # 首页/后台 Handler
│   │   └── auth.py                 # 认证 Handler（登录/登出/注册）
│   │
│   ├── models/                     # 【模型层 M】数据库操作、业务逻辑
│   │   ├── __init__.py             # 包初始化（空文件）
│   │   ├── db.py                   # 数据库连接管理、建表初始化
│   │   └── user.py                 # 用户模型：创建/查询/验证、密码加密
│   │
│   ├── templates/                  # 【视图层 V】HTML 模板（Tornado 模板语法）
│   │   ├── base.html               # 基础布局模板（继承父模板）
│   │   ├── login.html              # 登录页模板
│   │   ├── index.html              # 后台首页模板
│   │   └── register.html           # 注册页模板（空文件，待开发）
│   │
│   └── static/                     # 【静态资源】CSS/JS/图片等
│       ├── css/                    # 样式文件目录（当前为空，待补充 base.css）
│       └── js/                     # 脚本文件目录（当前为空，待补充 base.js）
│
├── database/                       # 【数据库目录】
│   └── app.db                      # SQLite 数据库文件
│
└── venv/                           # 【Python 虚拟环境】
    └── Lib/site-packages/          # 第三方依赖包（pip、tornado 等）
```

---

## 三、架构设计详解

### 3.1 整体架构：Tornado MVC + Web

```
┌─────────────────────────────────────────────────────────┐
│                      app.py (主入口)                      │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Tornado Application (HTTP 服务器容器)              │  │
│  │  ├── 路由配置 (URL → Handler 映射)                  │  │
│  │  ├── 全局设置 (模板路径/静态路径/Cookie/调试模式)     │  │
│  │  └── HTTPServer 绑定端口 10086                     │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
   │ Controllers  │ │   Models    │ │  Templates  │
   │  (控制层)     │ │  (模型层)    │ │  (视图层)    │
   │             │ │             │ │             │
   │ base.py     │ │ db.py       │ │ base.html   │
   │ home.py     │ │ user.py     │ │ login.html  │
   │ auth.py     │ │             │ │ index.html  │
   └─────────────┘ └─────────────┘ └─────────────┘
```

### 3.2 请求处理流程

```
用户请求 → URL 路由匹配 → Handler.get()/post()
                                    │
                                    ▼
                          参数校验 (get_body_argument)
                                    │
                                    ▼
                          调用 Model 层 (UserRepository)
                                    │
                                    ▼
                          渲染 Template 或 redirect 跳转
```

### 3.3 认证机制流程

```
登录请求 POST /auth/login
    │
    ▼
LoginHandler.post()
    │
    ├── 1. 获取表单参数 (username, password)
    │
    ├── 2. 参数非空校验 → 失败则返回 login.html + error 提示
    │
    ├── 3. UserRepository.verify_user(username, password)
    │       │
    │       ├── 3.1 根据 username 查询数据库
    │       ├── 3.2 取出 salt，重新计算 password_hash
    │       └── 3.3 比对 hash 值 → 返回 True/False
    │
    ├── 4. 验证失败 → 返回 login.html + "用户名或密码错误"
    │
    └── 5. 验证成功 → set_secure_cookie("username", username)
                      → redirect("/") 跳转到首页
```

---

## 四、核心代码模块详解

### 4.1 主入口 `app.py`

**职责**: 程序启动入口、HTTP 服务器容器、路由配置

**关键配置**:
```python
settings = dict(
    template_path = "app/templates",        # 模板文件路径
    static_path = "app/static",             # 静态文件路径
    cookie_secret = "demo-cookie-secret-change-me",  # Cookie 加密密钥（⚠️ 生产环境需更换）
    login_url = "/auth/login",              # 未登录跳转地址
    xsrf_cookies = True,                    # 开启 XSRF 防护
    debug = True,                           # 调试模式
    autoreload = True                       # 代码变更自动重启
)
```

**当前路由表**:

| URL 路径 | Handler | 方法 | 说明 | 认证要求 |
|----------|---------|------|------|----------|
| `/` | `IndexHandler` | GET | 首页/后台 | ✅ 需要登录 |
| `/auth/login` | `LoginHandler` (app.py 内联版) | GET/POST | 登录页 | ❌ 无需登录 |
| `/auth/logout` | `LogoutHandler` (app.py 内联版) | GET | 登出 | ❌ 无需登录 |
| `/private` | `PrivateHandler` | GET | 私有页面 | ✅ 需要登录 |

> **⚠️ 重要发现**: `app.py` 中定义了内联的 `LoginHandler`/`LogoutHandler`/`PrivateHandler`，
> 而 `app/controllers/auth.py` 中也定义了更完善的 `LoginHandler`/`LogoutHandler`。
> **当前路由指向的是 app.py 内联版本**（硬编码 admin/123456 验证），
> 而 `auth.py` 中的版本使用数据库验证（`UserRepository.verify_user`）。
> **后续开发需要统一路由指向，建议使用 `auth.py` 中的数据库验证版本。**

### 4.2 控制层 (Controllers)

#### 4.2.1 `base.py` - 基础 Handler

```python
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        """从 secure cookie 中获取当前登录用户名"""
        username = self.get_secure_cookie("username")
        if not username:
            return None
        return username.decode('utf-8')
```

**作用**:
- 继承自 `tornado.web.RequestHandler`
- 提供 `get_current_user()` 方法，实现用户态认证
- 配合 `@tornado.web.authenticated` 装饰器使用
- 当返回 `None` 时，框架自动跳转到 `login_url` 配置的路由

#### 4.2.2 `home.py` - 首页 Handler

```python
class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html", title="后台", username=self.current_user)
```

**作用**: 渲染后台首页，传递用户名到模板

#### 4.2.3 `auth.py` - 认证 Handler（数据库验证版）

```python
class LoginHandler(BaseHandler):
    def get(self):
        """GET: 渲染登录页"""
        self.render("login.html", title="登录", error=None)

    def post(self):
        """POST: 处理登录表单提交"""
        # 1. 获取并清理参数
        username = (self.get_body_argument("username", "") or "").strip()
        password = self.get_body_argument("password", "")

        # 2. 非空校验
        if not username or not password:
            return self.render("login.html", title="登录", error="用户名或密码不能为空...")

        # 3. 数据库验证
        if not UserRepository.verify_user(username, password):
            return self.render("login.html", title="登录", error="用户名或密码错误")

        # 4. 写入 Cookie 并跳转
        self.set_secure_cookie("username", username)
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def post(self):
        """POST: 清除 Cookie 并跳转回登录页"""
        self.clear_cookie("username")
        self.redirect("/auth/login")
```

**设计亮点**:
- 使用 `get_body_argument()` 安全获取表单参数
- 参数 strip() 清理空白字符
- 分层错误提示（空参数 vs 验证失败）
- 使用模板渲染替代内联 HTML 字符串
- 登出使用 POST 方法（符合 RESTful 规范，防止 CSRF）

### 4.3 模型层 (Models)

#### 4.3.1 `db.py` - 数据库管理

```python
# 数据库路径计算
DB_PATH = os.path.join(_project_root(), "database", "app.db")

def get_connection():
    """获取数据库连接，设置 Row factory 支持字典式访问"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化数据库表结构"""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                create_at TEXT NOT NULL DEFAULT(datetime('now'))
            )
        """)
```

**数据库表结构 `users`**:

| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | 自增主键 |
| `username` | TEXT | NOT NULL, UNIQUE | 用户名（唯一） |
| `password_hash` | TEXT | NOT NULL | PBKDF2 加密后的密码哈希 |
| `salt` | TEXT | NOT NULL | 随机盐值（hex 编码） |
| `create_at` | TEXT | NOT NULL, DEFAULT(datetime('now')) | 创建时间 |

#### 4.3.2 `user.py` - 用户模型

```python
def _hash_password(password: str, salt: bytes) -> str:
    """PBKDF2-HMAC-SHA256 密码加密，10万次迭代"""
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return dk.hex()

class UserRepository:
    @staticmethod
    def create_user(username: str, password: str) -> bool:
        """创建用户，返回 True/False（用户名冲突时返回 False）"""

    @staticmethod
    def get_user_by_username(username: str):
        """根据用户名查询用户信息（返回 sqlite3.Row 对象）"""

    @staticmethod
    def verify_user(username: str, password: str) -> bool:
        """验证用户名和密码"""
```

**密码加密流程**:
1. 生成 16 字节随机盐值: `secrets.token_bytes(16)`
2. PBKDF2-HMAC-SHA256 计算哈希: 100,000 次迭代
3. 存储 hex 编码的哈希值和盐值

**登录验证流程**:
1. 根据 username 查询数据库获取 `password_hash` 和 `salt`
2. 用存储的 salt 重新计算输入密码的 hash
3. 比对计算结果与存储的 hash 是否一致

### 4.4 视图层 (Templates)

#### 4.4.1 `base.html` - 基础模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="{{ static_url('css/base.css')}}">
    <script src="{{ static_url('js/base.js') }}"></script>
</head>
<body>
    <div class="container">
        {% block body %}{% end %}
    </div>
</body>
</html>
```

**模板语法说明**:
- `{{title}}` - 变量输出
- `{{ static_url('css/base.css') }}` - 静态文件 URL 生成（带版本缓存）
- `{% block body %}{% end %}` - 模板继承块，子模板可覆盖

#### 4.4.2 `login.html` - 登录页

```html
{% extends "base.html" %}
{% block body %}
<h3>登录</h3>
{% if error %}
<div class="error">{{error}}</div>
{% end %}
<form method="post" action="/auth/login">
    <input name="username">
    <input name="password">
    <button type="submit">登录admin</button>
    {% module xsrf_form_html() %}
</form>
{% end %}
```

**安全特性**:
- `{% module xsrf_form_html() %}` - 自动生成 XSRF Token 隐藏字段
- 错误信息条件渲染

#### 4.4.3 `index.html` - 后台首页

```html
{% extends "base.html" %}
{% block body %}
<h3>后台页面</h3>
<form action="/auth/logout" method="post">
    {% module xsrf_form_html() %}
    <button type="submit">退出</button>
</form>
<div>{{username}}</div>
{% end %}
```

#### 4.4.4 `register.html` - 注册页
- **状态**: 空文件（0 字节）
- **待开发**: 需要实现注册表单和对应的 Handler

### 4.5 测试脚本 `test.py`

```python
from app.models.db import init_db
from app.models.user import UserRepository

init_db()
# 测试用户创建
UserRepository.create_user("admin1", "123456")
UserRepository.create_user("admin2", "123456")
# 测试查询
UserRepository.get_user_by_username("admin")
# 测试验证（正确密码、错误密码、其他用户）
UserRepository.verify_user("admin", "123456")
UserRepository.verify_user("admin", "1234567")
UserRepository.verify_user("admin1", "123456")
```

---

## 五、登录功能验证记录

### 5.1 验证方式

项目存在 **两套登录实现**，验证情况如下：

#### 方式一：app.py 内联 LoginHandler（当前路由指向）
- **验证逻辑**: 硬编码 `username == "admin" and password == "123456"`
- **状态**: ✅ 可正常工作
- **缺点**: 不依赖数据库，无法扩展多用户，仅适合演示

#### 方式二：app/controllers/auth.py LoginHandler（推荐版本）
- **验证逻辑**: 调用 `UserRepository.verify_user()` 数据库验证
- **状态**: ✅ 代码完整，逻辑正确
- **前提**: 需要先在数据库中创建用户（通过 `test.py` 或注册功能）
- **优点**: 支持多用户、密码加密存储、可扩展

### 5.2 数据库用户数据

通过 `test.py` 可创建测试用户：
- `admin` / `123456`（需取消 test.py 第5行注释）
- `admin1` / `123456`
- `admin2` / `123456`

### 5.3 认证流程验证

```
1. 访问 / → @authenticated 检查 → 未登录 → 跳转 /auth/login
2. GET /auth/login → 渲染 login.html
3. POST /auth/login → 验证通过 → set_secure_cookie → redirect /
4. 访问 / → @authenticated 检查 → Cookie 有效 → 渲染 index.html
5. POST /auth/logout → clear_cookie → redirect /auth/login
```

---

## 六、安全机制分析

### 6.1 已实现的安全措施

| 安全机制 | 实现方式 | 状态 |
|----------|----------|------|
| XSRF/CSRF 防护 | `xsrf_cookies=True` + `{% module xsrf_form_html() %}` | ✅ 已启用 |
| Cookie 加密 | `set_secure_cookie()` + `cookie_secret` | ✅ 已启用 |
| 密码加密存储 | PBKDF2-HMAC-SHA256 (10万次迭代) + 随机盐值 | ✅ 已实现 |
| 登录态拦截 | `@tornado.web.authenticated` + `get_current_user()` | ✅ 已实现 |
| SQL 注入防护 | 参数化查询 `?` 占位符 | ✅ 已实现 |

### 6.2 需要改进的安全项

| 项目 | 当前状态 | 建议 |
|------|----------|------|
| `cookie_secret` | 硬编码明文 `"demo-cookie-secret-change-me"` | 生产环境使用环境变量或配置文件 |
| 登录失败限制 | 无 | 增加失败次数限制、验证码 |
| 密码强度校验 | 无 | 注册时增加密码复杂度要求 |
| Session 过期 | 无显式过期设置 | 设置 Cookie 过期时间 |
| HTTPS | 未配置 | 生产环境启用 HTTPS |

---

## 七、当前待完善/待开发项

### 7.1 框架层面

| 序号 | 任务 | 优先级 | 说明 |
|------|------|--------|------|
| 1 | **统一登录路由** | 🔴 高 | `app.py` 路由指向内联 LoginHandler，应改为指向 `app.controllers.auth.LoginHandler` |
| 2 | **补充静态文件** | 🟡 中 | `static/css/base.css` 和 `static/js/base.js` 文件缺失，模板中已引用 |
| 3 | **完善登出方法** | 🟡 中 | `app.py` 中 LogoutHandler 为 GET 方法，`auth.py` 中为 POST，应统一为 POST |
| 4 | **注册功能** | 🟡 中 | `register.html` 为空文件，需实现注册表单 + RegisterHandler |
| 5 | **错误页面** | 🟢 低 | 404/500 等自定义错误页面 |

### 7.2 AI 智能问答模块（待开发）

| 序号 | 任务 | 说明 |
|------|------|------|
| 1 | 数据库表设计 | 问答记录表、知识库表、会话表 |
| 2 | Model 层 | 问答记录 CRUD、知识库管理 |
| 3 | Controller 层 | 问答页面 Handler、API 接口 Handler |
| 4 | View 层 | 问答界面模板、历史记录展示 |
| 5 | AI 集成 | 接入大模型 API（如 OpenAI/文心/通义等） |

### 7.3 智能词表模块（待开发）

| 序号 | 任务 | 说明 |
|------|------|------|
| 1 | 数据库表设计 | 词表主表、词条表、分类表、用户词表关联 |
| 2 | Model 层 | 词表 CRUD、词条管理、分类管理 |
| 3 | Controller 层 | 词表列表页、词条编辑页、导入导出 |
| 4 | View 层 | 词表管理界面、词条编辑界面 |
| 5 | 智能功能 | AI 辅助生成词条、智能分类、词频分析 |

---

## 八、开发规范与约定

### 8.1 文件命名规范
- Python 文件: 小写下划线命名，如 `user.py`, `auth_handler.py`
- HTML 模板: 小写下划线，如 `login.html`, `word_list.html`
- 静态资源: 按功能分类存放

### 8.2 代码分层约定

```
Controller (Handler)  →  接收请求、参数校验、调用 Model、渲染/跳转
Model                 →  数据库操作、业务逻辑、数据验证
Template (View)       →  页面展示、数据渲染
```

### 8.3 路由命名约定
- 认证相关: `/auth/*` （如 `/auth/login`, `/auth/register`, `/auth/logout`）
- 业务模块: `/{module}/*` （如 `/qa/*`, `/word/*`）
- API 接口: `/api/{module}/*` （如 `/api/qa/ask`, `/api/word/import`）

### 8.4 Handler 命名约定
- 页面 Handler: `{功能}Handler` （如 `LoginHandler`, `WordListHandler`）
- API Handler: `Api{功能}Handler` （如 `ApiAskHandler`, `ApiWordImportHandler`）

---

## 九、启动与运行指南

### 9.1 环境准备
```bash
# 1. 激活虚拟环境（如未激活）
venv\Scripts\activate

# 2. 确认依赖已安装
pip list | findstr tornado
```

### 9.2 启动服务
```bash
python app.py
```

### 9.3 访问地址
- 首页: `http://localhost:10086/`
- 登录: `http://localhost:10086/auth/login`
- 私有页: `http://localhost:10086/private`

### 9.4 测试数据库
```bash
python test.py
```

---

## 十、后续开发任务排序建议

根据当前项目状态，建议按以下优先级推进开发：

### Phase 1: 框架完善（必须先完成）
1. ✅ 统一登录路由（将 `app.py` 路由指向 `auth.py` 的数据库验证版本）
2. ✅ 创建 `static/css/base.css` 和 `static/js/base.js` 基础文件
3. ✅ 实现注册功能（RegisterHandler + register.html 模板）
4. ✅ 统一登出方法为 POST

### Phase 2: AI 智能问答模块
5. 设计问答相关数据库表
6. 实现问答 Model 层
7. 实现问答 Controller 层
8. 实现问答 View 层
9. 接入 AI API

### Phase 3: 智能词表模块
10. 设计词表相关数据库表
11. 实现词表 Model 层
12. 实现词表 Controller 层
13. 实现词表 View 层
14. 实现智能辅助功能

### Phase 4: 系统优化
15. 安全加固（Cookie secret 配置化、登录限制等）
16. 前端 UI 美化
17. 性能优化
18. 日志系统

---

## 十一、关键文件清单

| 文件路径 | 作用 | 是否可修改 |
|----------|------|------------|
| `app.py` | 主入口、路由配置 | ⚠️ 需谨慎 |
| `app/controllers/base.py` | 基础 Handler、用户认证 | ✅ 可扩展 |
| `app/controllers/home.py` | 首页 Handler | ✅ 可扩展 |
| `app/controllers/auth.py` | 认证 Handler（推荐版本） | ✅ 可扩展 |
| `app/models/db.py` | 数据库连接、建表 | ⚠️ 改表结构需谨慎 |
| `app/models/user.py` | 用户模型、密码加密 | ✅ 可扩展 |
| `app/templates/base.html` | 基础模板 | ✅ 可扩展 |
| `app/templates/login.html` | 登录页模板 | ✅ 可扩展 |
| `app/templates/index.html` | 后台首页模板 | ✅ 可扩展 |
| `app/templates/register.html` | 注册页模板（空） | ✅ 待开发 |
| `database/app.db` | SQLite 数据库 | ⚠️ 勿直接编辑 |
| `test.py` | 测试脚本 | ✅ 可修改 |

---

> **文档生成时间**: 2026-05-24
> **学习状态**: ✅ 已完成项目架构学习，未修改任何代码文件
> **下一步**: 等待确认是否开始按需求完成开发任务
