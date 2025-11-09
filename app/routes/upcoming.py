# app/routes/upcoming.py
from flask import Blueprint, render_template, request
from flask_login import login_required
from datetime import datetime, date, time, timedelta
import re

from app import db
from app.models import Course
from app.utils.week_helper import FIRST_WEEK_START, get_week_number, get_week_date_range

bp = Blueprint('upcoming', __name__, url_prefix='')

# --- 节次时间定义 (保持不变) ---
# --- 节次时间定义 (更新后) ---
DEFAULT_PERIOD_TIMES = {
    1: (time(8, 0),  time(8, 45)),
    2: (time(8, 55), time(9, 40)),
    3: (time(10, 0), time(10, 45)),
    4: (time(10, 55), time(11, 40)),
    5: (time(12, 20), time(13, 5)),   # ✅ 新增：中午第一节
    6: (time(13, 10), time(13, 50)),  # ✅ 新增：中午第二节
    7: (time(14, 0),  time(14, 45)),
    8: (time(14, 55), time(15, 40)),
    9: (time(16, 0),  time(16, 45)),
    10: (time(16, 55), time(17, 40)),
    11: (time(19, 0), time(19, 45)),
    12: (time(19, 55), time(20, 40)),
}


# --- 星期映射 (保持不变) ---
CN_WEEKDAY_MAP = {
    '一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6, '天': 6
}
DAY_HEADERS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]

# --- 【新】定义课表的 "行" ---
# 这定义了表格的行。我们假设课表按2节合并显示。
# 格式: (slot_index, label, start_period, end_period)
PERIOD_ROW_SLOTS = [
    (0, "1-2节", 1, 2),
    (1, "3-4节", 3, 4),
    (2, "5-6节", 5, 6),   # ✅ 中午新增时段，12:20~13:50
    (3, "7-8节", 7, 8),
    (4, "9-10节", 9, 10), # ✅ 可选：下午或傍晚
]


# --- 辅助函数 ---
def parse_course_time(course_time_str):
    """
    解析课程时间字符串，支持多种格式：
    - "周一3-4节"
    - "周一 3-4节"
    - "周一3,4节"
    - "周一 08:00-09:40" (需要转换为节次)
    """
    if not course_time_str:
        return []
    
    results = []
    s = course_time_str.strip()
    
    # 支持多种分隔符分割多个时间段
    parts = re.split(r'[;,/]|，', s)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # 优先匹配模式2: 周X + 时间格式 (如: 周一 08:00-09:40, 周二 08:20-09:50)
        # 这个格式更精确，应该优先匹配
        pattern2 = re.compile(r'周([一二三四五六日天])\s+(\d{1,2}):(\d{2})\s*-\s*(\d{1,2}):(\d{2})')
        m2 = pattern2.search(part)
        if m2:
            cn_week = m2.group(1)
            start_h = int(m2.group(2))
            start_m = int(m2.group(3))
            end_h = int(m2.group(4))
            end_m = int(m2.group(5))
            
            weekday = CN_WEEKDAY_MAP.get(cn_week)
            if weekday is not None:
                # 将时间转换为节次
                start_period = time_to_period(start_h, start_m)
                end_period = time_to_period(end_h, end_m)
                
                # 如果开始节次和结束节次都找到了，添加到结果中
                if start_period and end_period:
                    # 确保开始节次 <= 结束节次
                    if start_period <= end_period:
                        results.append((weekday, start_period, end_period))
                    else:
                        # 如果开始节次 > 结束节次，可能是时间解析错误，使用开始节次作为结束节次
                        results.append((weekday, start_period, start_period))
                elif start_period:
                    # 如果只找到了开始节次，使用开始节次作为结束节次
                    results.append((weekday, start_period, start_period))
                elif end_period:
                    # 如果只找到了结束节次，使用结束节次作为开始节次
                    results.append((weekday, end_period, end_period))
            continue
        
        # 模式1: 周X + 节次格式 (如: 周一3-4节, 周一 3-4节, 周一3,4节, 周一第3-4节)
        # 注意：这个模式不应该匹配包含冒号的时间格式
        # 修改正则表达式，确保不匹配时间格式（不包含冒号）
        if ':' not in part:  # 如果包含冒号，说明是时间格式，跳过模式1
            pattern1 = re.compile(r'周([一二三四五六日天])\s*(?:第)?\s*([0-9]{1,2}(?:-[0-9]{1,2})?|[0-9]{1,2}\s*[,-]\s*[0-9]{1,2})\s*(?:节|节课)?')
            m1 = pattern1.search(part)
            if m1:
                cn_week = m1.group(1)
                period_part = m1.group(2).replace(' ', '').replace('，', ',')
                weekday = CN_WEEKDAY_MAP.get(cn_week)
                if weekday is not None:
                    try:
                        # 处理 "3-4" 或 "3,4" 格式
                        if '-' in period_part:
                            period_parts = period_part.split('-')
                            start_p = int(period_parts[0])
                            end_p = int(period_parts[1])
                        elif ',' in period_part:
                            periods = [int(p.strip()) for p in period_part.split(',') if p.strip().isdigit()]
                            if periods:
                                start_p = min(periods)
                                end_p = max(periods)
                            else:
                                continue
                        else:
                            start_p = end_p = int(period_part)
                        
                        # 验证节次范围（1-12）
                        if 1 <= start_p <= 12 and 1 <= end_p <= 12 and start_p <= end_p:
                            results.append((weekday, start_p, end_p))
                    except (ValueError, IndexError):
                        continue
    
    return results


def time_to_period(hour, minute):
    """
    将时间转换为节次
    返回节次数，如果不在任何节次范围内返回None
    
    改进逻辑：
    1. 如果时间在节次的时间范围内，直接返回该节次
    2. 如果时间在节次开始时间前后15分钟内，返回该节次
    3. 如果时间超过节次结束时间，但在下一个节次开始之前（间隔内），返回当前节次
    4. 对于边界情况，优先匹配时间上最接近的节次
    """
    try:
        t = time(hour, minute)
    except ValueError:
        return None
    
    t_seconds = t.hour * 3600 + t.minute * 60
    
    # 按节次顺序检查（1-12）
    sorted_periods = sorted(DEFAULT_PERIOD_TIMES.items())
    
    for i, (period, (start_time, end_time)) in enumerate(sorted_periods):
        start_seconds = start_time.hour * 3600 + start_time.minute * 60
        end_seconds = end_time.hour * 3600 + end_time.minute * 60
        
        # 情况1: 时间在节次的时间范围内
        if start_seconds <= t_seconds <= end_seconds:
            return period
        
        # 情况2: 时间在节次开始时间前后15分钟内（允许提前或延后）
        if abs(t_seconds - start_seconds) <= 900:  # 15分钟 = 900秒
            return period
        
        # 情况3: 时间超过节次结束时间，但在下一个节次开始之前
        # 计算到下一个节次开始的时间
        if i < len(sorted_periods) - 1:
            next_period, (next_start_time, _) = sorted_periods[i + 1]
            next_start_seconds = next_start_time.hour * 3600 + next_start_time.minute * 60
            
            # 如果时间在结束时间和下一个节次开始之间
            if end_seconds < t_seconds < next_start_seconds:
                # 计算距离结束时间和下一个开始时间的距离
                diff_to_end = t_seconds - end_seconds
                diff_to_next_start = next_start_seconds - t_seconds
                
                # 如果更接近当前节次的结束时间（在间隔的前半段），返回当前节次
                # 否则返回下一个节次
                if diff_to_end <= diff_to_next_start:
                    return period
                else:
                    return next_period
        else:
            # 最后一个节次，如果时间超过结束时间但在合理范围内（20分钟内）
            if t_seconds > end_seconds and (t_seconds - end_seconds) <= 1200:
                return period
    
    # 如果没有精确匹配，找最接近的节次（按开始时间）
    best_match = None
    min_diff = float('inf')
    
    for period, (start_time, _) in sorted_periods:
        start_seconds = start_time.hour * 3600 + start_time.minute * 60
        diff = abs(t_seconds - start_seconds)
        if diff < min_diff:
            min_diff = diff
            best_match = period
    
    # 只有在1小时内才返回，否则返回None
    if min_diff <= 3600:
        return best_match
    
    return None


def get_week_label_for_date(d: date):
    """
    获取指定日期所在的周次和该周的日期范围（周一到周日）
    """
    if not isinstance(d, date):
        d = d.date()
    
    # 使用week_helper中的函数计算周次
    week_no = get_week_number(d)
    if week_no is None or week_no <= 0:
        # 如果不在学期范围内，使用get_week_date_range计算
        # 假设为第1周
        week_no = 1
        week_start, week_end = get_week_date_range(week_no)
        return week_no, week_start, week_end
    
    # 使用week_helper中的函数获取周次日期范围
    week_start, week_end = get_week_date_range(week_no)
    
    return week_no, week_start, week_end


def get_color_hsl(s):
    """根据字符串 (如 course_id) 生成 HSL 颜色"""
    h = 0
    for i in range(len(s)):
        h = (h * 31 + ord(s[i])) % 360
    # 我们使用高饱和度(S)和高亮度(L)来得到柔和的彩色背景
    return f"hsl({h}, 85%, 85%)"


@bp.route('/upcoming-week')
@login_required
def upcoming_week_page():
    """
    渲染"周课表网格"页面。
    构建一个二维网格数据 (week_grid) 和行/列标题。
    """
    # 获取查询参数
    week_param = request.args.get('week', type=int)
    semester_param = request.args.get('semester', type=str, default='')
    
    # 确定要显示的周次
    if week_param and week_param > 0:
        # 使用指定的周次
        week_no = week_param
        week_start, week_end = get_week_date_range(week_no)
    else:
        # 使用当前周次
        today = date.today()
        week_no, week_start, week_end = get_week_label_for_date(today)
        if week_no == 0:
            week_no = 1
            week_start, week_end = get_week_date_range(week_no)
    
    week_label = f"第{week_no}周 ({week_start.strftime('%m/%d')} ~ {week_end.strftime('%m/%d')})"
    
    # 获取学期信息
    all_courses = Course.query.all()
    if all_courses:
        # 从课程中获取学期信息
        semesters = db.session.query(Course.semester).distinct().filter(
            Course.semester.isnot(None)
        ).order_by(Course.semester.desc()).all()
        semesters = [s[0] for s in semesters]
        if semester_param:
            current_semester = semester_param
        else:
            current_semester = semesters[0] if semesters else ''
    else:
        semesters = []
        current_semester = ''
    
    semester_title = current_semester or "当前学期"

    # 2. 构建行标题 (row_slots)
    row_slots = []
    for (idx, label, start_p, end_p) in PERIOD_ROW_SLOTS:
        try:
            start_time = DEFAULT_PERIOD_TIMES[start_p][0].strftime('%H:%M')
            end_time = DEFAULT_PERIOD_TIMES[end_p][1].strftime('%H:%M')
            time_display = f"{start_time}~{end_time}"
        except KeyError:
            time_display = "时间未定"

        row_slots.append({
            "slot_index": idx,
            "label": label,
            "time": time_display
        })

    # 3. 构建网格数据 (week_grid)
    week_grid = {}  # key: "day-slot", value: list of courses

    # 获取当前周次需要显示的所有课程
    query = Course.query
    if current_semester:
        query = query.filter(Course.semester == current_semester)
    all_courses = query.all()

    current_week_courses = []
    for c in all_courses:
        # 检查课程是否在当前周次上课
        if week_no > 0 and c.is_teaching_week(week_no):
            current_week_courses.append(c)

    # 填充网格
    for c in current_week_courses:
        parsed_times = parse_course_time(c.course_time)
        
        if not parsed_times:
            # 如果无法解析课程时间，记录日志（仅在开发环境）
            # 注意：这可能是时间格式不符合预期，需要检查数据库中的course_time格式
            continue

        for (wday, start_p, end_p) in parsed_times:
            # 找到这个时间跨越了哪些 "行"
            # 一个课程可能跨越多个时间段（如 3-6节 跨越 3-4节 和 5-6节）
            matched_slots = []
            for (slot_idx, label, slot_start, slot_end) in PERIOD_ROW_SLOTS:
                # 检查课程时间与表格行是否有交集
                # 如果课程的开始节次 <= 时间段的结束节次 且 课程的结束节次 >= 时间段的开始节次
                if start_p <= slot_end and end_p >= slot_start:
                    matched_slots.append((slot_idx, slot_start, slot_end))
            
            # 如果课程跨越多个时间段，在第一个匹配的时间段显示
            # 并记录课程跨越的节次数，用于调整显示高度
            if matched_slots:
                # 按slot_idx排序，选择第一个
                matched_slots.sort(key=lambda x: x[0])
                slot_idx, slot_start, slot_end = matched_slots[0]
                
                # 计算课程实际跨越的时间段数
                span_slots = len(matched_slots)
                
                key = f"{wday}-{slot_idx}"  # e.g., "0-1" (周一, 3-4节)

                if key not in week_grid:
                    week_grid[key] = []

                # 格式化周次范围显示
                week_range_display = c.week_range if c.week_range else "全学期"

                course_info = {
                    "name": c.course_name,
                    "teacher": c.teacher_name,
                    "place": c.course_place,
                    "week_range": week_range_display,
                    "raw_time": c.course_time,
                    "color_bg": get_color_hsl(c.course_id),
                    "course_id": c.course_id,
                    "span_slots": span_slots,  # 跨越的时间段数
                    "start_period": start_p,
                    "end_period": end_p
                }
                
                # 检查是否已存在相同的课程（避免重复添加）
                existing = False
                for existing_course in week_grid[key]:
                    if existing_course['course_id'] == c.course_id and existing_course['raw_time'] == c.course_time:
                        existing = True
                        break
                
                if not existing:
                    week_grid[key].append(course_info)

    # 4. 渲染模板
    return render_template(
        'calendar/upcoming_week.html',
        semester_title=semester_title,
        week_label=week_label,
        week_no=week_no,
        day_headers=DAY_HEADERS,
        row_slots=row_slots,
        week_grid=week_grid,
        semesters=semesters,
        current_semester=current_semester
    )