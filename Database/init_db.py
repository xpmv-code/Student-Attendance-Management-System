from app import create_app, db
from app.models import Student, Course, Attendance, LeaveRecord, User

# 创建Flask应用实例
app = create_app()

def init_database():
    # 在应用上下文内操作数据库
    with app.app_context():
        # # 删除所有现有表（谨慎使用！生产环境避免此操作）
        # db.drop_all()
        # # 创建所有模型对应的表
        # db.create_all()

        # 添加默认管理员用户
        admin_user = User(username='xpmv123', role='admin')
        admin_user.set_password('XW8023ljjnn..')
        db.session.add(admin_user)
        db.session.commit()

        print("数据库表结构创建成功！")
        print("默认管理员用户已创建 (用户名: admin, 密码: admin123)")

if __name__ == '__main__':
    init_database()