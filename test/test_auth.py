#!/usr/bin/env python3
"""
简单的登录模块测试脚本
"""
import sys
import os
sys.path.append('..')

def test_imports():
    """测试导入"""
    try:
        from app.models.user import User
        from app import create_app
        print("✓ 导入成功")
        return True
    except Exception as e:
        print(f"✗ 导入失败: {e}")
        return False

def test_user_model():
    """测试User模型"""
    try:
        from app.models.user import User
        user = User(username='test', role='admin')
        user.set_password('password')
        assert user.check_password('password') == True
        assert user.check_password('wrong') == False
        assert user.is_admin() == True
        assert user.is_teacher() == False
        print("✓ User模型测试通过")
        return True
    except Exception as e:
        print(f"✗ User模型测试失败: {e}")
        return False

def test_app_creation():
    """测试应用创建"""
    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            from app import db
            print("✓ 应用创建成功")
            return True
    except Exception as e:
        print(f"✗ 应用创建失败: {e}")
        return False

if __name__ == '__main__':
    print("开始登录模块测试...")
    print("=" * 50)

    tests = [
        test_imports,
        test_user_model,
        test_app_creation
    ]

    passed = 0
    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"测试结果: {passed}/{len(tests)} 通过")

    if passed == len(tests):
        print("🎉 所有测试通过！登录模块设计完成。")
    else:
        print("❌ 部分测试失败，请检查代码。")
