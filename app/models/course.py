from app import db


class Course(db.Model):
    __tablename__ = 'course'  # 对应数据库表名

    # 字段定义（与class.sql保持一致）
    course_id = db.Column(db.String(20), primary_key=True, comment='课程编号（主键）')
    course_name = db.Column(db.String(100), nullable=False, comment='课程名称')
    teacher_name = db.Column(db.String(50), nullable=False, comment='授课教师姓名')
    course_time = db.Column(db.String(50), nullable=False, comment='上课时间（如：周一3-4节）')
    course_place = db.Column(db.String(50), nullable=False, comment='上课地点（如：教学楼A201）')
    semester = db.Column(db.String(20), nullable=False, comment='学期（如：2023-2024学年上）')
    week_range = db.Column(db.String(50), nullable=True, comment='上课周次（如：1-8,13,15,17 或 9-16）')

    # 关系映射（关联考勤记录）
    attendances = db.relationship(
        'Attendance',
        backref='course',
        lazy='dynamic',
        cascade='all, delete-orphan'  # 删除课程时级联删除关联的考勤记录
    )

    def is_teaching_week(self, week_number):
        """
        判断给定周次是否在该课程的上课周次范围内
        
        Args:
            week_number: 周次（1-20）
            
        Returns:
            bool: True表示该周上课，False表示该周不上课
        """
        if not self.week_range:
            return True  # 如果没有设置周次范围，默认每周都上课
        
        # 解析周次范围，支持格式：1-8,13,15,17 或 9-16
        week_set = set()
        parts = self.week_range.split(',')
        
        for part in parts:
            part = part.strip()
            if '-' in part:
                # 范围格式：1-8
                start, end = part.split('-')
                week_set.update(range(int(start), int(end) + 1))
            else:
                # 单个周次：13
                week_set.add(int(part))
        
        return week_number in week_set
    
    def __repr__(self):
        return f'<Course {self.course_id}: {self.course_name}>'