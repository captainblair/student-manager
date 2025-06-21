import streamlit as st
import json
import os
import plotly.express as px
import pandas as pd
from student import Student
from course import Course, COURSES
from enrollment import Enrollment

# Ensure data folder exists
os.makedirs('data', exist_ok=True)

# Expected fields for a Student
valid_keys = ['name', 'email', 'student_id', 'age']

# Initialize session state
if 'students' not in st.session_state:
    st.session_state.students = []
    if os.path.exists('data/students.json'):
        with open('data/students.json', 'r') as f:
            student_data = json.load(f)

            # Keep only the valid keys and fill in missing ones
            cleaned_students = []
            for s in student_data:
                student_clean = {k: s.get(k) for k in valid_keys}
                student_clean.setdefault('name', 'Unknown')
                student_clean.setdefault('email', '')
                student_clean.setdefault('student_id', '')
                student_clean.setdefault('age', 18)
                cleaned_students.append(Student(**student_clean))

            st.session_state.students = cleaned_students

if 'enrollments' not in st.session_state:
    st.session_state.enrollments = []
    if os.path.exists('data/enrollments.json'):
        with open('data/enrollments.json', 'r') as f:
            enrollment_data = json.load(f)
            st.session_state.enrollments = [Enrollment(**e) for e in enrollment_data]

# Save students to JSON
def save_students():
    with open('data/students.json', 'w') as f:
        json.dump([vars(student) for student in st.session_state.students], f, indent=4)

# Save enrollments to JSON
def save_enrollments():
    with open('data/enrollments.json', 'w') as f:
        json.dump([vars(enrollment) for enrollment in st.session_state.enrollments], f, indent=4)

# App configuration
st.set_page_config(page_title="EDUTUK Manager", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for vibrant, large UI
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #34D399, #2563EB); padding: 20px; }
    .stButton>button { background-color: #10B981; color: white; font-size: 18px; padding: 10px 20px; border-radius: 8px; }
    .stButton>button:hover { background-color: #059669; transform: scale(1.05); transition: 0.2s; }
    .stTextInput>div>input { font-size: 16px; padding: 10px; border-radius: 8px; }
    .stSelectbox>div>select { font-size: 16px; padding: 10px; border-radius: 8px; }
    .sidebar .sidebar-content { background: #1F2937; color: white; }
    .sidebar .stSelectbox { background: #374151; color: white; border-radius: 8px; }
    h1, h2, h3 { color: #1F2937; font-weight: bold; }
    .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .st-expander { background: #F3F4F6; border-radius: 8px; }
    .search-bar { font-size: 16px; padding: 10px; border-radius: 8px; width: 100%; }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.markdown("<h1 style='color: #10B981;'>EDUTUK</h1>", unsafe_allow_html=True)
st.sidebar.markdown("---")
page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Manage Students", "Manage Enrollments", "View Courses"],
    help="Select a section to explore"
)
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='color: #10B981; font-weight: bold;'> Developed by BlairSystems</p>", unsafe_allow_html=True)

# Main content
if page == "Dashboard":
    st.markdown("<h1>EDUTUK Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<div class='card'><p style='font-size: 18px;'>Welcome to EDUTUK! Monitor student progress, view enrollment statistics, and manage courses efficiently.</p></div>", unsafe_allow_html=True)
    
    # Dashboard metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='card'><h3>Total Students</h3><p style='font-size: 24px; color: #10B981;'>{len(st.session_state.students)}</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='card'><h3>Total Enrollments</h3><p style='font-size: 24px; color: #2563EB;'>{len(st.session_state.enrollments)}</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='card'><h3>Total Courses</h3><p style='font-size: 24px; color: #EF4444;'>{len(COURSES)}</p></div>", unsafe_allow_html=True)
    
    # Enrollment chart
    if st.session_state.enrollments:
        df = pd.DataFrame([vars(e) for e in st.session_state.enrollments])
        fig = px.bar(df, x='course_name', title="Enrollments by Course", color='course_name',
                     color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(title_font_size=20, xaxis_title="Course", yaxis_title="Number of Enrollments")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No enrollments available to display in the chart.")

elif page == "Manage Students":
    st.markdown("<h1>Manage Students</h1>", unsafe_allow_html=True)
    
    # Search bar
    search_query = st.text_input("Search Students", placeholder="Enter name or ID...", key="search_students",
                                 help="Search by student name or ID")
    
    # Add new student
    with st.form("add_student_form"):
        st.markdown("<h3>Add New Student</h3>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            student_id = st.text_input("Student ID")
        with col2:
            email = st.text_input("Email")
            age = st.number_input("Age", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Add Student")
        
        if submitted:
            if any(s.student_id == student_id for s in st.session_state.students):
                st.error("Student ID already exists!")
            else:
                student = Student(name, email, student_id, age)
                st.session_state.students.append(student)
                save_students()
                st.success("Student added successfully!")
    
    # Display and manage students
    st.markdown("<h3>Student List</h3>", unsafe_allow_html=True)
    if st.session_state.students:
        filtered_students = [s for s in st.session_state.students if
                            search_query.lower() in s.name.lower() or search_query in s.student_id]
        if filtered_students:
            for idx, student in enumerate(filtered_students):
                with st.expander(f"{student.name} (ID: {student.student_id})", expanded=True):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        new_name = st.text_input("Name", student.name, key=f"name_{idx}")
                        new_email = st.text_input("Email", student.email, key=f"email_{idx}")
                        new_age = st.number_input("Age", min_value=0, max_value=100, value=student.age or 18, step=1, key=f"age_{idx}")
                    with col2:
                        if st.button("Update", key=f"update_{idx}"):
                            student.name = new_name
                            student.email = new_email
                            student.age = new_age
                            save_students()
                            st.success("Student updated!")
                        if st.button("Delete", key=f"delete_{idx}", type="secondary"):
                            st.session_state.students = [s for s in st.session_state.students if s.student_id != student.student_id]
                            save_students()
                            st.success("Student deleted!")
                            st.experimental_rerun()
        else:
            st.warning("No students match the search criteria.")
    else:
        st.info("No students added yet.")

elif page == "Manage Enrollments":
    st.markdown("<h1>Manage Enrollments</h1>", unsafe_allow_html=True)
    
    # Enroll student
    with st.form("enroll_form"):
        st.markdown("<h3>Enroll Student</h3>", unsafe_allow_html=True)
        student_ids = [s.student_id for s in st.session_state.students]
        col1, col2 = st.columns(2)
        with col1:
            selected_student = st.selectbox("Select Student", student_ids, key="enroll_student")
        with col2:
            selected_course = st.selectbox("Select Course", [c.name for c in COURSES], key="enroll_course")
        submitted = st.form_submit_button("Enroll")
        
        if submitted:
            if any(e.student_id == selected_student and e.course_name == selected_course for e in st.session_state.enrollments):
                st.error("Student already enrolled in this course!")
            else:
                enrollment = Enrollment(selected_student, selected_course)
                st.session_state.enrollments.append(enrollment)
                save_enrollments()
                st.success(f"Student {selected_student} enrolled in {selected_course}!")
    
    # Display enrollments with filter
    st.markdown("<h3>Enrollment List</h3>", unsafe_allow_html=True)
    course_filter = st.selectbox("Filter by Course", ["All"] + [c.name for c in COURSES], key="course_filter")
    if st.session_state.enrollments:
        filtered_enrollments = [e for e in st.session_state.enrollments if course_filter == "All" or e.course_name == course_filter]
        for idx, enrollment in enumerate(filtered_enrollments):
            st.markdown(f"<div class='card'>Student ID: {enrollment.student_id}, Course: {enrollment.course_name}, Enrolled: {enrollment.enrollment_date}</div>", unsafe_allow_html=True)
            if st.button("Remove Enrollment", key=f"remove_enroll_{idx}", type="secondary"):
                st.session_state.enrollments = [e for e in st.session_state.enrollments if not (e.student_id == enrollment.student_id and e.course_name == enrollment.course_name)]
                save_enrollments()
                st.success("Enrollment removed!")
                st.experimental_rerun()
    else:
        st.info("No enrollments yet.")

elif page == "View Courses":
    st.markdown("<h1>Available Courses</h1>", unsafe_allow_html=True)
    for course in COURSES:
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <h3>{course.name} ({course.code})</h3>
                <p><strong>Credits:</strong> {course.credits}</p>
                <p>{course.description}</p>
            </div>
            """, unsafe_allow_html=True)