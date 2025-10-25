"""
周次计算辅助函数
"""
from datetime import date, timedelta


# 第一周的开始日期：2025年9月1日
FIRST_WEEK_START = date(2025, 9, 1)


def get_week_number(target_date):
    """
    计算指定日期是第几周
    
    Args:
        target_date: 目标日期（date对象）
        
    Returns:
        int: 周次（1-20），如果在学期范围外返回None
    """
    if isinstance(target_date, str):
        from datetime import datetime
        target_date = datetime.strptime(target_date, '%Y-%m-%d').date()
    
    # 计算距离第一周开始的天数
    days_diff = (target_date - FIRST_WEEK_START).days
    
    # 如果在学期开始之前，返回None
    if days_diff < 0:
        return None
    
    # 计算周次（向下取整+1）
    week_number = (days_diff // 7) + 1
    
    # 一般学期最多20周
    if week_number > 20:
        return None
    
    return week_number


def get_week_date_range(week_number):
    """
    获取指定周次的日期范围（周一到周日）
    
    Args:
        week_number: 周次（1-20）
        
    Returns:
        tuple: (start_date, end_date)
    """
    # 计算该周周一的日期
    week_start = FIRST_WEEK_START + timedelta(weeks=week_number - 1)
    
    # 如果第一周的开始不是周一，需要调整到周一
    # FIRST_WEEK_START是2025-09-01（周一），所以不需要调整
    
    # 计算周日
    week_end = week_start + timedelta(days=6)
    
    return week_start, week_end


def get_current_week():
    """
    获取当前日期所在的周次
    
    Returns:
        int: 当前周次，如果在学期范围外返回None
    """
    return get_week_number(date.today())


def is_in_week_range(week_number, week_range_str):
    """
    判断指定周次是否在周次范围内
    
    Args:
        week_number: 周次（1-20）
        week_range_str: 周次范围字符串（如：1-8,13,15,17 或 9-16）
        
    Returns:
        bool: True表示在范围内，False表示不在范围内
    """
    if not week_range_str:
        return True  # 如果没有设置范围，默认所有周都上课
    
    # 解析周次范围
    week_set = set()
    parts = week_range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            # 范围格式：1-8
            try:
                start, end = part.split('-')
                week_set.update(range(int(start), int(end) + 1))
            except ValueError:
                continue
        else:
            # 单个周次：13
            try:
                week_set.add(int(part))
            except ValueError:
                continue
    
    return week_number in week_set


def format_week_range(week_range_str):
    """
    格式化周次范围显示
    
    Args:
        week_range_str: 周次范围字符串
        
    Returns:
        str: 格式化后的显示文本
    """
    if not week_range_str:
        return "全学期"
    
    # 解析并格式化
    parts = []
    for part in week_range_str.split(','):
        part = part.strip()
        if '-' in part:
            parts.append(f"第{part}周")
        else:
            parts.append(f"第{part}周")
    
    return "、".join(parts)

