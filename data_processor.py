import pandas as pd
from student import Student
import database


def load_csv(file):
    df = pd.read_csv(file)

    # keep only the clean columns we need, drop the messy duplicate ones
    columns_needed = [
        "StudentID", "Name", "Gender", "AttendanceRate",
        "StudyHoursPerWeek", "PreviousGrade", "ExtracurricularActivities",
        "ParentalSupport", "FinalGrade"
    ]
    df = df[columns_needed]

    # drop rows missing a name or a final grade - can't process those
    df = df.dropna(subset=["Name", "FinalGrade"])

    # fill remaining missing values with safe defaults
    df["StudentID"] = df["StudentID"].fillna(0)
    df["AttendanceRate"] = df["AttendanceRate"].fillna(0)
    df["StudyHoursPerWeek"] = df["StudyHoursPerWeek"].fillna(0)
    df["PreviousGrade"] = df["PreviousGrade"].fillna(0)
    df["ExtracurricularActivities"] = df["ExtracurricularActivities"].fillna(0)
    df["ParentalSupport"] = df["ParentalSupport"].fillna("Unknown")
    df["Gender"] = df["Gender"].fillna("Unknown")

    return df


def import_dataframe_to_db(df):
    database.clear_students()
    count = 0
    for _, row in df.iterrows():
        student = Student(
            student_id=int(row["StudentID"]),
            name=row["Name"],
            gender=row["Gender"],
            attendance_rate=float(row["AttendanceRate"]),
            study_hours_per_week=float(row["StudyHoursPerWeek"]),
            previous_grade=float(row["PreviousGrade"]),
            extracurricular_activities=int(row["ExtracurricularActivities"]),
            parental_support=row["ParentalSupport"],
            final_grade=float(row["FinalGrade"]),
        )
        database.insert_student(student.to_dict())
        count += 1
    return count
