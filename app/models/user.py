from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'  # 对应数据库表名

    # 字段定义
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户ID（主键）')
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password_hash = db.Column(db.String(256), nullable=False, comment='密码哈希')
    role = db.Column(db.String(20), default='user', comment='用户角色（admin/teacher/user）')
    is_active = db.Column(db.Boolean, default=True, comment='是否激活')
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='创建时间')

    def __repr__(self):
        return f'<User {self.username}: {self.role}>'

    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        """检查是否为管理员"""
        return self.role == 'admin'

    def is_teacher(self):
        """检查是否为教师"""
        return self.role == 'teacher'
