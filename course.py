class Course:
    def __init__(self, name, code, credits, description):
        self.name = name
        self.code = code
        self.credits = credits
        self.description = description
    
    def __repr__(self):
        return f"Course(name={self.name}, code={self.code}, credits={self.credits})"

# Predefined courses
COURSES = [
    Course("Introduction to Python", "CS101", 3, "Master Python basics, including variables, loops, and functions for real-world applications."),
    Course("Data Structures & Algorithms", "CS201", 4, "Dive into arrays, linked lists, trees, and sorting algorithms for efficient coding."),
    Course("Web Development", "CS301", 3, "Build dynamic websites using HTML, CSS, JavaScript, and modern frameworks."),
    Course("Machine Learning", "CS401", 4, "Explore supervised and unsupervised learning, neural networks, and AI applications."),
    Course("Database Systems", "CS501", 3, "Learn SQL, NoSQL, and database design for scalable applications.")
]