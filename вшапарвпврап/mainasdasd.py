import json
import os
from datetime import datetime

USERS_FILE = "users.json"
TASKS_FILE = "tasks.json"


# ------------------ FILE HANDLING ------------------

def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)


def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


# ------------------ USER SYSTEM ------------------

def register_user(users):
    username = input("Create username: ").strip()
    if username in users:
        print("❌ Username already exists.")
        return None

    password = input("Create password: ").strip()
    users[username] = {"password": password}
    save_data(USERS_FILE, users)
    print("✅ Registration successful!")
    return username


def login_user(users):
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    if username in users and users[username]["password"] == password:
        print(f"✅ Welcome back, {username}!")
        return username
    else:
        print("❌ Invalid login.")
        return None


# ------------------ TASK MANAGEMENT ------------------

def add_task(tasks, user):
    title = input("Task title: ")
    priority = input("Priority (Low / Medium / High): ")
    deadline = input("Deadline (YYYY-MM-DD): ")

    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        print("❌ Invalid date format.")
        return

    task = {
        "title": title,
        "priority": priority,
        "deadline": deadline,
        "completed": False,
        "created_at": str(datetime.now())
    }

    tasks[user].append(task)
    save_data(TASKS_FILE, tasks)
    print("✅ Task added.")


def view_tasks(tasks, user):
    if not tasks[user]:
        print("📭 No tasks found.")
        return

    for i, task in enumerate(tasks[user], start=1):
        status = "✔ Done" if task["completed"] else "⏳ Pending"
        print(f"""
Task #{i}
Title     : {task['title']}
Priority  : {task['priority']}
Deadline  : {task['deadline']}
Status    : {status}
""")


def complete_task(tasks, user):
    view_tasks(tasks, user)
    try:
        index = int(input("Enter task number to mark complete: ")) - 1
        tasks[user][index]["completed"] = True
        save_data(TASKS_FILE, tasks)
        print("✅ Task marked as completed.")
    except:
        print("❌ Invalid selection.")


def delete_task(tasks, user):
    view_tasks(tasks, user)
    try:
        index = int(input("Enter task number to delete: ")) - 1
        removed = tasks[user].pop(index)
        save_data(TASKS_FILE, tasks)
        print(f"🗑 Deleted task: {removed['title']}")
    except:
        print("❌ Invalid selection.")


def task_stats(tasks, user):
    total = len(tasks[user])
    completed = sum(1 for t in tasks[user] if t["completed"])
    pending = total - completed

    print("\n📊 Task Statistics")
    print(f"Total     : {total}")
    print(f"Completed : {completed}")
    print(f"Pending   : {pending}")


# ------------------ MENUS ------------------

def task_menu(user):
    tasks = load_data(TASKS_FILE)
    if user not in tasks:
        tasks[user] = []

    while True:
        print("""
======== TASK MENU ========
1. Add Task
2. View Tasks
3. Complete Task
4. Delete Task
5. Task Statistics
6. Logout
===========================
""")
        choice = input("Choose: ")

        if choice == "1":
            add_task(tasks, user)
        elif choice == "2":
            view_tasks(tasks, user)
        elif choice == "3":
            complete_task(tasks, user)
        elif choice == "4":
            delete_task(tasks, user)
        elif choice == "5":
            task_stats(tasks, user)
        elif choice == "6":
            print("👋 Logged out.")
            break
        else:
            print("❌ Invalid option.")


def main():
    users = load_data(USERS_FILE)

    while True:
        print("""
===== PERSONAL TASK MANAGER =====
1. Register
2. Login
3. Exit
================================
""")
        choice = input("Choose: ")

        if choice == "1":
            user = register_user(users)
            if user:
                task_menu(user)
        elif choice == "2":
            user = login_user(users)
            if user:
                task_menu(user)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option.")


if __name__ == "__main__":
    main()


import json
import os
from datetime import datetime, timedelta

DATA_FILE = "tasks_data.json"


class Task:
    def __init__(self, title, priority, deadline):
        self.title = title
        self.priority = priority  # Low / Medium / High
        self.deadline = deadline
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None

    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "deadline": self.deadline,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }


class StudySession:
    def __init__(self, task_title, minutes):
        self.task_title = task_title
        self.minutes = minutes
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "task_title": self.task_title,
            "minutes": self.minutes,
            "date": self.date
        }


class TaskPlanner:
    def __init__(self):
        self.tasks = []
        self.study_sessions = []
        self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.study_sessions = data.get("sessions", [])
        else:
            self.tasks = []
            self.study_sessions = []

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "tasks": self.tasks,
                "sessions": self.study_sessions
            }, f, indent=4)

    def add_task(self, title, priority, deadline):
        task = Task(title, priority, deadline)
        self.tasks.append(task.to_dict())
        self.save_data()

    def complete_task(self, index):
        try:
            self.tasks[index]["completed"] = True
            self.tasks[index]["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
        except IndexError:
            print("Invalid task number.")

    def add_study_session(self, task_title, minutes):
        session = StudySession(task_title, minutes)
        self.study_sessions.append(session.to_dict())
        self.save_data()

    def overdue_tasks(self):
        now = datetime.now()
        overdue = []

        for task in self.tasks:
            if not task["completed"]:
                deadline = datetime.strptime(task["deadline"], "%Y-%m-%d")
                if deadline < now:
                    overdue.append(task)

        return overdue

    def show_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return

        for i, task in enumerate(self.tasks, 1):
            status = "✓" if task["completed"] else "✗"
            print(f"{i}. [{status}] {task['title']} | Priority: {task['priority']} | Deadline: {task['deadline']}")

    def study_statistics(self):
        total_minutes = sum(s["minutes"] for s in self.study_sessions)
        return total_minutes


def menu():
    print("\n==== SMART TASK & STUDY PLANNER ====")
    print("1. Add Task")
    print("2. Complete Task")
    print("3. Show Tasks")
    print("4. Add Study Session")
    print("5. Overdue Tasks")
    print("6. Study Statistics")
    print("7. Exit")


def main():
    planner = TaskPlanner()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            title = input("Task title: ")
            priority = input("Priority (Low/Medium/High): ")
            deadline = input("Deadline (YYYY-MM-DD): ")
            planner.add_task(title, priority, deadline)
            print("Task added.")

        elif choice == "2":
            planner.show_tasks()
            index = int(input("Task number to complete: ")) - 1
            planner.complete_task(index)
            print("Task marked as completed.")

        elif choice == "3":
            planner.show_tasks()

        elif choice == "4":
            task_title = input("Task title: ")
            minutes = int(input("Study minutes: "))
            planner.add_study_session(task_title, minutes)
            print("Study session recorded.")

        elif choice == "5":
            overdue = planner.overdue_tasks()
            if not overdue:
                print("No overdue tasks 🎉")
            else:
                print("Overdue tasks:")
                for task in overdue:
                    print(f"- {task['title']} (Deadline: {task['deadline']})")

        elif choice == "6":
            total = planner.study_statistics()
            print(f"Total study time: {total} minutes")

        elif choice == "7":
            print("Goodbye!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()