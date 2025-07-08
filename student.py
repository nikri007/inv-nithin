
import json, re
from datetime import datetime

def load_data(file, default):
    try: return json.load(open(file))
    except: return default

def save_data(file, data):
    json.dump(data, open(file, 'w'), indent=2)

def validate(name, reg, age, email, phone, course):
    students = load_data("students.json", [])
    if len(name) < 2 or not name.replace(" ", "").isalpha(): return "Invalid name"
    if not (reg.isdigit() and len(reg) == 5): return "Invalid reg format"
    if any(s["reg"] == reg for s in students): return "Reg number exists"
    if not (18 <= int(age) <= 25): return "Age must be 18-25"
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): return "Invalid email"
    if any(s["email"] == email for s in students): return "Email exists"
    if not (phone.isdigit() and len(phone) == 10): return "Phone must be 10 digits"
    courses = ["Computer Science", "IT", "Electronics", "Mechanical", "Civil", "Business", "Math", "Physics", "Chemistry", "Biology"]
    if course not in courses: return "Invalid course"
    return None

def register():
    print("\n=== REGISTER STUDENT ===")
    name = input("Name: ").strip()
    reg = input("Reg Number (5 digits): ").strip()
    age = input("Age: ")
    email = input("Email: ").lower()
    phone = input("Phone (10 digits): ")
    
    courses = ["Computer Science", "IT", "Electronics", "Mechanical", "Civil", "Business", "Math", "Physics", "Chemistry", "Biology"]
    for i, c in enumerate(courses): print(f"{i+1}. {c}")
    course = courses[int(input("Select course: ")) - 1]
    
    error = validate(name, reg, age, email, phone, course)
    if error: print(f"Error: {error}"); return
    
    students = load_data("students.json", [])
    students.append({"name": name, "reg": reg, "age": int(age), "email": email, "phone": phone, "course": course, "date": datetime.now().strftime("%Y-%m-%d")})
    save_data("students.json", students)
    print("Student registered!")

def list_students():
    students = load_data("students.json", [])
    if not students: print("No students found!"); return
    
    print(f"\n=== STUDENTS ({len(students)}) ===")
    for s in students:
        print(f"{s['reg']} | {s['name']} | {s['age']} | {s['email']} | {s['course']}")

def search():
    students = load_data("students.json", [])
    if not students: print("No students!"); return
    
    print("1.Reg Number 2.Name 3.Email 4.Course")
    choice = input("Search by: ")
    
    if choice == "1":
        reg = input("Reg number: ").strip()
        found = [s for s in students if s["reg"] == reg]
    elif choice == "2":
        name = input("Name: ").lower()
        found = [s for s in students if name in s["name"].lower()]
    elif choice == "3":
        email = input("Email: ").lower()
        found = [s for s in students if s["email"] == email]
    elif choice == "4":
        course = input("Course: ")
        found = [s for s in students if course.lower() in s["course"].lower()]
    else: print("Invalid choice"); return
    
    if found:
        for s in found: print(f"{s['reg']} - {s['name']} ({s['course']})")
    else: print("No matches found")
