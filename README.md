# Student Performance & Analytics System

A Streamlit web application for importing, analyzing, and managing student performance data, built with Python and SQLite for the BIT1034 Advanced Programming case study project.

## Features

- **CSV Import** — upload a student performance dataset, automatically cleaned (missing values handled) and imported into a database.
- **Dashboard** — view total students, average final grade, pass rate, grade-letter distribution, top/bottom 5 students, and average grade by gender.
- **Manage Students** — view all records, edit a student's final grade, delete a record (full CRUD).
- **Search** — look up students by name.

## Tech Stack

- Python 3.12
- Streamlit (web interface)
- SQLite (database, via Python's built-in `sqlite3`)
- pandas (CSV processing)

## Project Structure

```
student-performance-system/
├── app.py                # Streamlit app: navigation and all pages
├── database.py           # SQLite connection and CRUD functions
├── data_processor.py     # CSV loading and cleaning logic
├── student.py             # Student class (OOP: grading logic)
├── data/
│   └── student_performance.csv
├── screenshots/
├── requirements.txt
└── README.md
```

## Setup & Running

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app opens automatically at `http://localhost:8501`.

## Dataset

`data/student_performance.csv` — student records including attendance rate, study hours per week, previous grade, extracurricular activities, parental support, and final grade.

## Database Schema

```sql
CREATE TABLE students (
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
);
```

All queries use parameterized statements to prevent SQL injection.

## Screenshots

See the `screenshots/` folder for app walkthrough images.
