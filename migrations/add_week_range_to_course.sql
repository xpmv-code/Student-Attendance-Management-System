-- 为course表添加week_range字段的迁移脚本
-- 执行日期: 2025-10-25
-- 用途: 支持课程周次范围管理

-- 添加week_range字段
ALTER TABLE course ADD COLUMN IF NOT EXISTS week_range VARCHAR(50);

-- 添加注释
COMMENT ON COLUMN course.week_range IS '上课周次范围（如：1-8,13,15,17 或 9-16）';

-- 查看修改结果
SELECT course_id, course_name, course_time, week_range FROM course LIMIT 5;

