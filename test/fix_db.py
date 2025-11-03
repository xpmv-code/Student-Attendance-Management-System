#!/usr/bin/env python3
"""
修复数据库问题的脚本
"""
import sys
import os
sys.path.append('..')

def fix_database():
    """修复数据库问题"""
    try:
        from app import create_app, db
        from sqlalchemy import text

        app = create_app()

        with app.app_context():
            print("正在修复数据库...")

            # 删除可能存在的user表
            try:
                db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))
                db.session.commit()
                print("✓ 已清理旧的user表")
            except Exception as e:
                print(f"清理表时出现警告（可能不存在）: {e}")

            # 重新创建所有表
            db.create_all()
            print("✓ 已重新创建所有表")

            # 添加默认管理员用户
            from app.models import User
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ 默认管理员用户已创建")
            print("  用户名: admin")
            print("  密码: admin123")

            print("\n🎉 数据库修复完成！")

    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所有依赖包: pip install -r requirements.txt")
    except Exception as e:
        print(f"修复过程中出现错误: {e}")

if __name__ == '__main__':
    fix_database()
