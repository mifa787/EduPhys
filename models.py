import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = "user_data.json"
ASSIGNMENTS_FILE = "assignments_data.json"
MATERIALS_FILE = "materials_data.json"

class User:
    def __init__(self, name, surname, status, password):
        self.name = name
        self.surname = surname
        self.status = status
        self.password = password
        self.username = f"{name.lower()}_{surname.lower()}"
        self.students = [] if self.status == "учитель" else None  # Список учеников для учителя

    def save(self):
        users = User.load_all()
        users[self.username] = {
            "name": self.name,
            "surname": self.surname,
            "status": self.status,
            "password": self.password,
            "students": self.students if self.status == "учитель" else None,  # Сохраняем список учеников, если это учитель
            "username": self.username  # Добавляем username в данные
        }
        with open(DATA_FILE, 'w') as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def load_all():
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def find(username):
        users = User.load_all()
        return users.get(username, None)


class Assignment:
    def __init__(self, teacher_username, student_username, title, description, deadline):
        self.teacher_username = teacher_username
        self.student_username = student_username
        self.title = title
        self.description = description
        self.deadline = deadline
        self.submission = None  # Initially no submission

    def save(self):
        assignments = Assignment.load_all()
        assignments[self.title] = {
            "teacher": self.teacher_username,
            "student": self.student_username,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "submission": self.submission
        }
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(assignments, f, indent=4)

    @staticmethod
    def load_all():
        if os.path.exists(ASSIGNMENTS_FILE):
            with open(ASSIGNMENTS_FILE, 'r') as f:
                return json.load(f)
        return {}

    @staticmethod
    def get_by_student(student_username):
        assignments = Assignment.load_all()
        return {title: assignment for title, assignment in assignments.items() if assignment["student"] == student_username}

    @staticmethod
    def get_by_teacher(teacher_username):
        assignments = Assignment.load_all()
        return {title: assignment for title, assignment in assignments.items() if assignment["teacher"] == teacher_username}

class Registration:
    def open_registration_window(self, root, app):
        registration_window = tk.Toplevel(root)
        registration_window.title("Регистрация")
        registration_window.geometry("500x700")  # Увеличиваем размер окна
        registration_window.configure(bg="#E6E6FA")

        tk.Label(registration_window, text="Имя:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_name = tk.Entry(registration_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_name.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Фамилия:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_surname = tk.Entry(registration_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_surname.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Статус:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)

        status_var = tk.StringVar(value="ученик")

        radio_teacher = tk.Radiobutton(registration_window, text="Учитель", variable=status_var, value="учитель", font=("Arial", 16), bg="#E6E6FA", fg="#333333")
        radio_teacher.pack(pady=5)

        radio_student = tk.Radiobutton(registration_window, text="Ученик", variable=status_var, value="ученик", font=("Arial", 16), bg="#E6E6FA", fg="#333333")
        radio_student.pack(pady=5)

        tk.Label(registration_window, text="Пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_password = tk.Entry(registration_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_password.pack(pady=10, padx=20, fill="x")

        tk.Label(registration_window, text="Повторите пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_confirm_password = tk.Entry(registration_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_confirm_password.pack(pady=10, padx=20, fill="x")

        def register():
            name = entry_name.get()
            surname = entry_surname.get()
            status = status_var.get()
            password = entry_password.get()
            confirm_password = entry_confirm_password.get()

            if name and surname and password and confirm_password:
                if password == confirm_password:
                    user = User(name, surname, status, password)
                    user.save()
                    messagebox.showinfo("Успех", "Регистрация прошла успешно!")
                    registration_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Пароли не совпадают!")
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(registration_window, text="Зарегистрироваться", command=register, bg="#4CAF50", fg="black", font=("Arial", 16), width=22, height=2, relief="raised", bd=5).pack(pady=30)

    def open_login_window(self, root, app):
        login_window = tk.Toplevel(root)
        login_window.title("Авторизация")
        login_window.geometry("500x500")
        login_window.configure(bg="#E6E6FA")

        tk.Label(login_window, text="Имя:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_name = tk.Entry(login_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_name.pack(pady=10, padx=20, fill="x")

        tk.Label(login_window, text="Фамилия:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_surname = tk.Entry(login_window, font=("Arial", 16), relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_surname.pack(pady=10, padx=20, fill="x")

        tk.Label(login_window, text="Пароль:", bg="#E6E6FA", fg="black", font=("Arial", 16)).pack(pady=10)
        entry_password = tk.Entry(login_window, font=("Arial", 16), show="*", relief="flat", highlightthickness=2, highlightbackground="#8A2BE2", width=30)
        entry_password.pack(pady=10, padx=20, fill="x")

        def login():
            name = entry_name.get()
            surname = entry_surname.get()
            password = entry_password.get()

            if name and surname and password:
                username = f"{name.lower()}_{surname.lower()}"
                user = User.find(username)
                if user and user["password"] == password:
                    if user["status"] == "учитель":
                        app.open_teacher_window(username)
                    else:
                        app.open_student_window(username)
                    login_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Неверные данные для входа.")
            else:
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля корректно.")

        tk.Button(login_window, text="Войти", command=login, bg="#2196F3", fg="black", font=("Arial", 16), width=22, height=2, relief="raised", bd=5).pack(pady=30)
