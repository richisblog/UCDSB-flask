from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    student_id = db.Column(db.String(16), unique=True)
    term_code = db.Column(db.String(8))

    courses = db.relationship('Course', backref='student', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(16))     # e.g., MAT 021C A06
    title = db.Column(db.String(128))
    status = db.Column(db.String(16))          # Registered / Waitlist
    instructor = db.Column(db.String(64))
    days = db.Column(db.String(8))             # e.g., MWF
    time = db.Column(db.String(64))            # e.g., 8:00–8:50
    location = db.Column(db.String(128))

    student_id_fk = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
