from app import db
from datetime import datetime


class Student(db.Model):
    __tablename__ = 'student'  # 对应数据库表名

    # 字段定义（与class.sql保持一致）
    student_id = db.Column(db.String(20), primary_key=True, comment='学生学号（主键）')
    student_name = db.Column(db.String(50), nullable=False, comment='学生姓名')
    political_status = db.Column(db.String(20), comment='政治面貌')
    phone = db.Column(db.String(20), nullable=False, comment='联系电话')
    create_time = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='创建时间')

    # 关系映射（关联考勤记录和请假记录）
    attendances = db.relationship(
        'Attendance',
        backref='student',  # 在Attendance中可通过student属性访问关联的学生
        lazy='dynamic',
        cascade='all, delete-orphan'  # 删除学生时级联删除关联的考勤记录
    )
    leave_records = db.relationship(
        'LeaveRecord',
        backref='student',
        lazy='dynamic',
        cascade='all, delete-orphan'  # 删除学生时级联删除关联的请假记录
    )

    def __repr__(self):
        return f'<Student {self.student_id}: {self.student_name}>'