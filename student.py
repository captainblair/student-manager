# student.py

class Student:
    def __init__(self, name, age, course):
        self.name = name
        self.age = age
        self.course = course

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "course": self.course
        }
