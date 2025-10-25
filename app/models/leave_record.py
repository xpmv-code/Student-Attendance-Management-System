from app import db
from datetime import datetime


class LeaveRecord(db.Model):
    __tablename__ = 'leave_record'  # 对应数据库表名

    # 字段定义（与class.sql保持一致）
    leave_id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='请假记录ID（自增主键）')
    student_id = db.Column(
        db.String(20),
        db.ForeignKey('student.student_id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        comment='学生学号（外键）'
    )
    leave_type = db.Column(db.String(20), nullable=False, comment='请假类型（病假/事假/其他）')
    leave_start_date = db.Column(db.Date, nullable=False, comment='请假开始日期')
    leave_end_date = db.Column(db.Date, nullable=False, comment='请假结束日期')
    leave_days = db.Column(db.Integer, nullable=False, comment='请假天数')
    leave_reason = db.Column(db.String(500), nullable=False, comment='请假原因')
    create_time = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, comment='申请提交时间')

    # 检查约束（结束日期 >= 开始日期，对应class.sql的ck_leave_date）
    __table_args__ = (
        db.CheckConstraint('leave_end_date >= leave_start_date', name='ck_leave_date'),
    )

    def __repr__(self):
        return f'<LeaveRecord {self.leave_id}: {self.student_id}>'