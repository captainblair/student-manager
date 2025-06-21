import streamlit as st
from student import Student  # Assuming you have a Student class
import json
import os

# ----- Styling -----
st.set_page_config(page_title="🎓 Student Manager", layout="wide")

st.markdown("""
    <style>
    .main {
        background-color: #f9fafc;
    }
    .title {
        font-size: 50px;
        font-weight: bold;
        color: #6C63FF;
        text-align: center;
        margin-bottom: 30px;
    }
    .subheader {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Sidebar -----
st.sidebar.title("📚 Menu")
page = st.sidebar.radio("Go to", ["➕ Add Student", "📋 View Students"])

# ----- Main Header -----
st.markdown("<div class='title'>🎓 Student Manager App</div>", unsafe_allow_html=True)

data_path = "data/students.json"

if not os.path.exists(data_path):
    with open(data_path, "w") as f:
        json.dump([], f)

# ----- Add Student -----
if page == "➕ Add Student":
    st.markdown("## 👤 Add a New Student")

    name = st.text_input("👤 Student Name")
    age = st.number_input("🎂 Age", min_value=1, step=1)
    course = st.selectbox("📚 Select Course", ["Computer Science", "Business", "Engineering", "Arts"])
    if st.button("💾 Save Student"):
        new_student = {
            "name": name,
            "age": age,
            "course": course
        }

        with open(data_path, "r") as f:
            students = json.load(f)
        students.append(new_student)

        with open(data_path, "w") as f:
            json.dump(students, f, indent=2)

        st.success(f"🎉 Student {name} saved successfully!")

# ----- View Students -----
elif page == "📋 View Students":
    st.markdown("## 👀 All Students")

    with open(data_path, "r") as f:
        students = json.load(f)

    if students:
        for student in students:
            st.markdown(f"""
                <div style='background-color:#ffffff;padding:10px 20px;border-radius:10px;margin-bottom:10px;box-shadow:0 0 5px rgba(0,0,0,0.1);'>
                    <b>👤 Name:</b> {student['name']} <br>
                    <b>🎂 Age:</b> {student['age']} <br>
                    <b>📚 Course:</b> {student['course']}
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No students found. Please add some.")
