from app import db
from datetime import datetime


class Attendance(db.Model):
    __tablename__ = 'attendance'  # 对应数据库表名

    # 字段定义（与class.sql保持一致）
    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='考勤记录ID（自增主键）')
    student_id = db.Column(
        db.String(20),
        db.ForeignKey('student.student_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment='学生学号（外键）'
    )
    course_id = db.Column(
        db.String(20),
        db.ForeignKey('course.course_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment='课程编号（外键）'
    )
    attendance_date = db.Column(db.Date, nullable=False, comment='考勤日期')
    attendance_type = db.Column(db.String(20), nullable=False, comment='考勤状态（正常/迟到/早退/缺席/请假）')
    late_minutes = db.Column(db.Integer, default=0, comment='迟到分钟数（仅迟到状态有效）')
    attendance_note = db.Column(db.String(200), comment='考勤备注')
    create_time = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='记录创建时间')

    def __repr__(self):
        return f'<Attendance {self.attendance_id}: {self.student_id} - {self.course_id}>'