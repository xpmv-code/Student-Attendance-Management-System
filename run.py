import os
from app import create_app, db
from app.models import Student, Course, Attendance, LeaveRecord

# 创建应用实例
app = create_app()


# 注册命令：初始化数据库（在终端可用 `flask init-db` 执行）
@app.cli.command("init-db")
def init_db_command():
    """清空现有数据并创建新表"""
    db.drop_all()
    db.create_all()
    print("数据库已初始化，表结构创建完成！")

# 注册命令：重新创建user表（解决字段长度问题）
@app.cli.command("recreate-user-table")
def recreate_user_table():
    """重新创建user表，解决字段长度问题"""
    with app.app_context():
        try:
            # 尝试删除user表（如果存在）
            from sqlalchemy import text
            db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
            db.session.commit()
            print("已删除旧的user表")
        except Exception as e:
            print(f"删除表时出错（可能不存在）: {e}")

        try:
            # 重新创建所有表
            db.create_all()
            print("✓ 已重新创建user表，password_hash字段长度为256")
        except Exception as e:
            print(f"创建表失败: {e}")
            return

        # 添加默认管理员用户
        from app.models import User
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("默认管理员用户已创建 (用户名: admin, 密码: admin123)")


# 注册命令：添加测试数据（可选，方便测试）
@app.cli.command("add-test-data")
def add_test_data():
    """添加测试数据到数据库"""
    with app.app_context():
        # 添加默认管理员用户
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("默认管理员用户已创建 (用户名: admin, 密码: admin123)")

        # 添加测试学生
        s1 = Student(student_id="2023001", student_name="张三", political_status="共青团员", phone="13800138001")
        s2 = Student(student_id="2023002", student_name="李四", political_status="群众", phone="13900139001")
        db.session.add_all([s1, s2])

        # 添加测试课程
        c1 = Course(course_id="C001", course_name="高等数学", teacher_name="王老师",
                    course_time="周一3-4节", course_place="教学楼A201", semester="2023-2024学年上")
        c2 = Course(course_id="C002", course_name="Python编程", teacher_name="李老师",
                    course_time="周三5-6节", course_place="实验楼B302", semester="2023-2024学年上")
        db.session.add_all([c1, c2])

        db.session.commit()
        print("测试数据添加完成！")


# 确保在直接运行脚本时启动应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5080, debug=True)  # 0.0.0.0 允许内网其他设备访问