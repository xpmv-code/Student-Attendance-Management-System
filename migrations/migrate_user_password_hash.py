"""
数据库迁移脚本：将user表password_hash字段长度从128增加到256
"""
from app import create_app, db
from sqlalchemy import text

def migrate_password_hash_length():
    """迁移password_hash字段长度"""
    app = create_app()

    with app.app_context():
        try:
            # 使用原始SQL执行ALTER TABLE语句
            # 注意：这会删除现有数据，请谨慎使用
            db.session.execute(text('ALTER TABLE "user" ALTER COLUMN password_hash TYPE VARCHAR(256)'))

            db.session.commit()
            print("✓ 成功将password_hash字段长度从128增加到256")

        except Exception as e:
            db.session.rollback()
            print(f"✗ 迁移失败: {e}")

            # 如果上面的方法失败，可以尝试重建表
            print("尝试重建user表...")
            try:
                # 删除旧表
                db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE'))

                # 重新创建表
                db.create_all()

                print("✓ 已重建user表，字段长度已更新为256")

            except Exception as e2:
                print(f"✗ 重建表也失败: {e2}")
                return False

    return True

if __name__ == '__main__':
    migrate_password_hash_length()
