from datetime import datetime

class Enrollment:
    def __init__(self, student_id, course_name, enrollment_date=None):
        self.student_id = student_id
        self.course_name = course_name
        # Use existing date if provided, else set to now
        self.enrollment_date = enrollment_date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __repr__(self):
        return (
            f"Enrollment(student_id={self.student_id}, "
            f"course_name={self.course_name}, "
            f"date={self.enrollment_date})"
        )
