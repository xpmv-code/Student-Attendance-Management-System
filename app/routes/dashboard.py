"""
数据概览路由模块
"""
from flask import Blueprint, render_template, jsonify
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_, or_

from app import db
from app.models.student import Student
from app.models.course import Course
from app.models.attendance import Attendance
from app.models.leave_record import LeaveRecord
from app.utils.week_helper import get_current_week, get_week_number

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    """数据概览仪表盘"""
    # 获取基础统计数据
    stats = get_basic_stats()
    
    # 获取图表数据
    chart_data = get_chart_data()
    
    # 获取最近活动
    recent_activities = get_recent_activities()
    
    return render_template(
        'dashboard/index.html',
        stats=stats,
        chart_data=chart_data,
        recent_activities=recent_activities
    )

@dashboard_bp.route('/api/stats')
def api_stats():
    """API接口：获取统计数据"""
    stats = get_basic_stats()
    return jsonify(stats)

@dashboard_bp.route('/api/charts')
def api_charts():
    """API接口：获取图表数据"""
    chart_data = get_chart_data()
    return jsonify(chart_data)

def get_basic_stats():
    """获取基础统计数据"""
    today = date.today()
    current_week = get_current_week()
    
    # 学生统计
    total_students = Student.query.count()
    
    # 课程统计
    total_courses = Course.query.count()
    
    # 今日考勤统计
    today_attendance = Attendance.query.filter_by(attendance_date=today).count()
    today_present = Attendance.query.filter_by(
        attendance_date=today,
        attendance_type='到课'
    ).count()
    today_absent = Attendance.query.filter_by(
        attendance_date=today,
        attendance_type='旷课'
    ).count()
    today_leave = Attendance.query.filter_by(
        attendance_date=today,
        attendance_type='请假'
    ).count()
    
    # 本周考勤统计
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    week_attendance = Attendance.query.filter(
        Attendance.attendance_date >= week_start,
        Attendance.attendance_date <= week_end
    ).count()
    
    # 请假统计
    active_leaves = LeaveRecord.query.filter(
        LeaveRecord.leave_start_date <= today,
        LeaveRecord.leave_end_date >= today
    ).count()
    
    total_leaves = LeaveRecord.query.count()
    
    # 本月请假统计
    month_start = date(today.year, today.month, 1)
    if today.month == 12:
        month_end = date(today.year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = date(today.year, today.month + 1, 1) - timedelta(days=1)
    
    month_leaves = LeaveRecord.query.filter(
        LeaveRecord.leave_start_date >= month_start,
        LeaveRecord.leave_start_date <= month_end
    ).count()
    
    # 计算到勤率
    attendance_rate = 0
    if total_students > 0 and today_attendance > 0:
        attendance_rate = round((today_present / (today_present + today_absent)) * 100, 1)
    
    return {
        'students': {
            'total': total_students,
            'label': '学生总数'
        },
        'courses': {
            'total': total_courses,
            'label': '课程总数'
        },
        'attendance': {
            'today_total': today_attendance,
            'today_present': today_present,
            'today_absent': today_absent,
            'today_leave': today_leave,
            'week_total': week_attendance,
            'rate': attendance_rate,
            'label': '今日考勤'
        },
        'leaves': {
            'active': active_leaves,
            'total': total_leaves,
            'month': month_leaves,
            'label': '请假记录'
        },
        'current_week': current_week,
        'today': today.strftime('%Y年%m月%d日')
    }

def get_chart_data():
    """获取图表数据"""
    today = date.today()
    
    # 最近7天考勤趋势
    attendance_trend = []
    for i in range(6, -1, -1):
        chart_date = today - timedelta(days=i)
        present = Attendance.query.filter_by(
            attendance_date=chart_date,
            attendance_type='到课'
        ).count()
        absent = Attendance.query.filter_by(
            attendance_date=chart_date,
            attendance_type='旷课'
        ).count()
        leave_count = Attendance.query.filter_by(
            attendance_date=chart_date,
            attendance_type='请假'
        ).count()
        
        attendance_trend.append({
            'date': chart_date.strftime('%m-%d'),
            'present': present,
            'absent': absent,
            'leave': leave_count
        })
    
    # 请假类型分布
    leave_type_stats = db.session.query(
        LeaveRecord.leave_type,
        func.count(LeaveRecord.leave_id).label('count')
    ).group_by(LeaveRecord.leave_type).all()
    
    leave_type_distribution = [
        {'type': stat.leave_type, 'count': stat.count}
        for stat in leave_type_stats
    ]
    
    # 本周每日课程数量
    week_courses = []
    weekday_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    
    for i in range(7):
        weekday = weekday_names[i]
        course_count = Course.query.filter(
            Course.course_time.like(f'{weekday}%')
        ).count()
        
        week_courses.append({
            'day': weekday,
            'count': course_count
        })
    
    # 学生政治面貌分布
    political_stats = db.session.query(
        Student.political_status,
        func.count(Student.student_id).label('count')
    ).group_by(Student.political_status).all()
    
    political_distribution = [
        {'status': stat.political_status, 'count': stat.count}
        for stat in political_stats
    ]
    
    return {
        'attendance_trend': attendance_trend,
        'leave_type_distribution': leave_type_distribution,
        'week_courses': week_courses,
        'political_distribution': political_distribution
    }

def get_recent_activities():
    """获取最近活动"""
    activities = []
    
    # 最近考勤记录
    recent_attendances = Attendance.query.order_by(
        Attendance.create_time.desc()
    ).limit(5).all()
    
    for attendance in recent_attendances:
        activities.append({
            'type': 'attendance',
            'time': attendance.create_time,
            'title': f"{attendance.student.student_name} 的考勤记录",
            'description': f"{attendance.course.course_name} - {attendance.attendance_type}",
            'icon': 'check-square-o',
            'color': 'green' if attendance.attendance_type == '到课' else 'red'
        })
    
    # 最近请假记录
    recent_leaves = LeaveRecord.query.order_by(
        LeaveRecord.create_time.desc()
    ).limit(5).all()
    
    for leave in recent_leaves:
        activities.append({
            'type': 'leave',
            'time': leave.create_time,
            'title': f"{leave.student.student_name} 的请假申请",
            'description': f"{leave.leave_type} - {leave.leave_days}天",
            'icon': 'calendar-o',
            'color': 'blue'
        })
    
    # 按时间排序
    activities.sort(key=lambda x: x['time'], reverse=True)
    
    return activities[:10]  # 返回最近10条

