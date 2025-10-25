-- ѧ������student�������ֺ�����Ϣ
CREATE TABLE student (
    student_id VARCHAR(20) NOT NULL COMMENT 'ѧ��Ψһѧ�ţ�������',
    student_name VARCHAR(50) NOT NULL COMMENT 'ѧ������',
    political_status VARCHAR(20) COMMENT '������ò���磺Ⱥ��/������Ա/�й���Ա�ȣ�',
    phone VARCHAR(20) NOT NULL COMMENT 'ѧ����ϵ�绰',
    create_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
    PRIMARY KEY (student_id)
) COMMENT 'ѧ����Ϣ��';


-- �γ̱���course����ά��ԭ�нṹ
CREATE TABLE course (
    course_id VARCHAR(20) NOT NULL COMMENT '�γ�Ψһ���',
    course_name VARCHAR(100) NOT NULL COMMENT '�γ�����',
    teacher_name VARCHAR(50) NOT NULL COMMENT '�ڿν�ʦ����',
    course_time VARCHAR(50) NOT NULL COMMENT '�Ͽ�ʱ�䣨����һ3-4�ڣ�',
    course_place VARCHAR(50) NOT NULL COMMENT '�Ͽεص㣨���ѧ¥A201��',
    semester VARCHAR(20) NOT NULL COMMENT '����ѧ�ڣ���2023-2024ѧ���ϣ�',
    week_range VARCHAR(50) COMMENT '�Ͽ���Σ�������磺1-8,13,15,17 �� 9-16��',
    PRIMARY KEY (course_id)
) COMMENT '�γ���Ϣ��';


-- ���ڱ���attendance���������߼�����
CREATE TABLE attendance (
    attendance_id SERIAL PRIMARY KEY COMMENT '���ڼ�¼ΨһID��������',
    student_id VARCHAR(20) NOT NULL COMMENT '����ѧ��ѧ��',
    course_id VARCHAR(20) NOT NULL COMMENT '�����γ̱��',
    attendance_date DATE NOT NULL COMMENT '��������',
    attendance_type VARCHAR(20) NOT NULL COMMENT '����״̬������/�ٵ�/����/����/��٣�',
    late_minutes INT DEFAULT 0 COMMENT '�ٵ������������ٵ�״̬��д��',
    attendance_note VARCHAR(200) COMMENT '���ڱ�ע',
    create_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '��¼����ʱ��',
    -- �������ѧ����
    CONSTRAINT fk_attendance_student 
        FOREIGN KEY (student_id) 
        REFERENCES student(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    -- ��������γ̱�
    CONSTRAINT fk_attendance_course 
        FOREIGN KEY (course_id) 
        REFERENCES course(course_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT 'ѧ�����ڼ�¼��';


-- ��ټ�¼����leave_record�����Ƴ���������ֶ�
CREATE TABLE leave_record (
    leave_id SERIAL PRIMARY KEY COMMENT '��ټ�¼ΨһID��������',
    student_id VARCHAR(20) NOT NULL COMMENT '����ѧ��ѧ��',
    leave_type VARCHAR(20) NOT NULL COMMENT '������ͣ��¼�/����/������',
    leave_start_date DATE NOT NULL COMMENT '��ٿ�ʼ����',
    leave_end_date DATE NOT NULL COMMENT '��ٽ�������',
    leave_days INT NOT NULL COMMENT '�������',
    leave_reason VARCHAR(500) NOT NULL COMMENT '���ԭ��',
    create_time TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '�����ύʱ��',
    -- Լ�����������ڡݿ�ʼ����
    CONSTRAINT ck_leave_date CHECK (leave_end_date >= leave_start_date),
    -- �������ѧ����
    CONSTRAINT fk_leave_student 
        FOREIGN KEY (student_id) 
        REFERENCES student(student_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
) COMMENT 'ѧ����ټ�¼�������������̣�';