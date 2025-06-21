class Student:
       def __init__(self, name, email, student_id, age=None):
           self.name = name
           self.email = email
           self.student_id = student_id
           self.age = age
       
       def __repr__(self):
           return f"Student(name={self.name}, email={self.email}, student_id={self.student_id}, age={self.age})"