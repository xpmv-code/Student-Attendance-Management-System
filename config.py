import os
from dotenv import load_dotenv

# 加载环境变量（如需）
load_dotenv()


class Config:
    # 数据库配置（根据实际数据库类型调整，这里以PostgreSQL为例）
    # 格式：数据库类型+驱动://用户名:密码@主机:端口/数据库名
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'postgresql://postgres:opoo1234@localhost/attendance_db'  # 密码和数据库名根据实际修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 关闭SQLAlchemy的修改跟踪，提升性能

    # Flask密钥（用于会话管理等，内网使用可简单设置）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-for-internal-use'

    # 分页配置（每页显示记录数）
    PER_PAGE = 10