# 学生考勤管理系统

一个基于Flask开发的学生考勤管理系统，提供学生管理、课程管理、考勤记录、请假管理和数据概览等功能。

## 📋 系统功能

### 🎯 核心模块

- **学生管理** - 学生信息的增删改查、Excel导入导出、筛选搜索
- **课程管理** - 课程信息维护、ICS文件导入、课程详情查看
- **考勤记录** - 每日考勤记录、历史查询、Excel导出
- **请假管理** - 请假记录管理、统计分析、数据导出
- **数据概览** - 仪表盘展示、图表分析、实时统计

### ✨ 主要特性

- 📊 **数据可视化** - Chart.js图表展示，直观的数据分析
- 📱 **响应式设计** - 支持桌面、平板、手机多端访问
- 📈 **统计分析** - 多维度数据统计和趋势分析
- 📋 **Excel导入导出** - 支持学生数据批量导入和考勤数据导出
- 🎨 **现代化UI** - 基于Tailwind CSS的美观界面
- 🔄 **实时更新** - 自动数据刷新和实时统计

## 🛠️ 技术栈

- **后端**: Flask + SQLAlchemy + PostgreSQL
- **前端**: HTML5 + Tailwind CSS + Chart.js
- **数据库**: PostgreSQL
- **文件处理**: openpyxl (Excel), icalendar (ICS)
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
Flask==3.0.0              # Web框架
Flask-SQLAlchemy==3.1.1   # ORM数据库操作
psycopg2-binary==2.9.9    # PostgreSQL数据库驱动
openpyxl==3.1.2           # Excel文件处理
icalendar==5.0.11         # ICS文件解析
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

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/student_attendance'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 15
```

## 🚀 系统运行

### 1. 初始化数据库
```bash
# 创建数据库表
python run.py init-db

# 添加测试数据（可选）
python run.py add-test-data
```

### 2. 启动系统
```bash
# 开发模式
python run.py

# 或直接运行
flask run

# 生产模式（使用gunicorn）
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### 3. 访问系统
打开浏览器访问：`http://127.0.0.1:5000`

## 📊 系统使用

### 🏠 首页（数据概览）
- 系统核心数据统计
- 图表分析和趋势展示
- 最近活动监控
- 快速操作入口

### 👥 学生管理
- **学生列表**: 查看所有学生信息
- **添加学生**: 手动添加学生记录
- **Excel导入**: 批量导入学生数据
- **学生详情**: 查看学生详细信息
- **数据导出**: 导出学生名单

### 📚 课程管理
- **课程列表**: 查看所有课程
- **ICS导入**: 导入课程表文件
- **课程详情**: 查看课程详细信息
- **今日考勤**: 查看今日课程考勤情况

### ✅ 考勤记录
- **考勤日历**: 按日期查看考勤
- **记录考勤**: 录入学生考勤状态
- **历史查询**: 查询历史考勤记录
- **数据导出**: 导出考勤数据

### 📝 请假管理
- **请假记录**: 查看所有请假记录
- **添加请假**: 录入请假信息
- **统计分析**: 请假数据统计
- **数据导出**: 导出请假记录

## 📁 项目结构

```
class/
├── app/                    # 应用主目录
│   ├── __init__.py        # Flask应用工厂
│   ├── models/            # 数据模型
│   │   ├── student.py     # 学生模型
│   │   ├── course.py      # 课程模型
│   │   ├── attendance.py  # 考勤模型
│   │   └── leave_record.py # 请假模型
│   ├── routes/            # 路由模块
│   │   ├── student.py     # 学生管理路由
│   │   ├── course.py      # 课程管理路由
│   │   ├── attendance.py   # 考勤记录路由
│   │   ├── leave.py       # 请假管理路由
│   │   └── dashboard.py   # 数据概览路由
│   ├── templates/         # 模板文件
│   │   ├── base.html      # 基础模板
│   │   ├── index.html     # 首页模板
│   │   ├── student/       # 学生管理模板
│   │   ├── course/        # 课程管理模板
│   │   ├── attendance/    # 考勤记录模板
│   │   ├── leave/         # 请假管理模板
│   │   └── dashboard/     # 数据概览模板
│   └── utils/            # 工具模块
│       └── week_helper.py # 周次计算工具
├── config.py             # 配置文件
├── run.py                # 应用入口
├── requirements.txt      # 依赖包列表
├── class.sql            # 数据库结构
└── README.md            # 项目说明
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
    SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 15  # 分页大小
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
# 查看端口占用
lsof -i :5000
# 或
netstat -tulpn | grep :5000
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

## 🔒 安全说明

- 生产环境请修改默认的SECRET_KEY
- 使用HTTPS协议保护数据传输
- 定期备份数据库
- 设置适当的数据库用户权限

## 📈 性能优化

- 使用Redis缓存热点数据
- 配置数据库连接池
- 启用Gzip压缩
- 使用CDN加速静态资源

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
