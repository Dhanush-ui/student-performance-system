class Student:
    def __init__(self, student_id, name, gender, attendance_rate,
                 study_hours_per_week, previous_grade,
                 extracurricular_activities, parental_support, final_grade):
        self.student_id = student_id
        self.name = name
        self.gender = gender
        self.attendance_rate = attendance_rate
        self.study_hours_per_week = study_hours_per_week
        self.previous_grade = previous_grade
        self.extracurricular_activities = extracurricular_activities
        self.parental_support = parental_support
        self.final_grade = final_grade
        self.grade_letter = self.assign_grade_letter()
        self.passing = self.is_passing()

    def assign_grade_letter(self):
        score = self.final_grade
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def is_passing(self):
        return self.final_grade >= 60

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "gender": self.gender,
            "attendance_rate": self.attendance_rate,
            "study_hours_per_week": self.study_hours_per_week,
            "previous_grade": self.previous_grade,
            "extracurricular_activities": self.extracurricular_activities,
            "parental_support": self.parental_support,
            "final_grade": self.final_grade,
            "grade_letter": self.grade_letter,
            "is_passing": int(self.passing),
        }
