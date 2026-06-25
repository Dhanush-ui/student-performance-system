import sqlite3

DB_NAME = "students.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            name TEXT,
            gender TEXT,
            attendance_rate REAL,
            study_hours_per_week REAL,
            previous_grade REAL,
            extracurricular_activities INTEGER,
            parental_support TEXT,
            final_grade REAL,
            grade_letter TEXT,
            is_passing INTEGER
        )
    """)
    conn.commit()
    conn.close()


def clear_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    conn.commit()
    conn.close()


def insert_student(student_dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO students (
            student_id, name, gender, attendance_rate, study_hours_per_week,
            previous_grade, extracurricular_activities, parental_support,
            final_grade, grade_letter, is_passing
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        student_dict["student_id"],
        student_dict["name"],
        student_dict["gender"],
        student_dict["attendance_rate"],
        student_dict["study_hours_per_week"],
        student_dict["previous_grade"],
        student_dict["extracurricular_activities"],
        student_dict["parental_support"],
        student_dict["final_grade"],
        student_dict["grade_letter"],
        student_dict["is_passing"],
    ))
    conn.commit()
    conn.close()


def get_all_students():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns


def search_student_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE name LIKE ?", (f"%{name}%",))
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return rows, columns


def update_student(row_id, final_grade, grade_letter, is_passing):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE students
        SET final_grade = ?, grade_letter = ?, is_passing = ?
        WHERE id = ?
    """, (final_grade, grade_letter, is_passing, row_id))
    conn.commit()
    conn.close()


def delete_student(row_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (row_id,))
    conn.commit()
    conn.close()
