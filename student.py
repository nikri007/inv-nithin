import json, re
from datetime import datetime

def load_data(file, default):
    try: return json.load(open(file))
    except: return default

def save_data(file, data):
    json.dump(data, open(file, 'w'), indent=2)

def validate_name(name):
    if len(name.strip()) < 2: return "Name must be at least 2 characters"
    if len(name.strip()) > 20: return "Name cannot exceed 20 characters"
    if not name.replace(" ", "").isalpha(): return "Name can only contain letters and spaces"
    return None

def validate_reg_number(reg):
    if not reg.isdigit(): return "Registration number must contain only digits"
    if len(reg) != 5: return "Registration number must be exactly 5 digits"
    students = load_data("students.json", [])
    if any(s["reg"] == reg for s in students): return "Registration number already exists"
    return None

def validate_age(age_str):
    try:
        age = int(age_str)
        if not (18 <= age <= 25): return "Age must be between 18 and 25 years"
        return None
    except ValueError:
        return "Age must be a valid number"

def validate_email(email):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email): return "Invalid email format"
    students = load_data("students.json", [])
    if any(s["email"] == email.lower() for s in students): return "Email already exists"
    return None

def validate_phone(phone):
    if not phone.isdigit(): return "Phone number must contain only digits"
    if len(phone) != 10: return "Phone number must be exactly 10 digits"
    if phone.startswith('0'): return "Phone number should not start with 0"
    return None

def get_valid_name():
    while True:
        name = input("Name (2-20 characters, letters only): ").strip()
        error = validate_name(name)
        if not error:
            return name.title()  # Capitalize properly
        print(f"{error}")

def get_valid_reg_number():
    while True:
        reg = input("Registration Number (5 digits): ").strip()
        error = validate_reg_number(reg)
        if not error:
            return reg
        print(f"{error}")

def get_valid_age():
    while True:
        age = input("Age (18-25): ").strip()
        error = validate_age(age)
        if not error:
            return int(age)
        print(f" {error}")

def get_valid_email():
    while True:
        email = input("Email: ").strip().lower()
        error = validate_email(email)
        if not error:
            return email
        print(f" {error}")

def get_valid_phone():
    while True:
        phone = input("Phone Number (10 digits): ").strip()
        error = validate_phone(phone)
        if not error:
            return phone
        print(f"{error}")

def get_valid_course():
    courses = ["Computer Science", "IT", "Electronics", "Mechanical", "Civil", "Business", "Math", "Physics", "Chemistry", "Biology"]
    
    while True:
        print("\nAvailable Courses:")
        for i, c in enumerate(courses): 
            print(f"  {i+1}. {c}")
        
        try:
            choice = int(input("Select course (1-10): ").strip())
            if 1 <= choice <= len(courses):
                return courses[choice - 1]
            print(f" Please enter a number between 1 and {len(courses)}")
        except ValueError:
            print("Please enter a valid number")

def register():
    print("\n=== REGISTER STUDENT ===")
    print("Fill in the details below. Each field will be validated instantly.")
    print()
    
    # Collect data with instant validation
    name = get_valid_name()
    reg = get_valid_reg_number()
    age = get_valid_age()
    email = get_valid_email()
    phone = get_valid_phone()
    course = get_valid_course()
    
    # Show summary
    print("\nRegistration Summary:")
    print(f"Name: {name}")
    print(f"Registration: {reg}")
    print(f"Age: {age}")
    print(f"Email: {email}")
    print(f"Phone: {phone}")
    print(f"Course: {course}")
    
    confirm = input("\nConfirm registration? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Registration cancelled.")
        return
    
    # Save student
    students = load_data("students.json", [])
    students.append({
        "name": name,
        "reg": reg,
        "age": age,
        "email": email,
        "phone": phone,
        "course": course,
        "date": datetime.now().strftime("%Y-%m-%d")
    })
    save_data("students.json", students)
    print("Student registered successfully!")

def list_students():
    students = load_data("students.json", [])
    if not students: print("No students found!"); return
    
    print(f"\nSTUDENTS ({len(students)}) ===")
    print(f"{'Reg':<8} | {'Name':<20} | {'Age':<3} | {'Email':<25} | {'Course':<15}")
    print("-" * 80)
    for s in students:
        print(f"{s['reg']:<8} | {s['name']:<20} | {s['age']:<3} | {s['email']:<25} | {s['course']:<15}")

def search():
    students = load_data("students.json", [])
    if not students: print("No students to search!"); return
    
    print("\nSEARCH OPTIONS")
    print("1. By Registration Number")
    print("2. By Name")
    print("3. By Email")
    print("4. By Course")
    
    choice = input("Search by (1-4): ").strip()
    
    if choice == "1":
        reg = input("Enter registration number: ").strip()
        found = [s for s in students if s["reg"] == reg]
    elif choice == "2":
        name = input("Enter name (partial match): ").strip().lower()
        found = [s for s in students if name in s["name"].lower()]
    elif choice == "3":
        email = input("Enter email: ").strip().lower()
        found = [s for s in students if s["email"] == email]
    elif choice == "4":
        course = input("Enter course name: ").strip()
        found = [s for s in students if course.lower() in s["course"].lower()]
    else: 
        print(" Invalid choice"); 
        return
    
    if found:
        print(f"\n Found {len(found)} student(s):")
        print("-" * 50)
        for s in found: 
            print(f" {s['name']} ({s['reg']}) - {s['course']}")
            print(f"   {s['email']} | 📞 {s['phone']} | Age: {s['age']}")
            print()
    else: 
        print(" No students found matching your search")
