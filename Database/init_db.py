from app import create_app, db
from app.models import Student, Course, Attendance, LeaveRecord

# 创建Flask应用实例
app = create_app()

def init_database():
    # 在应用上下文内操作数据库
    with app.app_context():
        # 删除所有现有表（谨慎使用！生产环境避免此操作）
        db.drop_all()
        # 创建所有模型对应的表
        db.create_all()
        print("数据库表结构创建成功！")

if __name__ == '__main__':
    init_database()