from sqlite3 import Row
from typing import List

from api import con


def create_user(skills: List[str] = None) -> int:
    if skills is not None:
        skills = ','.join(skills)
    c = con.execute('INSERT INTO user (skills) VALUES (?)', (skills,))
    return c.lastrowid


def read_user(id: int) -> Row:
    return con.execute('SELECT * FROM user WHERE id = ?', (id,)) \
              .fetchone()


def update_user(userID: int, new_skills: List[str]) -> bool:
    if new_skills is not None:
        new_skills = ','.join(new_skills)
    n = con.execute('UPDATE user SET skills = :skills WHERE id = :id',
                    {"id": userID, "skills": new_skills}).rowcount
    if n > 0:
        return True
    return False


def delete_user(id: int) -> bool:
    n = con.execute('DELETE FROM user WHERE id = ?', (id,)).rowcount
    if n > 0:
        return True
    return False


def create_university(name: str) -> Row:
    name = name.strip().title()  # Convert name to titlecase for consistency
    con.execute('INSERT INTO university VALUES (?)', (name,))
    return read_university(name)


def read_university(name: str) -> Row:
    # `name` column is `COLLATE NOCASE` so we just need to strip whitespace
    name = name.strip()
    return con.execute('SELECT * FROM university WHERE name = ?', (name,)) \
              .fetchone()


def update_university(old_name: str, new_name: str) -> bool:
    """Change the name of a university and update all references to it."""
    pass


def delete_university(name: str) -> bool:
    n = con.execute('DELETE FROM university WHERE name = ?', (name,)).rowcount
    if n > 0:
        return True
    return False


def create_course(name: str, num: str, uni: str) -> int:
    # standardize course name and number before inserting
    name = name.strip().title()
    num = num.strip().upper()

    university = read_or_create_university(uni)
    return con.execute('''INSERT INTO course (universityName, courseTitle, courseNumber)
                       VALUES (?, ?, ?)''', (uni, name, num)) \
              .lastrowid


def read_course(id: int) -> Row:
    return con.execute('SELECT * FROM course WHERE id = ?', (id,)) \
              .fetchone()


def find_course(name: str, num: str, uni: str) -> Row:
    pass


def update_course(id: int, **kwargs) -> bool:
    pass


def delete_course(id: int) -> bool:
    pass


# Explicit transaction management
def begin_transaction():
    con.execute('BEGIN')


def commit():
    con.commit()


def rollback():
    con.rollback()
