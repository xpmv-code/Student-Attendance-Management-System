from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import timedelta

# 初始化SQLAlchemy实例
db = SQLAlchemy()



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 绑定数据库实例到Flask应用
    db.init_app(app)
    
    # 注册全局模板函数
    app.jinja_env.globals.update(min=min, max=max, timedelta=timedelta, enumerate=enumerate)

    # 注册路由蓝图
    from app.routes.student import student_bp
    from app.routes.course import course_bp
    from app.routes.attendance import attendance_bp
    from app.routes.leave import leave_bp
    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(student_bp, url_prefix='/student')
    app.register_blueprint(course_bp, url_prefix='/course')
    app.register_blueprint(attendance_bp, url_prefix='/attendance')
    app.register_blueprint(leave_bp, url_prefix='/leave')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

    # 首页路由（重定向到数据概览）
    @app.route('/')
    def index():
        from flask import redirect, url_for
        return redirect(url_for('dashboard.index'))

    return app