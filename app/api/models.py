import enum
from api import db

class CompanySize(enum.Enum):
    micro = '< 10'
    small = '< 250'
    medium = '< 500'
    large = '< 1000'
    enterprise = '1000+'


class DegreeType(enum.Enum):
    associates = 1
    bachelors = 2
    masters = 3
    phd = 4


class JobType(enum.Enum):
    intern = 1
    co_op = 2
    research = 3
    part_time = 4
    full_time = 5


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skills = db.Column(db.Text)

    def __repr__(self):
        return '<User {}>'.format(self.userID)


class University(db.Model):
    name = db.Column(db.String(255), primary_key=True)
    courses = db.relationship('Course', backref='offered_at', lazy=True)

    def __repr__(self):
        return '<University {}>'.format(self.name)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    universityName = db.Column(db.String(255), db.ForeignKey('university.name'), primary_key=True)
    courseTitle = db.Column(db.String(255), nullable=False)
    focusArea = db.Column(db.String(255))   # TODO: perhaps ENUM would be better?
    # offered_at: backref to University

    def __repr__(self):
        return '<Course {} at {}>'.format(self.courseTitle, self.university)


class Employer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    industry = db.Column(db.String(255))    # TODO: perhaps ENUM would be better?
    size = db.Column(
        db.Enum(CompanySize, values_callable=lambda x: [e.value for e in x])
    )
    positions = db.relationship('Position', backref='company', lazy=True)

    def __repr__(self):
        return '<Employer {}>'.format(self.name)


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employerID = db.Column(db.Integer, db.ForeignKey('employer.id'), primary_key=True)
    # company: backref to Employer
    jobTitle = db.Column(db.String(50))
    focusArea = db.Column(db.String(255))
    minSalary = db.Column(db.Integer)
    maxSalary = db.Column(db.Integer)

    def __repr__(self):
        return '<Job: {}>'.format(self.jobTitle)


graduated = db.Table('graduated',
    # entity attributes
    db.Column('userID', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('university', db.String(255), db.ForeignKey('university.name'), primary_key=True),
    db.Column('gradDate', db.Date, primary_key=True),
    # relationship attributes
    db.Column('degree', db.Enum(DegreeType)),
    db.Column('major', db.String(255)),
    db.Column('gpa', db.Numeric(3,2)),
)


enrollment = db.Table('enrollment',
    # entity attributes
    db.Column('userID', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('courseID', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('university', db.String(255), db.ForeignKey('university.name'), primary_key=True),
)


experience = db.Table('experience',
    db.Column('userID', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('employerID', db.Integer, db.ForeignKey('employer.id'), primary_key=True),
    db.Column('jobTitle', db.String(50), db.ForeignKey('position.jobTitle'), primary_key=True),

    db.Column('startDate', db.Date),
    db.Column('salary', db.Integer),
    db.Column('type', db.Enum(JobType)),
    db.Column('rating', db.SmallInteger),
    db.Column('location', db.String(255)),
)
