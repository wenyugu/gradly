from typing import List, Union

from api import db
# model classes and types
from models import User, University, Course, Employer, Position, Graduate, Experience
from models import DegreeType, JobType, Industry


# User Entities
def create_user(skills: List[str] = None) -> int:
    """
    Equivalent to:
        INSERT INTO user (id, skills) VALUES (<id>, <skills>);
    Where <id> is an autoincremented integer (state maintained by program, not DB),
    and <skills> is the comma-joined list passed as input
    """
    if skills is not None:
        skills = ','.join(skills)
    user = User(skills=skills)
    db.session.add(user)
    db.session.commit()
    return user.id


def read_user(id: int) -> User:
    """
    Equivalent to:
        SELECT * FROM user WHERE id = <id>;
    """
    return User.query.get(id)


def update_user(user: Union[int, User], new_skills: List[str]) -> bool:
    """Update a user's skill list.

    If `new_skills` is None, then `user.skills` is set to None, otherwise
    `user.skills` is the comma-joined concatenation of `new_skills`. Old values
    are overwritten.

    Returns true if user exists and update is successful.
    ---
    Equivalent to:
        UPDATE user SET skills = <new_skills> WHERE id = <userID>;
    where <new_skills> is the comma-joined input list,
    and <userID> is the `user` argument if an integer, otherwise `user.id` if passed a "tuple"
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
    """
    Equivalent to:
        DELETE FROM user WHERE id = <id>;
    """
    user = read_user(id)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return True
    return False


# University Entities
def read_or_create_university(name: str) -> University:
    """
    Equivalent to:
        INSERT INTO university (name) VALUES (
            SELECT '<name>'
            WHERE NOT EXISTS (SELECT 1 FROM university WHERE name = <name>);
        SELECT * FROM university WHERE name = <name>;
    """
    uni = read_university(name)
    if uni is not None:
        return uni
    uni = University(name=name)
    db.session.add(uni)
    db.session.commit()
    return uni


def read_university(name: str) -> University:
    """
    Equivalent to:
        SELECT * FROM university WHERE name = <name>;
    """
    return University.query.get(name)


# Why would we need to update a university?
# def update_university(name: str) -> bool:
#     pass


def delete_university(name: str) -> bool:
    """
    Equivalent to:
        DELETE FROM university WHERE name = <name>;
    """
    uni = University.query.get(name)
    if uni is not None:
        db.session.delete(uni)
        db.session.commit()
        return True
    return False


# Course Entities
def create_course(name: str, num: str, uni: str) -> int:
    """
    Equivalent to:
        INSERT INTO course (id, universityName, courseTitle, courseNumber)
            VALUES (<id>, <uni>, <name>, <num>);
    Where <id> is an autoincremented integer,
    and <uni> is a university name (existence enforced by FK constraint)
    """
    university = read_university(uni)
    if university is None:
        # TODO: do we want to create the missing university here or raise an error?
        raise ValueError('No such university: {}'.format(uni))
    course = Course(courseTitle=name, courseNumber=num, offered_at=university)
    db.session.add(course)
    db.session.commit()
    return course.id


def read_course(id: int) -> Course:
    """
    Equivalent to:
        SELECT * FROM course WHERE id = <id>;
    """
    return Course.query.get(id)


def find_course(title: str, num: str, uni: str) -> Course:
    """
    Equivalent to:
        a = SELECT * FROM course
            WHERE universityName = <uni>
            AND courseTitle = <title>
            AND courseNumber = <num>;
        if a == NULL:
            a = SELECT * FROM course
                WHERE universityName = <uni>
                AND courseNumber = <num>;
        if a == NULL:
            a = SELECT * FROM course
                WHERE universityName = <uni>
                AND courseTitle = <title>;
    Where `a` is the returned row set. If no exact match exists, search for matches
    with different titles or numbers, in that order.
    """
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
    """
    Equivalent to:
        UPDATE course
            SET courseTitle = <name>, courseNumber = <num>
            WHERE id = <id>;
    Where <name> and <num> are specified as kwargs (and only included if specified)
    """
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
    """
    Equivalent to:
        DELETE FROM course WHERE id = <id>;
    """
    course = read_course(id)
    if course is not None:
        db.session.delete(course)
        db.session.commit()
        return True
    return False


# Employer Entities
def read_or_create_employer(name: str) -> Employer:
    """
    Equivalent to:
        INSERT INTO employer (name) VALUES
            SELECT '<name>'
            WHERE NOT EXISTS (SELECT 1 FROM employer WHERE name = <name>);
        SELECT * FROM employer WHERE name = <name>;
    """
    employer = read_employer(name)
    if employer is not None:
        return employer
    employer = Employer(name=name)
    db.session.add(employer)
    db.session.commit()
    return employer


def read_employer(name: str) -> Employer:
    """
    Equivalent to:
        SELECT * FROM employer WHERE name = <name>;
    """
    return Employer.query.get(name)


def update_employer(name: str):
    pass


def delete_employer(name: str) -> bool:
    """
    Equivalent to:
        DELETE FROM employer WHERE name = '<name>';
    """
    employer = read_employer(name)
    if employer is not None:
        db.session.delete(employer)
        db.session.commit()
        return True
    return False


# Position Entities
def create_position(employer: Union[str, Employer], title: str) -> int:
    """
    Equivalent to:
        INSERT INTO position (id, employerName, jobTitle)
            VALUES (<id>, <employer>, <title>);
    Where <employer> is `employer` argument if a string, otherwise `employer.name` if passed a "tuple"
    """
    if not isinstance(employer, Employer):
        employer = read_or_create_employer(employer)
    if employer is None:
        # TODO: create new or error?
        raise ValueError('No such employer: {}'.format(employer))
    position = Position(company=employer, jobTitle=title)
    db.session.add(position)
    db.session.commit()
    return position.id


def read_position(id: int) -> Position:
    """
    Equivalent to:
        SELECT * FROM postion WHERE id = <id>;
    """
    return Position.query.get(id)


def find_position(employer: Union[str, Employer], title: str) -> Position:
    """
    Equivalent to:
        SELECT * FROM position WHERE employerName = <employer> AND jobTitle = <title>;
    Where <employer> is `employer` argument if a string, otherwise `employer.name` if passed a "tuple"
    """
    if not isinstance(employer, Employer):
        employer = read_employer(employer)
    return Position.query.filter_by(company=employer, jobTitle=title).first()


def update_position(id: int, **kwargs) -> bool:
    """
    Equivalent to:
        UPDATE position
            SET employerName = <employer>, title = <title>
            WHERE id = <id>;
    Where <employer> and <title> are specified as kwargs (and only included if specified)
    """
    position = read_position(id)
    if position is not None:
        for key, value in kwargs.items():
            if key == 'employer':
                if not isinstance(value, str):
                    raise TypeError
                position.employerName = value
            elif key == 'title':
                if not isinstance(value, str):
                    raise TypeError
                position.jobTitle = value
            # elif key == 'focus':
            #     if not isinstance(value, str):
            #         raise TypeError
            #     position.focusArea = value
        db.session.commit()
        return True
    return False


def delete_position(id: int) -> bool:
    """
    Equivalent to:
        DELETE FROM position WHERE id = <id>;
    """
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
    """
    Equivalent to:
        INSERT INTO graduate VALUES
            SELECT <userID>, <uni>, <date>, <degree>, <major>, <gpa>
            WHERE NOT EXISTS (
                SELECT 1 FROM graduate
                WHERE userID = <userID>
                AND university = <uni>
                AND gradDate = <date>
            );
    """
    grad = read_graduation(userID, uni, date)
    if grad is not None:
        return
    grad = Graduate(userID=userID, university=uni, gradDate=date, degree=degree, major=major, gpa=gpa)
    db.session.add(grad)
    db.session.commit()


def read_graduation(userID: int, uni: str, date: int) -> Graduate:
    """
    Equivalent to:
        SELECT * FROM graduate
            WHERE userID = <userID>
            AND university = <uni>
            AND gradDate = <date>
    """
    return Graduate.query.get([userID, uni, date])


def update_graduation(userID: int, uni: str, date: int, **kwargs) -> bool:
    """
    Equivalent to:
        UPDATE graduate
            SET degree = <degree>, major = <major>, gpa = <gpa>
            WHERE userID = <userID> AND university = <uni> AND gradDate = <date>;
    Where <degree>, <major>, and <gpa> are specified as kwargs (and only included if specified)
    """
    grad = read_graduation(userID, uni, date)
    if grad is not None:
        for key, value in kwargs.items():
            if key == 'degree':
                if not isinstance(value, DegreeType):
                    raise TypeError('degree must be DegreeType')
                grad.degree = value
            elif key == 'major':
                if not isinstance(value, str):
                    raise TypeError('major must be str')
                grad.major = value
            elif key == 'gpa':
                if not isinstance(value, float):
                    raise TypeError('gpa must be float')
                grad.gpa = value
        db.session.commit()
        return True
    return False


def delete_graduation(userID: int, uni: str, date: int) -> bool:
    """
    Equivalent to:
        DELETE FROM graduate WHERE userID = <userID>;
    """
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
    """
    Equivalent to:
        INSERT INTO experience VALUES
            SELECT <userID>, <posID>, <industry>, <salary>, <type>, <rating>
            WHERE NOT EXISTS (
                SELECT 1 FROM experience
                WHERE userID = <userID>
                AND positionID = <posID>
            );
    """
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
    """
    Equivalent to:
        SELECT * FROM experience WHERE userID = <userID> AND positionID = <posID>
    """
    return Experience.query.get([userID, posID])


def update_experience(userID: int, posID: int, **kwargs) -> bool:
    """
    Equivalent to:
        UPDATE experience
            SET salary = <salary>, type = <type>, rating = <rating>, industry = <industry>
            WHERE userID = <userID> AND positionID = <posID>;
    Where <industry>, <salary>, <type>, and <rating> are specified as kwargs (and only included if specified)
    """
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
    """
    Equivalent to:
        DELETE FROM experience WHERE userID = <userID> AND positionID = <posID>;
    """
    exp = read_experience(userID, posID)
    if exp is not None:
        db.session.delete(exp)
        db.session.commit()
        return True
    return False


# Course Enrollment relationships
def add_enrollment(user: Union[int, User], course: Union[int, Course]) -> bool:
    """
    Equivalent to:
        INSERT INTO enrollement VALUES (user, course);
    """
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
    """
    Equivalent to:
        DELETE FROM enrollment WHERE userID = <user> AND courseID = <course>;
    """
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
