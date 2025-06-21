# course.py

class Course:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def to_dict(self):
        return {
            "name": self.name,
            "code": self.code
        }

# Predefined courses
default_courses = [
    Course("Computer Science", "CS101"),
    Course("Business Administration", "BA201"),
    Course("Electrical Engineering", "EE301"),
    Course("Social Work", "SW401"),
    Course("Information Technology", "IT501")
]

def get_course_names():
    return [course.name for course in default_courses]
