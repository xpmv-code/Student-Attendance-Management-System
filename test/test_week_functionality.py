#!/usr/bin/env python
"""
课程周次功能测试脚本

用法：
python test_week_functionality.py
"""

from datetime import date
from app.utils.week_helper import (
    get_week_number, 
    get_week_date_range, 
    get_current_week,
    is_in_week_range,
    format_week_range,
    FIRST_WEEK_START
)


def test_week_number_calculation():
    """测试周次计算"""
    print("=" * 60)
    print("测试1：周次计算")
    print("=" * 60)
    
    test_cases = [
        (date(2025, 9, 1), 1, "第一周周一"),
        (date(2025, 9, 7), 1, "第一周周日"),
        (date(2025, 9, 8), 2, "第二周周一"),
        (date(2025, 9, 14), 2, "第二周周日"),
        (date(2025, 10, 27), 9, "第九周周一"),
        (date(2025, 12, 29), 17, "第十七周周一"),
        (date(2025, 8, 31), None, "学期开始前"),
    ]
    
    for test_date, expected, description in test_cases:
        result = get_week_number(test_date)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}: {test_date} → 第{result}周 (期望: {expected})")
    
    print()


def test_week_date_range():
    """测试周次日期范围"""
    print("=" * 60)
    print("测试2：周次日期范围")
    print("=" * 60)
    
    test_cases = [
        (1, (date(2025, 9, 1), date(2025, 9, 7)), "第1周"),
        (2, (date(2025, 9, 8), date(2025, 9, 14)), "第2周"),
        (9, (date(2025, 10, 27), date(2025, 11, 2)), "第9周"),
    ]
    
    for week, expected, description in test_cases:
        result = get_week_date_range(week)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}: {result[0]} 至 {result[1]} (期望: {expected[0]} 至 {expected[1]})")
    
    print()


def test_is_in_week_range():
    """测试周次范围判断"""
    print("=" * 60)
    print("测试3：周次范围判断")
    print("=" * 60)
    
    test_cases = [
        # (周次, 范围字符串, 期望结果, 描述)
        (1, "1-8", True, "第1周在1-8范围内"),
        (5, "1-8", True, "第5周在1-8范围内"),
        (8, "1-8", True, "第8周在1-8范围内"),
        (9, "1-8", False, "第9周不在1-8范围内"),
        (13, "1-8,13,15,17", True, "第13周在1-8,13,15,17范围内"),
        (14, "1-8,13,15,17", False, "第14周不在1-8,13,15,17范围内"),
        (15, "1-8,13,15,17", True, "第15周在1-8,13,15,17范围内"),
        (10, "9-16", True, "第10周在9-16范围内"),
        (1, "9-16", False, "第1周不在9-16范围内"),
        (5, None, True, "没有设置范围，默认所有周都上课"),
        (5, "", True, "空范围，默认所有周都上课"),
    ]
    
    for week, range_str, expected, description in test_cases:
        result = is_in_week_range(week, range_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}: week={week}, range='{range_str}' → {result}")
    
    print()


def test_format_week_range():
    """测试周次范围格式化"""
    print("=" * 60)
    print("测试4：周次范围格式化")
    print("=" * 60)
    
    test_cases = [
        ("1-8", "第1-8周", "连续范围"),
        ("9-16", "第9-16周", "连续范围"),
        ("1-8,13,15,17", "第1-8周、第13周、第15周、第17周", "组合范围"),
        ("1,3,5,7,9", "第1周、第3周、第5周、第7周、第9周", "不连续周次"),
        (None, "全学期", "未设置范围"),
        ("", "全学期", "空范围"),
    ]
    
    for range_str, expected, description in test_cases:
        result = format_week_range(range_str)
        status = "✅" if result == expected else "❌"
        print(f"{status} {description}: '{range_str}' → '{result}' (期望: '{expected}')")
    
    print()


def test_course_scenario():
    """测试实际课程场景"""
    print("=" * 60)
    print("测试5：实际课程场景")
    print("=" * 60)
    
    print(f"学期第一周开始日期: {FIRST_WEEK_START}")
    print(f"当前周次: 第{get_current_week()}周")
    print()
    
    # 模拟课程
    courses = [
        {"name": "高等数学", "time": "周一 08:00-09:40", "week_range": "1-16"},
        {"name": "大学英语", "time": "周一 10:00-11:40", "week_range": "1-8"},
        {"name": "专业选修", "time": "周一 14:00-15:40", "week_range": "9-16"},
        {"name": "专题讲座", "time": "周五 10:00-11:40", "week_range": "1-8,13,15,17"},
    ]
    
    # 测试不同周次
    test_weeks = [1, 5, 9, 13, 15]
    
    for week in test_weeks:
        print(f"第{week}周周一应该上的课程:")
        for course in courses:
            if "周一" in course["time"]:
                if is_in_week_range(week, course["week_range"]):
                    print(f"  ✅ {course['name']} ({course['time']}) - {course['week_range']}")
                else:
                    print(f"  ❌ {course['name']} (本周不上课) - {course['week_range']}")
        print()


def test_edge_cases():
    """测试边界情况"""
    print("=" * 60)
    print("测试6：边界情况")
    print("=" * 60)
    
    # 测试第20周（学期最后一周）
    week_20 = get_week_number(date(2025, 12, 29))
    print(f"✅ 第20周: {date(2025, 12, 29)} → 第{week_20}周")
    
    # 测试第21周（超出学期范围）
    week_21 = get_week_number(date(2026, 1, 5))
    print(f"✅ 第21周（超出范围）: {date(2026, 1, 5)} → {week_21}")
    
    # 测试学期开始前
    before = get_week_number(date(2025, 8, 25))
    print(f"✅ 学期开始前: {date(2025, 8, 25)} → {before}")
    
    print()


def main():
    """运行所有测试"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 16 + "课程周次功能测试" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    try:
        test_week_number_calculation()
        test_week_date_range()
        test_is_in_week_range()
        test_format_week_range()
        test_course_scenario()
        test_edge_cases()
        
        print("=" * 60)
        print("✅ 所有测试完成！")
        print("=" * 60)
        print()
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

