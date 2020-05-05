from sqlite3 import Row
from typing import List

from api import con
from db_types import DegreeType, JobType, Industry


def create_user(skills: List[str] = None) -> int:
    if skills is not None:
        skills = ','.join(skills)
    return con.execute('INSERT INTO user (skills) VALUES (?)', (skills,)) \
              .lastrowid


def read_user(id: int) -> Row:
    return con.execute('SELECT * FROM user WHERE id = ?', (id,)) \
              .fetchone()


def update_user(userID: int, new_skills: List[str]) -> bool:
    if new_skills is not None:
        new_skills = ','.join(new_skills)
    n = con.execute('UPDATE user SET skills = :skills WHERE id = :id',
                    {"id": userID, "skills": new_skills}).rowcount
    return n > 0


def delete_user(id: int) -> bool:
    n = con.execute('DELETE FROM user WHERE id = ?', (id,)).rowcount
    return n > 0


def create_university(name: str) -> Row:
    name = name.strip()
    con.execute('INSERT INTO university (name) VALUES (?)', (name,))
    return read_university(name)


def read_university(name: str) -> Row:
    # `name` column is `COLLATE NOCASE` so we just need to strip whitespace
    name = name.strip()
    return con.execute('SELECT * FROM university WHERE name = ?', (name,)) \
              .fetchone()


def read_or_create_university(name: str) -> Row:
    ret = read_university(name)
    if ret is None:
        ret = create_university(name)
    return ret


def update_university(old_name: str, new_name: str) -> bool:
    """Change the name of a university and update all references to it."""
    pass


def delete_university(name: str) -> bool:
    name = name.strip()
    n = con.execute('DELETE FROM university WHERE name = ?', (name,)).rowcount
    return n > 0


def create_course(name: str, num: str, uni: str) -> int:
    # standardize course name and number before inserting
    name = name.strip()
    num = num.strip().upper()

    university = read_university(uni)
    if university is None:
        create_university(uni)

    return con.execute('''INSERT INTO course (universityName, courseTitle, courseNumber)
                       VALUES (?, ?, ?)''', (uni, name, num)) \
              .lastrowid


def read_course(id: int) -> Row:
    return con.execute('SELECT * FROM course WHERE id = ?', (id,)) \
              .fetchone()


def find_course(name: str, num: str, uni: str) -> Row:
    name = name.strip()
    num = num.strip()
    uni = uni.strip()
    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseTitle = ?
                            AND courseNumber = ?''',
                         (uni, name, num)) \
                .fetchone()
    if result is not None:
        return result

    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseNumber = ?''',
                         (uni, num)) \
                .fetchone()

    if result is not None:
        return result

    result = con.execute('''SELECT * FROM course
                            WHERE universityName = ?
                            AND courseTitle = ?''',
                         (uni, name)) \
                .fetchone()
    return result  # may be None, but that's ok if none of the cases match


def update_course(id: int, name: str, num: str) -> bool:
    """Change the name/number of a course and update all references to it."""
    n = con.execute('''UPDATE course
                       SET courseTitle = :name, courseNumber = :num
                       WHERE id = :id
                    ''', {'id': id, 'name': name, 'num': num}).rowcount
    return n > 0


def delete_course(id: int) -> bool:
    n = con.execute('DELETE FROM course WHERE id = ?', (id,)).rowcount
    return n > 0


def create_employer(name: str) -> Row:
    name = name.strip()
    c = con.execute('INSERT INTO employer (name) VALUES (?)', (name,))
    return c.execute('SELECT * FROM employer WHERE name = ?', (name,)) \
            .fetchone()


def read_employer(name: str) -> Row:
    name = name.strip()
    return con.execute('SELECT * FROM employer WHERE name = ?', (name,)) \
              .fetchone()


def read_or_create_employer(name: str) -> Row:
    ret = read_employer(name)
    if ret is None:
        ret = create_employer(name)
    return ret


def update_employer(old_name: str, new_name: str) -> bool:
    """Change the name of an employer and update all references to it."""
    pass


def delete_employer(name: str) -> bool:
    name = name.strip()
    n = con.execute('DELETE FROM employer WHERE name = ?', (name,)).rowcount
    return n > 0


def create_position(employer: str, title: str) -> int:
    title = title.strip()
    emp = read_employer(employer)
    if emp is None:
        emp = create_employer(employer)

    return con.execute('''INSERT INTO position (employerName, jobTitle)
                          VALUES (?, ?)''', (emp['name'], title)) \
              .lastrowid


def read_position(id: int) -> Row:
    return con.execute('SELECT * FROM position WHERE id = ?', (id,)) \
              .fetchone()


def find_position(employer: str, title: str) -> Row:
    employer = employer.strip()
    title = title.strip()
    return con.execute('''SELECT * FROM position
                          WHERE employerName = ?
                          AND jobTitle = ?''',
                       (employer, title)) \
              .fetchone()


def update_position(id: int, **kwargs) -> bool:
    new_employer = kwargs.get('employer')
    new_title = kwargs.get('title')
    if new_employer:
        new_employer = 'employerName = ' + new_employer
    if new_title:
        new_title = 'title = ' + new_title

    set_clause = ', '.join((new_employer, new_title))
    if set_clause == '':
        return False
    n = con.execute('''UPDATE position
                       SET ?
                       WHERE id = ?''',
                    (set_clause, id)) \
           .rowcount
    return n > 0


def delete_position(id: int) -> bool:
    n = con.execute('DELETE FROM position WHERE id = ?', (id,)).rowcount
    return n > 0


def create_education(
    userID: int,
    uni: str,
    year: int,
    degree: DegreeType = None,
    major: str = None,
    gpa: float = None,
) -> int:
    university = read_university(uni)
    if university is None:
        university = create_university(uni)

    id = con.execute('''INSERT INTO education (userID, university, year)
                        VALUES (?, ?, ?)''',
                     (userID, uni, year)) \
            .lastrowid
    update_education(id, degree=degree, major=major, gpa=gpa)
    return id


def read_education(id: int) -> Row:
    return con.execute('SELECT * FROM education WHERE id = ?', (id,)).fetchone()


def find_education(userID: int, uni: str, year: int) -> Row:
    uni = uni.strip()
    return con.execute('''SELECT * FROM education
                          WHERE userID = ?
                          AND university = ?
                          AND year = ?''',
                       (userID, uni, year)) \
              .fetchone()


def update_education(id: int, **kwargs) -> bool:
    new_degree = kwargs.get('degree')
    new_major = kwargs.get('major')
    new_gpa = kwargs.get('gpa')

    n = 0

    if new_degree is not None:
        if isinstance(new_degree, DegreeType):
            new_degree = new_degree.value
        n += con.execute('''UPDATE education SET degree = :degree
                            WHERE id = :id
                         ''',
                         {
                             'degree': new_degree,
                             'id': id
                         }) \
                .rowcount

    if new_major is not None:
        new_major = new_major.strip().title()
        n += con.execute('''UPDATE education SET major = :major
                            WHERE id = :id
                         ''',
                         {
                             'major': new_major,
                             'id': id
                         }) \
                .rowcount

    if new_gpa is not None:
        n += con.execute('''UPDATE education SET gpa = :gpa
                            WHERE id = :id
                         ''',
                         {
                             'gpa': new_gpa,
                             'id': id,
                         }) \
                .rowcount

    return n > 0


def delete_education(id: int) -> bool:
    n = con.execute('DELETE FROM education WHERE id = ?', (id,)).rowcount
    return n > 0


def create_experience(
    userID: int,
    posID: int,
    industry: Industry = None,
    salary: int = None,
    type: JobType = None,
    rating: int = None,
):
    con.execute('INSERT INTO experience (userID, positionID) VALUES (?, ?)',
                (userID, posID))
    update_experience(userID, posID, industry=industry,
                      salary=salary, type=type, rating=rating)


def read_experience(userID: int, posID: int) -> Row:
    return con.execute('''SELECT * FROM experience
                          WHERE userID = ? AND positionID = ?''',
                       (userID, posID)) \
              .fetchone()


def update_experience(userID: int, posID: int, **kwargs) -> bool:
    new_industry = kwargs.get('industry')
    new_salary = kwargs.get('salary')
    new_type = kwargs.get('type')
    new_rating = kwargs.get('rating')

    n = 0

    if new_industry:
        if isinstance(new_industry, Industry):
            new_industry = new_industry.value
        n += con.execute('''UPDATE experience SET industry = :industry
                            WHERE userID = :user
                            AND positionID = :pos
                         ''',
                         {
                             'industry': new_industry,
                             'user': userID,
                             'pos': posID,
                         }) \
                .rowcount
    if new_salary:
        n += con.execute('''UPDATE experience SET salary = :salary
                            WHERE userID = :user
                            AND positionID = :pos
                         ''',
                         {
                             'salary': new_salary,
                             'user': userID,
                             'pos': posID,
                         }) \
                .rowcount
    if new_type:
        if isinstance(new_type, JobType):
            new_type = new_type.value
        n += con.execute('''UPDATE experience SET type = :type
                            WHERE userID = :user
                            AND positionID = :pos
                         ''',
                         {
                             'type': new_type,
                             'user': userID,
                             'pos': posID,
                         }) \
                .rowcount
    if new_rating:
        n += con.execute('''UPDATE experience SET rating = :rating
                            WHERE userID = :user
                            AND positionID = :pos
                         ''',
                         {
                             'rating': new_rating,
                             'user': userID,
                             'pos': posID,
                         }) \
                .rowcount

    return n > 0


def delete_experience(userID: int, posID: int) -> bool:
    n = con.execute('''DELETE FROM experience
                       WHERE userID = ? AND positionID = ?''',
                    (userID, posID)) \
           .rowcount
    return n > 0


def add_enrollment(educationID: int, courseID: int) -> bool:
    n = con.execute('INSERT INTO enrollment VALUES (?, ?)',
                    (educationID, courseID)) \
           .rowcount
    return n > 0


def check_enrollment(educationID: int, courseID: int) -> bool:
    r = con.execute('''SELECT * FROM enrollment
                       WHERE educationID = ? AND courseID = ?''',
                    (educationID, courseID)).fetchall()
    return len(r) > 0


def check_enrollment_all(userID: int, courseID: int) -> bool:
    r = con.execute('''SELECT * FROM enrollment e JOIN education edu
                       ON e.educationID = edu.id
                       WHERE userID = ? AND courseID = ?''',
                    (userID, courseID)).fetchall()
    return len(r) > 0


def remove_enrollment(educationID: int, courseID: int) -> bool:
    n = con.execute('''DELETE FROM enrollment
                       WHERE educationID = ? AND courseID = ?''',
                    (educationID, courseID)).rowcount
    return n > 0
