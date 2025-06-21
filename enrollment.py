# enrollment.py

class Enrollment:
    def __init__(self, student_name, course_name):
        self.student_name = student_name
        self.course_name = course_name

    def to_dict(self):
        return {
            "student_name": self.student_name,
            "course_name": self.course_name
        }

    def __str__(self):
        return f"📚 {self.student_name} is enrolled in {self.course_name}"

# Optional: You could also add a class method to load enrollments from a JSON file later
