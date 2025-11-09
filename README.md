# 学生考勤管理系统

一个基于Flask开发的学生考勤管理系统，提供学生管理、课程管理、考勤记录、请假管理和数据概览等功能。

## 📋 系统功能

### 🎯 核心模块

- **用户认证** - 用户登录、登出、会话管理、角色权限控制
- **学生管理** - 学生信息的增删改查、Excel导入导出、筛选搜索
- **课程管理** - 课程信息维护、ICS文件导入、课程详情查看、周次范围管理
- **考勤记录** - 每日考勤记录、历史查询、Excel导出、周次关联
- **请假管理** - 请假记录管理、统计分析、数据导出
- **数据概览** - 仪表盘展示、图表分析、实时统计

### ✨ 主要特性

- 🔐 **用户认证** - 基于Flask-Login的用户认证系统，支持角色权限管理
- 📊 **数据可视化** - Chart.js图表展示，直观的数据分析
- 📱 **响应式设计** - 支持桌面、平板、手机多端访问
- 📈 **统计分析** - 多维度数据统计和趋势分析
- 📋 **Excel导入导出** - 支持学生数据批量导入和考勤数据导出
- 🎨 **现代化UI** - 基于Tailwind CSS的美观界面
- 🔄 **实时更新** - 自动数据刷新和实时统计
- 📅 **周次管理** - 支持课程周次范围设置，自动判断上课周次
- 📆 **ICS导入** - 支持导入标准ICS格式课程表文件

## 🛠️ 技术栈

- **后端**: Flask 2.3.3 + SQLAlchemy + Flask-Login + PostgreSQL
- **前端**: HTML5 + Tailwind CSS + Chart.js + Font Awesome
- **数据库**: PostgreSQL
- **文件处理**: openpyxl (Excel), icalendar (ICS)
- **认证**: Flask-Login + Werkzeug (密码哈希)
- **Python版本**: 3.8+

## 📦 安装依赖

### 1. 克隆项目
```bash
git clone <repository-url>
cd class
```

### 2. 创建虚拟环境
```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

### 3. 安装依赖包
```bash
pip install -r requirements.txt
```

### 4. 依赖包说明
```
Flask==2.3.3              # Web框架
Flask-SQLAlchemy          # ORM数据库操作
flask-login               # 用户认证和会话管理
psycopg2-binary           # PostgreSQL数据库驱动
openpyxl==3.1.2           # Excel文件处理
icalendar                 # ICS文件解析
python-dotenv             # 环境变量管理
Werkzeug==2.3.7           # Web工具库（用于密码哈希）
flask_wtf                 # Flask表单处理
```

## 🗄️ 数据库配置

### 1. 安装PostgreSQL
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS (使用Homebrew)
brew install postgresql
brew services start postgresql

# Windows
# 下载并安装PostgreSQL官方安装包
```

### 2. 创建数据库
```bash
# 登录PostgreSQL
sudo -u postgres psql

# 创建数据库
CREATE DATABASE attendance_db;

# 创建用户（可选）
CREATE USER attendance_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE attendance_db TO attendance_user;

# 退出
\q
```

### 3. 配置数据库连接
编辑 `config.py` 文件：
```python
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql+psycopg2://username:password@localhost/attendance_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask密钥（生产环境请修改）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-internal-use'
    
    # 分页配置
    PER_PAGE = 10
    
    # Flask-Login配置
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # 记住登录状态7天
    SESSION_PROTECTION = 'strong'  # 启用会话保护
```

## 🚀 系统运行

### 1. 初始化数据库
```bash
# 创建数据库表
flask init-db

# 添加测试数据（可选）
flask add-test-data

# 重新创建user表（如果遇到字段长度问题）
flask recreate-user-table
```

**默认管理员账户**（初始化后自动创建）：
- 用户名: `admin`
- 密码: `admin123`

### 2. 启动系统
```bash
# 开发模式（推荐）
python run.py

# 或使用Flask命令
flask run --host=0.0.0.0 --port=5080

# 生产模式（使用gunicorn）
gunicorn -w 4 -b 0.0.0.0:5080 run:app
```

### 3. 访问系统
打开浏览器访问：`http://127.0.0.1:5080`

默认端口为 **5080**，可在 `run.py` 中修改。

## 📊 系统使用

### 🔐 用户认证
- **用户登录**: 使用管理员账户登录系统
- **会话管理**: 支持"记住我"功能，登录状态保持7天
- **角色权限**: 支持管理员、教师、普通用户等角色
- **安全登出**: 安全退出系统

### 🏠 首页（数据概览）
- 系统核心数据统计
- 图表分析和趋势展示
- 最近活动监控
- 快速操作入口

### 👥 学生管理
- **学生列表**: 查看所有学生信息，支持分页和筛选
- **添加学生**: 手动添加学生记录
- **Excel导入**: 批量导入学生数据
- **学生详情**: 查看学生详细信息和关联记录
- **数据导出**: 导出学生名单为Excel文件
- **编辑删除**: 编辑和删除学生信息

### 📚 课程管理
- **课程列表**: 查看所有课程，支持分页和搜索
- **ICS导入**: 导入标准ICS格式课程表文件
- **课程详情**: 查看课程详细信息和考勤情况
- **今日考勤**: 查看今日课程考勤情况
- **周次管理**: 设置课程上课周次范围（如：1-8,13,15,17）
- **周次判断**: 系统自动判断当前日期是否在课程上课周次内

### ✅ 考勤记录
- **考勤日历**: 按日期查看考勤记录
- **记录考勤**: 录入学生考勤状态（正常/迟到/早退/缺席/请假）
- **历史查询**: 查询历史考勤记录，支持多条件筛选
- **数据导出**: 导出考勤数据为Excel文件
- **周次关联**: 考勤记录自动关联课程周次信息
- **迟到记录**: 支持记录迟到分钟数

### 📝 请假管理
- **请假记录**: 查看所有请假记录，支持分页和筛选
- **添加请假**: 录入请假信息（病假/事假/其他）
- **统计分析**: 请假数据统计和图表分析
- **数据导出**: 导出请假记录为Excel文件
- **日期验证**: 自动验证请假日期范围合理性

## 📁 项目结构

```
Student-Attendance-Management-System/
├── app/                    # 应用主目录
│   ├── __init__.py        # Flask应用工厂
│   ├── models/            # 数据模型
│   │   ├── __init__.py    # 模型初始化
│   │   ├── user.py        # 用户模型
│   │   ├── student.py     # 学生模型
│   │   ├── course.py      # 课程模型
│   │   ├── attendance.py  # 考勤模型
│   │   └── leave_record.py # 请假模型
│   ├── routes/            # 路由模块
│   │   ├── __init__.py    # 路由初始化
│   │   ├── auth.py        # 用户认证路由
│   │   ├── student.py     # 学生管理路由
│   │   ├── course.py      # 课程管理路由
│   │   ├── attendance.py  # 考勤记录路由
│   │   ├── leave.py       # 请假管理路由
│   │   └── dashboard.py   # 数据概览路由
│   ├── templates/         # 模板文件
│   │   ├── base.html      # 基础模板
│   │   ├── index.html     # 首页模板
│   │   ├── auth/          # 认证模板
│   │   │   └── login.html # 登录页面
│   │   ├── student/       # 学生管理模板
│   │   ├── course/        # 课程管理模板
│   │   ├── attendance/    # 考勤记录模板
│   │   ├── leave/         # 请假管理模板
│   │   └── dashboard/     # 数据概览模板
│   └── utils/            # 工具模块
│       ├── __init__.py    # 工具初始化
│       ├── db.py          # 数据库工具
│       └── week_helper.py # 周次计算工具
├── Database/              # 数据库相关
│   ├── class.sql         # 数据库结构SQL
│   └── init_db.py        # 数据库初始化脚本
├── migrations/           # 数据库迁移文件
├── test/                # 测试文件
├── MD/                  # 项目文档
├── config.py            # 配置文件
├── run.py               # 应用入口
├── requirements.txt     # 依赖包列表
└── README.md           # 项目说明
```

## 🔧 配置说明

### 环境变量
```bash
# 设置环境变量
export SECRET_KEY="your-secret-key"
export DATABASE_URL="postgresql://user:pass@localhost/dbname"
export FLASK_ENV="development"  # 或 "production"
```

### 数据库配置
```python
# config.py
class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://user:pass@localhost/attendance_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10  # 分页大小
    REMEMBER_COOKIE_DURATION = timedelta(days=7)  # 记住登录状态7天
    SESSION_PROTECTION = 'strong'  # 启用会话保护
```

## 📋 数据导入

### Excel学生数据导入
1. 准备Excel文件，格式如下：
   - A1: 学号
   - B1: 姓名  
   - C1: 政治面貌
   - D1: 联系电话

2. 访问学生管理页面，点击"Excel导入"
3. 选择文件并上传
4. 系统自动解析并导入数据

### ICS课程表导入
1. 准备ICS格式的课程表文件
2. 访问课程管理页面，点击"导入课程表"
3. 选择ICS文件并上传
4. 系统自动解析课程信息并导入

## 📅 周次管理功能

系统支持课程周次范围设置，可以指定课程在哪些周次上课。

### 周次格式
- **连续周次**: `1-8` 表示第1周到第8周
- **单个周次**: `13` 表示第13周
- **混合格式**: `1-8,13,15,17` 表示第1-8周、第13周、第15周、第17周

### 周次计算
- 第一周起始日期：**2025年9月1日**
- 系统自动计算当前日期对应的周次
- 自动判断课程在当前周次是否上课
- 支持查看指定周次的日期范围

### 使用方法
1. 在课程管理中设置课程的 `week_range` 字段
2. 系统在考勤时会自动判断当前日期是否在课程上课周次内
3. 可以通过 `week_helper.py` 工具函数进行周次计算

## 🚨 常见问题

### Q1: 数据库连接失败
**A**: 检查PostgreSQL服务是否启动，数据库配置是否正确
```bash
# 检查PostgreSQL状态
sudo systemctl status postgresql  # Linux
brew services list | grep postgresql  # macOS
```

### Q2: 端口被占用
**A**: 更换端口或停止占用端口的进程
```bash
# 查看端口占用（默认端口5080）
lsof -i :5080
# 或
netstat -tulpn | grep :5080

# 修改端口：编辑 run.py 文件中的 port 参数
```

### Q3: 依赖包安装失败
**A**: 更新pip并重新安装
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q4: 图表不显示
**A**: 检查网络连接，Chart.js需要CDN访问
```html
<!-- 确保Chart.js CDN可访问 -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

### Q5: 用户认证失败
**A**: 检查数据库中的用户表是否正确创建
```bash
# 重新创建user表
flask recreate-user-table

# 或重新初始化数据库
flask init-db
```

### Q6: 周次计算不正确
**A**: 检查 `week_helper.py` 中的 `FIRST_WEEK_START` 日期设置
```python
# app/utils/week_helper.py
FIRST_WEEK_START = date(2025, 9, 1)  # 根据实际学期开始日期修改
```

## 🔒 安全说明

- **生产环境必须修改默认的SECRET_KEY**
- **修改默认管理员密码**，不要使用默认的 `admin123`
- 使用HTTPS协议保护数据传输
- 定期备份数据库
- 设置适当的数据库用户权限
- 使用环境变量存储敏感信息（如数据库密码）
- 启用Flask-Login的会话保护功能
- 定期更新依赖包，修复安全漏洞

## 📈 性能优化

- 使用Redis缓存热点数据
- 配置数据库连接池
- 启用Gzip压缩
- 使用CDN加速静态资源
- 优化数据库查询，使用索引
- 使用分页减少单次查询数据量
- 启用SQLAlchemy的查询缓存

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交Issue
- 发送邮件
- 项目讨论区

---

**学生考勤管理系统** - 让考勤管理更简单、更高效！ 🎉
