#!/usr/bin/env python3
import json
import getpass
from datetime import datetime, timedelta
from student import register, list_students, search

def load_data(file, default):
    try: return json.load(open(file))
    except: return default

def save_data(file, data):
    json.dump(data, open(file, 'w'), indent=2)

def login():
    attempts_data = load_data("attempts.json", {"fails": 0, "locked": None})
    if attempts_data["locked"] and datetime.now() < datetime.fromisoformat(attempts_data["locked"]):
        print("System locked! Try later."); return False
    
    for i in range(3):
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")  # Hidden password input
        
        if username == "admin" and password == "admin":
            save_data("attempts.json", {"fails": 0, "locked": None})
            return True
        print(f"Wrong! {2-i} attempts left")
    
    save_data("attempts.json", {"fails": 3, "locked": (datetime.now() + timedelta(minutes=5)).isoformat()})
    print("System locked for 5 minutes!"); return False

def main():
    print("School Management System\nLogin required!")
    if not login(): return
    
    while True:
        print("\n1.Register 2.List 3.Search 4.Exit")
        choice = input("Choice: ")
        
        if choice == "1": register()
        elif choice == "2": list_students()
        elif choice == "3": search()
        elif choice == "4": print("Goodbye!"); break
        else: print("Invalid choice")

if __name__ == "__main__": main()
