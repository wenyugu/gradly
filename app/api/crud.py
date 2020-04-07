from typing import List, Union

from api import db
# model classes and types
from models import User, University, Course, Employer, Position, Graduate, Experience
from models import DegreeType, JobType, Industry


# User Entities
def create_user(skills: List[str] = None) -> int:
    if skills is not None:
        skills = ','.join(skills)
    user = User(skills=skills)
    db.session.add(user)
    db.session.commit()
    return user.id


def read_user(id: int) -> User:
    return User.query.get(id)


def update_user(user: Union[int, User], new_skills: List[str]) -> bool:
    """Update a user's skill list.

    If `new_skills` is None, then `user.skills` is set to None, otherwise
    `user.skills` is the comma-joined concatenation of `new_skills`. Old values
    are overwritten.

    Returns true if user exists and update is successful.
    """
    if not isinstance(user, User):
        user = read_user(id)

    if user is None:
        return False

    if new_skills is None:
        user.skills = None
    else:
        user.skills = ','.join(new_skills)
    db.session.commit()
    return True


def delete_user(id: int) -> bool:
    user = read_user(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


# University Entities
def read_or_create_university(name: str) -> University:
    uni = read_university(name)
    if uni is not None:
        return uni
    uni = University(name=name)
    db.session.add(uni)
    db.session.commit()
    return uni


def read_university(name: str) -> University:
    return University.query.get(name)


# Why would we need to update a university?
# def update_university(name: str) -> bool:
#     pass


def delete_university(name: str) -> bool:
    uni = University.query.get(name)
    if uni is not None:
        db.session.delete(uni)
        db.session.commit()
        return True
    return False


# Course Entities
def create_course(name: str, num: str, uni: str) -> int:
    university = read_university(uni)
    if university is None:
        # TODO: do we want to create the missing university here or raise an error?
        raise ValueError('No such university: {}'.format(uni))
    course = Course(courseTitle=name, courseNumber=num, offered_at=university)
    db.session.add(course)
    db.session.commit()
    return course.id


def read_course(id: int) -> Course:
    return Course.query.get(id)


def find_course(title: str, num: str, uni: str) -> Course:
    # try for an exact match
    result = Course.query.filter_by(universityName=uni,
                                    courseTitle=title,
                                    courseNumber=num).first()
    if result is not None:
        return result

    # try matching just the course number
    result = Course.query.filter_by(universityName=uni,
                                    courseNumber=num).first()
    if result is not None:
        return result

    # try matching just the course title
    result = Course.query.filter_by(universityName=uni,
                                    courseTitle=title).first()
    if result is not None:
        return result

    # no match found
    return None


def update_course(id: int, **kwargs) -> bool:
    course = read_course(id)
    if course is not None:
        for key, value in kwargs.items():
            if key == 'name':
                if not isinstance(value, str):
                    raise TypeError
                course.courseTitle = value
            elif key == 'num':
                if not isinstance(value, str):
                    raise TypeError
                course.courseNumber = value
            # elif key == 'focus':
            #     if not isinstance(value, str):
            #         raise TypeError
            #     course.focusArea = value
        db.session.commit()
        return True
    return False


def delete_course(id: int) -> bool:
    course = read_course(id)
    if course is not None:
        db.session.delete(course)
        db.session.commit()
        return True
    return False


# Employer Entities
def read_or_create_employer(name: str) -> Employer:
    employer = read_employer(name)
    if employer is not None:
        return employer
    employer = Employer(name=name)
    db.session.add(employer)
    db.session.commit()
    return employer


def read_employer(name: str) -> Employer:
    return Employer.query.get(name)


# def update_employer(id: int, **kwargs) -> bool:
#     employer = read_employer(id)
#     if employer is not None:
#         for key, value in kwargs.items():
#             if key == 'name':
#                 if not isinstance(value, str):
#                     raise TypeError
#                 employer.name = value
#             elif key == 'industry':
#                 if not isinstance(value, str):
#                     raise TypeError
#                 employer.industry = value
#             # elif key == 'size':
#             #     if not isinstance(value, CompanySize):
#             #         raise TypeError
#             #     employer.size = value
#         db.session.commit()
#         return True
#     return False


def delete_employer(id: int) -> bool:
    employer = read_employer(id)
    if employer is not None:
        db.session.delete(employer)
        db.session.commit()
        return True
    return False


# Position Entities
def create_position(employer: Union[str, Employer], title: str) -> int:
    if not isinstance(employer, Employer):
        employer = read_employer(employer)
    if employer is None:
        # TODO: create new or error?
        raise ValueError('No such employer: {}'.format(employer))
    position = Position(company=employer, jobTitle=title)
    db.session.add(position)
    db.session.commit()
    return position.id


def read_position(id: int) -> Position:
    return Position.query.get(id)


def find_position(employer: Union[str, Employer], title: str) -> Position:
    if not isinstance(employer, Employer):
        employer = read_employer(employer)
    return Position.query.filter_by(company=employer, jobTitle=title).first()


def update_position(id: int, **kwargs) -> bool:
    position = read_position(id)
    if position is not None:
        for key, value in kwargs.items():
            if key == 'title':
                if not isinstance(value, str):
                    raise TypeError
                position.jobTitle = value
            elif key == 'focus':
                if not isinstance(value, str):
                    raise TypeError
                position.focusArea = value
        db.session.commit()
        return True
    return False


def delete_position(id: int) -> bool:
    position = read_position(id)
    if position is not None:
        db.session.delete(position)
        db.session.commit()
        return True
    return False


# Graduation relationships
def create_graduation(
    userID: int,
    uni: str,
    date: int,
    degree: DegreeType = None,
    major: str = None,
    gpa: float = None,
):
    grad = read_graduation(userID, uni, date)
    if grad is not None:
        return
    grad = Graduate(userID=userID, university=uni, gradDate=date, degree=degree, major=major, gpa=gpa)
    db.session.add(grad)
    db.session.commit()


def read_graduation(userID: int, uni: str, date: int) -> Graduate:
    return Graduate.query.get([userID, uni, date])


def update_graduation(userID: int, uni: str, date: int, **kwargs) -> bool:
    grad = read_graduation(userID, uni, date)
    if grad is not None:
        for key, value in kwargs.items():
            if key == 'degree':
                if not isinstance(value, DegreeType):
                    raise TypeError
                grad.degree = value
            elif key == 'major':
                if not isinstance(value, str):
                    raise TypeError
                grad.major = value
            elif key == 'gpa':
                if not isinstance(value, float):
                    raise TypeError
                grad.gpa = value
        db.session.commit()
        return True
    return False


def delete_graduation(userID: int, uni: str, date: int) -> bool:
    grad = read_graduation(userID, uni, date)
    if grad is not None:
        db.session.delete(grad)
        db.session.commit()
        return True
    return False


# Employment Experience relationships
def create_experience(
    userID: int,
    posID: int,
    industry: Industry = None,
    salary: int = None,
    type: JobType = None,
    rating: int = None,
):
    exp = read_experience(userID, posID)
    if exp is not None:
        return
    exp = Experience(userID=userID,
                     positionID=posID,
                     salary=salary,
                     type=type,
                     rating=rating,
                     industry=industry
                     )
    db.session.add(exp)
    db.session.commit()


def read_experience(userID: int, posID: int) -> Experience:
    return Experience.query.get([userID, posID])


def update_experience(userID: int, posID: int, **kwargs) -> bool:
    exp = read_experience(userID, posID)
    if exp is not None:
        for key, value in kwargs.items():
            if key == 'salary':
                if not isinstance(value, int):
                    raise TypeError
                exp.salary = value
            elif key == 'type':
                if not isinstance(value, JobType):
                    raise TypeError
                exp.type = value
            elif key == 'rating':
                if not isinstance(value, int):
                    raise TypeError
                exp.rating = value
            elif key == 'industry':
                if not isinstance(value, Industry):
                    raise TypeError
                exp.industry = value
        db.session.commit()
        return True
    return False


def delete_experience(userID: int, posID: int) -> bool:
    exp = read_experience(userID, posID)
    if exp is not None:
        db.session.delete(exp)
        db.session.commit()
        return True
    return False


# Course Enrollment relationships
def add_enrollment(user: Union[int, User], course: Union[int, Course]) -> bool:
    if not isinstance(user, User):
        user = User.query.get(user)
    if not isinstance(course, Course):
        course = Course.query.get(course)
    if user is None or course is None:
        return False
    user.courses.append(course)  # alternatively: course.students.append(user)
    db.session.commit()
    return True


def remove_enrollment(user: Union[int, User], course: Union[int, Course]) -> bool:
    if not isinstance(user, User):
        user = User.query.get(user)
    if not isinstance(course, Course):
        course = Course.query.get(course)
    if user is None or course is None:
        return False

    if course in user.courses:
        user.courses.remove(course)  # alternatively: course.students.remove(user)
        db.session.commit()
        return True
    return False
