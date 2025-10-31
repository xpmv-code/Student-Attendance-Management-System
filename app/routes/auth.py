"""
登录认证路由模块
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    # 如果用户已登录，重定向到首页
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        if not username or not password:
            flash('请输入用户名和密码', 'error')
            return redirect(url_for('auth.login'))

        # 查找用户
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password) and user.is_active:
            # 登录成功
            login_user(user, remember=remember)
            flash(f'欢迎回来，{user.username}！', 'success')

            # 重定向到之前的页面或首页
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard.index'))
        else:
            flash('用户名或密码错误，或账户已被禁用', 'error')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """用户个人资料"""
    return render_template('auth/profile.html')
